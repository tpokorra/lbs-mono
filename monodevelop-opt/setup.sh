#!/bin/bash

function buildTarBallFromTag {
  tag=$1
  version=$2
  fileversion=$3
  git clone https://github.com/mono/monodevelop.git $tag
  cd $tag
  git branch release $tag
  . /opt/mono/env.sh
  ./configure
  make dist
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" monodevelop-opt*.spec
  sed -i "s/%define fileversion.*/%define fileversion $fileversion/g" monodevelop-opt*.spec
  cp $branch/monodevelop-$version.tar.bz2 ~/tarball
  mv $branch/monodevelop-$version.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $branch
}

mkdir ~/sources
yum install -y git-core automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2

buildTarBallFromTag monodevelop-4.2.5.0 4.2.5 4.2.5.0

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
