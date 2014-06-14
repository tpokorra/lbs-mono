#!/bin/bash

function buildTarBall {
  giturl=$1
  branch=$2
  git clone $giturl work
  cd work
  if [[ "$branch" != "master" ]]
  then
    git checkout --track remotes/origin/$branch
  fi
  . /opt/mono/env.sh
  ./configure --profile=stable
  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s, need newer autoconf
  make dist
  status=$?
  if [ $status -ne 0 ]
  then
    echo "LBSERROR: error during make dist"
  fi

  line=`cat version.config | grep "^Version"`
  fileversion=${line:8}
  version="$fileversion.99"
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" monodevelop*.spec
  sed -i "s/%define fileversion.*/%define fileversion $fileversion/g" monodevelop*.spec
  
  if [[ ! `ls work/tarballs/monodevelop-*.tar.bz2` ]]
  then
    echo "LBSERROR: no tarball was created"
  fi
  cp work/tarballs/monodevelop-*.tar.bz2 ~/tarball/monodevelop-$branch-nightly.tar.bz2
  mv work/tarballs/monodevelop-*.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $giturl $branch
  echo "download at http://lbs.solidcharity.com/tarballs/tpokorra/mono/monodevelop-nightly.tar.bz2"
}

mkdir ~/sources
if [ -f /etc/redhat-release ] 
then
  gitpackage=git-core
  # for CentOS6, we need a newer version of git, see issue https://github.com/tpokorra/lbs-mono/issues/5
  if [ "`cat /etc/redhat-release | grep 'CentOS release 6'`" ]
  then
    rpm -Uhv http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/epel-release-6-5.noarch.rpm
    rpm -Uhv http://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-11.ius.centos6.noarch.rpm
    gitpackage=git18
  fi
  yum install -y $gitpackage make automake autoconf libtool tar which gcc-c++ gettext bzip2
else
  apt-get install -y --force-yes git-core automake autoconf libtool tar build-essential gettext mono-opt bzip2
fi

# build nightly from master
branch=$1
buildTarBall "https://github.com/mono/monodevelop.git" $branch

# build testbuild from my branch
#buildTarBall "https://github.com/tpokorra/monodevelop.git" testtimo

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
