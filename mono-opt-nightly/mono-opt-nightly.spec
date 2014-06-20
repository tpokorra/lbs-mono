%define name mono-opt-nightly
%define version 1.0.0
%define tarballversion 1.0.0
%define MonoPath /opt/mono

Summary: Mono
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development/Languages/Mono
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch dos2unix libgdiplus
BuildRoot: /tmp/buildroot
Provides: mono-opt
Source: mono-nightly.tar.bz2

%description
Mono

%package devel
License:      GPL
Group:        Development/Libraries
Summary:      development files for Mono
Requires:     %{name} = %{version}
%description devel
Development files for Mono

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n mono-%{tarballversion}

%build
# Configure and make source
./configure --prefix=%{MonoPath}
make

%install
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

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%exclude %{MonoPath}/include
%exclude %{MonoPath}/lib/pkgconfig
%exclude %{MonoPath}/lib/*.a
%exclude %{MonoPath}/lib/*.so
%{MonoPath}

%files devel
%{MonoPath}/include
%{MonoPath}/lib/pkgconfig
%{MonoPath}/lib/*.so
%{MonoPath}/lib/*.a

%changelog
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
* Wed Sep 26 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.3
* Wed Aug 14 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.1
* Wed Jul 31 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- split into mono-opt and mono-opt-devel, required by SUSE packaging
* Mon Jul 29 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.2.0
* Wed Jul 17 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono 3.0.12

