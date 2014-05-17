#!/bin/bash

function buildTarBall {
  branch=$1
  git clone https://github.com/mono/mono.git $branch
  cd $branch
  git checkout --track remotes/origin/$branch
  . /opt/mono/env.sh
  ./autogen.sh
  make dist
  cd ..
  echo "DONE with building the tarball for " $branch
}

yum install -y git-core automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2

buildTarBall master
buildTarBall mono-3.4.0-branch

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
