#!/bin/bash
branch=mono-3.4.0-branch

yum install -y automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2
wget https://github.com/mono/mono/archive/$branch.tar.gz
tar xzf $branch.tar.gz
cd mono-$branch
./autogen.sh
. /opt/mono/env.sh
make dist

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
