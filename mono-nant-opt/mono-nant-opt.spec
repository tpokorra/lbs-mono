%define name mono-nant-opt
%define version 0.92
%define MonoPath /opt/mono
%define GitReference 97bf572559a00fec1d65d11deb3167b7ce6062e4

Summary: some development tools for Mono
Name: %{name}
Version: %{version}
Release: 7 
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development
Requires: pkgconfig mono-opt libgdiplus mono-libgdiplus-opt liberation-mono-fonts
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch mono-opt pkgconfig
%if 0%{?suse_version}
Requires: mono-opt-devel
BuildRequires: mono-opt-devel
%endif
BuildRoot: /tmp/buildroot
Source: %{GitReference}.tar.gz

%description
some development tools for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup  -q -n nant-%{GitReference}

%build
# Configure and make source
. /opt/mono/env.sh
sed -i "s#gmcs#mcs#g" Makefile
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
make prefix=%{MonoPath}

%install
rm -rf %{buildroot}
. /opt/mono/env.sh
make DESTDIR=%{buildroot} install prefix=%{MonoPath}
sed -i 's#/bin/mono#/bin/mono --runtime=v4.0#g' %{buildroot}%{MonoPath}/bin/nant

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%post

%changelog
* Thu Jul 11 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- using separate package mono-libgdiplus-opt
* Sat Jun 01 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
