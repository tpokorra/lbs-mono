%define name mono-opt
%define version 4.4.0
%define fileversion 4.4.0.182
%define MonoPath /opt/mono

Summary: Mono
Name: %{name}
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development/Languages/Mono
BuildRequires: bison gettext make bzip2 automake patch dos2unix libgdiplus mono-llvm-opt mono-llvm-opt-devel
%if 0%{?rhel} < 7
# need newer gcc version
BuildRequires: devtoolset-2-gcc >= 4.7 devtoolset-2-gcc-c++ devtoolset-2-binutils
%else
BuildRequires: gcc >= 4.7 gcc-c++ libtool
%endif
%if 0%{?suse_version}
BuildRequires: timezone
Requires: timezone
%else
Obsoletes: mono-opt-devel
%endif

BuildRoot: /tmp/buildroot
Source: mono-%{fileversion}.tar.bz2
Source1: env.sh
Patch0: mono-4.0.0-libgdiplusconfig.patch

%description
Mono

%if 0%{?suse_version}
%package devel
License:      GPL
Group:        Development/Libraries
Summary:      development files for Mono
Requires:     %{name} = %{version}
%description devel
Development files for Mono
%endif

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n mono-%{version}
%patch0 -p1

%build

%if 0%{?rhel} < 7
# we need a newer gcc
PATH=/opt/rh/devtoolset-2/root/usr/bin:$PATH
CC=/opt/rh/devtoolset-2/root/usr/bin/gcc
CPP=/opt/rh/devtoolset-2/root/usr/bin/cpp
CXX=/opt/rh/devtoolset-2/root/usr/bin/c++
%endif

# Configure and make source
./configure --prefix=%{MonoPath} --enable-llvm --with-llvm=%{MonoPath}
make

%install

%if 0%{?rhel} < 7
# we need a newer gcc
PATH=/opt/rh/devtoolset-2/root/usr/bin:$PATH
CC=/opt/rh/devtoolset-2/root/usr/bin/gcc
CPP=/opt/rh/devtoolset-2/root/usr/bin/cpp
CXX=/opt/rh/devtoolset-2/root/usr/bin/c++
%endif

rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
find %{buildroot} -iname "*.exe.so" -exec rm '{}' ';'
# fix problem with symbolic link for mono pointing at absolute path
ln -sf mono-sgen %{buildroot}/%{MonoPath}/bin/mono
# fix problems with wrong symbolic link
# ERROR: link target doesn't exist (neither in build root nor in installed system):
#   /opt/mono/lib/mono/xbuild/12.0/bin/Mono.XBuild.Tasks.dll -> /opt/mono/lib/mono/xbuild/12.0/gac/Mono.XBuild.Tasks/4.0.0.0__0738eb9f132ed756/Mono.XBuild.Tasks.dll
cd %{buildroot}/%{MonoPath}/lib/mono/xbuild/12.0/bin;
ln -sf ../../../gac/Mono.XBuild.Tasks/4.0.0.0__0738eb9f132ed756/Mono.XBuild.Tasks.dll
ln -sf ../../../gac/Microsoft.Build.Tasks.v12.0/12.0.0.0__b03f5f7f11d50a3a/Microsoft.Build.Tasks.v12.0.dll
ln -sf ../../../gac/Microsoft.Build.Framework/12.0.0.0__b03f5f7f11d50a3a/Microsoft.Build.Framework.dll
ln -sf ../../../gac/Microsoft.Build/12.0.0.0__b03f5f7f11d50a3a/Microsoft.Build.dll
ln -sf ../../../gac/Microsoft.Build.Engine/12.0.0.0__b03f5f7f11d50a3a/Microsoft.Build.Engine.dll
ln -sf ../../../gac/Microsoft.Build.Utilities.v12.0/12.0.0.0__b03f5f7f11d50a3a/Microsoft.Build.Utilities.v12.0.dll
cd -

cp ../../SOURCES/env.sh %{buildroot}/%{MonoPath}
chmod a+x %{buildroot}/%{MonoPath}/env.sh
rm -f %{buildroot}/%{MonoPath}/share/libgc-mono/README.OS2
rm -f %{buildroot}/%{MonoPath}/share/libgc-mono/README.Mac
rm -f %{buildroot}/%{MonoPath}/share/libgc-mono/README.win32

# remove the mono-nunit files
rm -f %{buildroot}%{_bindir}/nunit-console
rm -f %{buildroot}%{_bindir}/nunit-console2
rm -f %{buildroot}%{_bindir}/nunit-console4
rm -f %{buildroot}%{_monodir}/4.5/nunit*
rm -Rf %{buildroot}%{_monodir}/gac/nunit*
rm -f %{buildroot}%{_libdir}/pkgconfig/mono-nunit.pc

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%if 0%{?suse_version}
%exclude %{MonoPath}/include
%exclude %{MonoPath}/lib/pkgconfig
%exclude %{MonoPath}/lib/*.a
%exclude %{MonoPath}/lib/*.so
%endif
%{MonoPath}

%if 0%{?suse_version}
%files devel
%{MonoPath}/include
%{MonoPath}/lib/pkgconfig
%{MonoPath}/lib/*.so
%{MonoPath}/lib/*.a
%endif

%changelog
* Tue Jun 14 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.4.0-1
- update to Mono 4.4.0.182, Cycel 7 Final
* Sat Feb 13 2016 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.2.2-2
- update to Mono 4.2.2 Cycle 6 Service Release 1
* Mon Nov 23 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.2.1.102 aka Cycle 6 Final
* Thu Oct 08 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.0.4.1 aka Cycle 5 Service Release 4
* Tue Aug 04 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- obsoletes mono-opt-devel for all but OpenSUSE
* Mon Jul 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- only create a mono-opt-devel package for OpenSUSE, but for other Distributions: create one package mono-opt
* Thu Jul 02 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.0.2.5 aka 4.0.2 SR2
* Wed Jun 03 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.0.1.44 aka 4.0.1 SR1
* Wed May 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.0.1.28
* Mon Apr 27 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 4.0.1
* Fri Apr 24 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Drop the mono-nunit 2.4.8, we have now a separate package nunit-opt with 2.6.3
* Sat Mar 07 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.12.1
* Tue Jan 13 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.12.0
* Sat Oct 04 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.10.0
* Thu Sep 04 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.8.0
* Fri Aug 15 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Enabling llvm
* Wed Aug 13 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.6.0
* Tue Apr 01 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.4.0
* Thu Feb 20 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.8
* Sat Jan 18 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.6
* Thu Dec 05 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- including a patch so that mono-tools build
* Mon Dec 02 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.5
* Thu Sep 26 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.3
* Wed Aug 14 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.1
* Wed Jul 31 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- split into mono-opt and mono-opt-devel, required by SUSE packaging
* Mon Jul 29 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.0
* Wed Jul 17 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.0.12
