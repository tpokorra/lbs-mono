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
  # only apply for Monodevelop >= 5.2
  if [ -f main/src/addins/AspNet/MonoDevelop.AspNet.csproj ]
  then
    if [[ $branch == monodevelop-5.2* || $branch == monodevelop-5.3* ]]
    then
      patch -p1 < ../nuget_aspnet_5.2.patch || exit 1
    else
      if [[ $branch == monodevelop-5.4* ]]
      then
        patch -p1 < ../nuget_aspnet.patch || exit 1
        patch -p1 < ../NUnitRunner.patch || exit 1
      else
        patch -p1 < ../nuget_aspnet_master.patch || exit 1
      fi
    fi
  fi

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

buildTarBallFromTag monodevelop-5.5.4.15 5.5.4 5.5.4.15
buildTarBallFromTag monodevelop-5.6.3.3 5.6.3 5.6.3.3

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
