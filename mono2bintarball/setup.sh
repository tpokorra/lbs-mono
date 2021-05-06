#!/bin/bash

MONO_PACKAGES=mono-xsp4 mono-fastcgi-server4 ca-certificates-mono

apt-get -y install python3

# get the installed packages on the target system (at Hostsharing)
. ~/.ssh/LOGIN_TARGET_SYSTEM_ENV.sh
ssh $TARGET_USER@$TARGET_HOST "dpkg-query -f '\${Package}\n' -W" > pkgs_target.txt || exit -1

# we are using our own repo for newer Mono for Debian Buster
echo "deb [arch=amd64] https://lbs.solidcharity.com/repos/tpokorra/mono/debian/buster buster main" > /etc/apt/sources.list.d/mono-tpokorra.list
apt-get update

# get the packages that will be installed on a clean Debian Buster system
apt-get install $MONO_PACKAGES --dry-run | grep -E "^Inst " | awk '{print $2}' > pkgs_mono.txt || exit -1

# install the mono packages
apt-get -y install $MONO_PACKAGES || exit -1

# this will check for all packages that have been installed, that are not installed on the target system
# all files from those packages will be added to a binary tarball, ~/tarball/mono
python3 mono2bintarball.py || exit -1

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
