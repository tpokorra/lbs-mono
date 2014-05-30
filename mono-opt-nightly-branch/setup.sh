#!/bin/bash

function buildTarBall {
  branch=$1
  git clone https://github.com/mono/mono.git $branch
  cd $branch
  git checkout --track remotes/origin/$branch
  . /opt/mono/env.sh
  ./autogen.sh
  make dist
  # get the version number from the generated tarball, eg. mono-3.6.1.tar.bz2
  filename=`ls mono-*.tar.bz2`
  # cut off .bz2
  version=${filename%.*}
  # cut off .tar
  version=${version%.*}
  # cut off mono-
  version=${version#*-}
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" mono-opt-nightly*.spec
  mv $branch/mono-$version.tar.bz2 ~/sources/mono-branch-nightly.tar.bz2

  echo "DONE with building the tarball for " $branch
}

mkdir ~/sources
yum install -y git-core automake autoconf libtool tar which gcc-c++ gettext mono-opt bzip2

buildTarBall mono-3.6.0-branch

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
