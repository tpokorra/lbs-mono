#!/bin/bash

function buildTarBallFromTag {
  tag=$1
  version=$2
  fileversion=$3
  branch=$tag
  git clone https://github.com/mono/monodevelop.git $branch
  cd $branch
  git branch release $branch
  git checkout release
  . /opt/mono/env.sh
  ./configure --profile=stable
  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s
  make dist
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" monodevelop-opt*.spec
  sed -i "s/%define fileversion.*/%define fileversion $fileversion/g" monodevelop-opt*.spec
  cp $branch/tarballs/monodevelop-$version.tar.bz2 ~/tarball
  mv $branch/tarballs/monodevelop-$version.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $branch
  echo "download at http://lbs.solidcharity.com/tarballs/mono/monodevelop-4.2.5.tar.bz2"
}

mkdir ~/sources
if [ -f /etc/redhat-release ] 
then
  yum install -y git-core automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2
else
  apt-get install -y --force-yes git-core automake autoconf libtool tar build-essential gettext mono-opt bzip2
  # TODO should be done via .dsc file, build required:
  apt-get install -y --force-yes debhelper automake make libgdiplus bash pkg-config shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt autoconf hostname
fi

buildTarBallFromTag monodevelop-4.2.5.0 4.2.5 4.2.5.0

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
