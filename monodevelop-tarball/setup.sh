#!/bin/bash

function buildTarBallFromTag {
  tag=$1
  version=$2
  fileversion=$3
  branch=$tag
  git clone --depth 1 https://github.com/mono/monodevelop.git $branch
  cd $branch
  git branch release $branch
  git checkout release

  ./configure --profile=stable || exit 1

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
  echo "download at https://download.solidcharity.com/tarballs/tpokorra/mono/monodevelop-$fileversion.tar.bz2"
}

mkdir ~/sources

dnf install -y git-core make automake autoconf libtool tar which gcc-c++ gettext bzip2 wget \
               automake autoconf libtool mono-core mono-devel libgdiplus pkgconfig \
               shared-mime-info intltool gtk-sharp2-devel gnome-sharp-devel

#buildTarBallFromTag monodevelop-5.6.3.3 5.6.3 5.6.3.3
buildTarBallFromTag monodevelop-6.0.0.5174 6.0 6.0.0.5174

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
