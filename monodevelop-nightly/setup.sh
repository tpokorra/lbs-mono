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
  echo "current revision of git $giturl $branch: " `git rev-parse HEAD`
  . /opt/mono/env.sh
  ./configure --profile=stable

  # install the certificates for nuget, see http://stackoverflow.com/questions/15181888/nuget-on-linux-error-getting-response-stream
  # this is needed for Microsoft AspNet
  # only apply for Monodevelop >= 5.2
  if [ -f main/src/addins/AspNet/MonoDevelop.AspNet.csproj ]
  then
    if [[ "$branch" == "monodevelop-5.2-branch" || "$branch" == "monodevelop-5.3-branch" ]]
    then
      patch -p1 < ../nuget_aspnet_5.2.patch || exit 1
    else
      patch -p1 < ../nuget_aspnet.patch || exit 1
      patch -p1 < ../NUnitRunner.patch || exit 1
    fi
  fi

  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s, need newer autoconf
  make dist || exit 1

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
    exit 1
  fi
  cp work/tarballs/monodevelop-*.tar.bz2 ~/tarball/monodevelop-$branch-nightly.tar.bz2
  mv work/tarballs/monodevelop-*.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $giturl $branch
  echo "download at http://lbs.solidcharity.com/tarballs/tpokorra/mono/monodevelop-$branch-nightly.tar.bz2"
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
