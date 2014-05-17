#!/bin/bash

function buildTarBall {
  branch=$1
  version=$2
  git clone https://github.com/mono/mono.git $branch
  cd $branch
  git checkout --track remotes/origin/$branch
  . /opt/mono/env.sh
  ./autogen.sh
  make dist
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" mono-opt-nightly*.spec
  mv $branch/mono-$version.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $branch
}

mkdir ~/sources
yum install -y git-core automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2

buildTarBall master 3.4.1

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
