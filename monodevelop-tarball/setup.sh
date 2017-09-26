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
  git clone --depth 1 https://github.com/mono/monodevelop.git -b $branch $branch || exit 1
  cd $branch
  git checkout -b release || exit 1

  # somehow the version in version.config is already one ahead???
  sed -i "s#^Version=.*#Version=$version#" version.config
  sed -i "s#^Label=.*#Label=$version#" version.config
  git commit version.config -m "setting version.config to $version"

  # let the distribution decide if they want to use external dlls and exes or not
  #patch -p1 < ../notdeletingdlls.patch || exit 1
  # download the nuget packages
  #patch -p1 < ../downloadnugetpackages.patch || exit 1

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

  # now create archives for some nuget binary packages
  cd $branch/main
  tar czf ~/tarball/nuget-binary.tar.gz external/nuget-binary
  cd -
  p=`pwd`/$branch/packages
  mkdir -p $p
  cd $branch/main/src/core/MonoDevelop.Core
  mono ../../../external/nuget-binary/nuget.exe restore -PackagesDirectory $p || exit -1
  cd -
  cd $branch
  find packages -name '*.nupkg' -exec rm -f {} \;
  find packages -name 'portable-net45+win8' -exec rm -Rf {} \;
  find packages -name 'netstandard1.3' -exec rm -Rf {} \;
  tar czf ~/tarball/Microsoft.CodeAnalysis.1.3.2.tar.gz packages/Microsoft.CodeAnalysis.*.1.3.2 || exit -1
  tar czf ~/tarball/Microsoft.Composition.1.0.27.tar.gz packages/Microsoft.Composition.1.0.27 || exit -1
  tar czf ~/tarball/Newtonsoft.Json.8.0.3.tar.gz packages/Newtonsoft.Json.8.0.3 || exit -1
  tar czf ~/tarball/System.Collections.Immutable.1.1.37.tar.gz packages/System.Collections.Immutable.1.1.37 || exit -1
  cd -
}

mkdir -p ~/sources

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
          mono-complete mono-devel fsharp gnome-sharp2 gtk-sharp2 libssh2-1-dev nuget zlib libssh2
fi

#buildTarBallFromTag monodevelop-5.6.3.3 5.6.3 5.6.3.3
#buildTarBallFromTag monodevelop-6.2.0.1821 6.2 6.2.0.1821
buildTarBallFromTag monodevelop-7.1.0.1291 7.1 7.1.0.1291
#buildTarBallFromTag monodevelop-7.1.5.2 7.1.5 7.1.5.2

# tell the LBS that the calling python script can continue
echo "LBSScriptFinished"
