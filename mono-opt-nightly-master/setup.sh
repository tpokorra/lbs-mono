#!/bin/bash

function buildTarBall {
    echo "LBSERROR: no tarball was created"
    echo "LBSScriptFinished"
    exit 1
  giturl=$1
  branch=$2
  git clone $giturl work
  cd work
  if [[ "$branch" != "master" ]]
  then
    git checkout --track remotes/origin/$branch
  fi
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
  tarballversion=${version#*-}
  version="$tarballversion.99"
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" mono-opt-nightly*.spec
  sed -i "s/%define tarballversion.*/%define tarballversion $tarballversion/g" mono-opt-nightly*.spec

  cp work/tarballs/monodevelop-*.tar.bz2 ~/tarball/mono-$branch-nightly.tar.bz2
  mv work/mono-*.tar.bz2 ~/sources/mono-$branch-nightly.tar.bz2
  if [[ ! -f ~/tarball/mono-$branch-nightly.tar.bz2 ]]
  then
    echo "LBSERROR: no tarball was created"
    echo "LBSScriptFinished"
    exit 1
  fi
  echo "DONE with building the tarball for " $branch
  echo "download at http://lbs.solidcharity.com/tarballs/tpokorra/mono/mono-$branch-nightly.tar.bz2"
  exit 0
}

mkdir ~/sources

if [ -f /etc/redhat-release ] 
then
  yum install -y git-core
else
  apt-get install -y --force-yes git-core
fi

buildTarBall "https://github.com/mono/mono.git" master
result=$?
# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"

exit $result
