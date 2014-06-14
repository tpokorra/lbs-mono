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
  yum install -y git-core make automake autoconf libtool tar which gcc-c++ gettext bzip2
  # TODO should get these packages from the spec file, BuildRequires:
  yum install -y automake autoconf libtool mono-opt mono-opt-devel libgdiplus pkgconfig shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt
else
  apt-get install -y --force-yes git-core automake autoconf libtool tar build-essential gettext mono-opt bzip2
  # TODO should be done via .dsc file, build required:
  apt-get install -y --force-yes debhelper automake make libgdiplus bash pkg-config shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt autoconf hostname
fi

# build nightly from master
branch=$1
buildTarBall "https://github.com/mono/monodevelop.git" $branch

# build testbuild from my branch
#buildTarBall "https://github.com/tpokorra/monodevelop.git" testtimo

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
