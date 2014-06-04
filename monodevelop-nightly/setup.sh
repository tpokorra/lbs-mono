#!/bin/bash

function buildTarBallFromMaster {
  tag=$1
  version=$2
  fileversion=$3
  branch=master
  git clone https://github.com/mono/monodevelop.git $branch
  #git clone https://github.com/tpokorra/monodevelop $branch
  cd $branch
  #git checkout --track remotes/origin/FixTarball
  . /opt/mono/env.sh
  ./configure --profile=stable
  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s
  make dist
  cd ..
  # adjust the spec file for correct version number
  sed -i "s/%define version.*/%define version $version/g" monodevelop*.spec
  sed -i "s/%define fileversion.*/%define fileversion $fileversion/g" monodevelop*.spec
  cp $branch/tarballs/monodevelop-$version.tar.bz2 ~/tarball/monodevelop-nightly.tar.bz2
  mv $branch/tarballs/monodevelop-$version.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $branch
  echo "download at http://lbs.solidcharity.com/tarballs/mono/monodevelop-nightly.tar.bz2"
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
buildTarBallFromMaster master 5.1.99 5.1

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
