#!/bin/bash

# because of bug https://bugzilla.xamarin.com/show_bug.cgi?id=39191
# "execvp: /bin/sh: Argument list too long"
# we cannot build on Fedora, I tried with Rawhide in June 2016 (future F25)
# need to build on Ubuntu 14.04

function buildTarBallFromTag {
  tag=$1
  version=$2
  fileversion=$3
  branch=$tag
  git clone --depth 1 https://github.com/mono/monodevelop.git $branch
  cd $branch
  git branch release $branch
  git checkout release

  # somehow the version in version.config is already one ahead???
  sed -i "s#^Version=.*#Version=$version#" version.config
  sed -i "s#^Label=.*#Label=$version#" version.config

  ./configure --profile=stable || exit 1

  # this does not seem to work for CentOS: error: possibly undefined macro: m4_esyscmd_s
  make dist || exit 1
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

if [ -f /etc/redhat-release ]
then
  dnf install -y 'dnf-command(config-manager)'
  dnf config-manager --add-repo http://download.mono-project.com/repo/centos/
  rpm --import "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF"

  dnf install -y git-core make cmake automake autoconf libtool tar which gcc-c++ gettext bzip2 wget \
               automake autoconf libtool mono-core mono-devel libgdiplus pkgconfig \
               shared-mime-info intltool gtk-sharp2-devel gnome-sharp-devel fsharp monodoc-devel \
               libssh2-devel
else
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
  echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
  apt-get update
  apt-get -y install git cmake automake autoconf tar intltool \
          mono-complete mono-devel fsharp gnome-sharp2 gtk-sharp2 libssh2-1-dev
fi

#buildTarBallFromTag monodevelop-5.6.3.3 5.6.3 5.6.3.3
buildTarBallFromTag monodevelop-6.0.1.8 6.0 6.0.1.8

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
