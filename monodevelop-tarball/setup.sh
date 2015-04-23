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

  # install the certificates for nuget, see http://stackoverflow.com/questions/15181888/nuget-on-linux-error-getting-response-stream
  # this is needed for Microsoft AspNet
  patch -p1 < ../nuget_aspnet_master.patch || exit 1

  # quick fix to include dlls and .exe files in the tarball
  # reverting commit https://github.com/mono/monodevelop/commit/a6ce3fd8982770e8d72bfdfb1cd8c5d2c11fdd6b
  sed -i "s#find tarballs/monodevelop#echo Disabled: find tarballs/monodevelop#g" Makefile

  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s
  make dist
  cd ..
  if [ "`ls monodevelop-opt*.spec`" != "" ];
  then
    # adjust the spec file for correct version number
    sed -i "s/%define version.*/%define version $version/g" monodevelop-opt*.spec
    sed -i "s/%define fileversion.*/%define fileversion $fileversion/g" monodevelop-opt*.spec
  fi
  cp $branch/tarballs/monodevelop-$version.tar.bz2 ~/tarball/monodevelop-$fileversion.tar.bz2 || exit 1
  mv $branch/tarballs/monodevelop-$version.tar.bz2 ~/sources

  echo "DONE with building the tarball for " $branch
  echo "download at http://download.lbs.solidcharity.com/tarballs/tpokorra/mono/monodevelop-$fileversion.tar.bz2"
}

mkdir ~/sources

cd /etc/yum.repos.d/
wget http://download.opensuse.org/repositories/home:tpokorra:mono/Fedora_21/home:tpokorra:mono.repo
cd -

yum install -y git-core make automake autoconf libtool tar which gcc-c++ gettext bzip2
yum install -y automake autoconf libtool mono-opt mono-opt-devel libgdiplus pkgconfig shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt

#buildTarBallFromTag monodevelop-5.6.3.3 5.6.3 5.6.3.3
buildTarBallFromTag monodevelop-5.9.0.431 5.9 5.9.0.431

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
