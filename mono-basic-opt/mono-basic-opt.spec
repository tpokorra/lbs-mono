%define name mono-basic-opt
%define version 4.0.1
%define MonoPath /opt/mono

Summary: Basic compiler for Mono
Name: %{name}
Version: %{version}
Release: 4
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Productivity/Networking/Web/Utilities
Requires: pkgconfig mono-opt
BuildRequires: gcc libtool bison gettext make bzip2 autoconf automake libtool gcc-c++ patch mono-opt pkgconfig sqlite
%if 0%{?suse_version}
Requires: mono-opt-devel
BuildRequires: mono-opt-devel
%endif
BuildRoot: /tmp/buildroot
Source: mono-basic-%{version}.tar.bz2

%description
Basic compiler for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup -q -n mono-basic-%{version}

%build
# Configure and make source
. %{MonoPath}/env.sh
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
./configure --prefix=%{MonoPath}
make

%install
rm -rf %{buildroot}
. %{MonoPath}/env.sh
make DESTDIR=%{buildroot} install

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%post

%changelog
* Sat May 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.0.1
* Fri Feb 07 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
