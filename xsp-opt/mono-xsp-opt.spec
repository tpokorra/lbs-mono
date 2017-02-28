%define name mono-xsp-opt
%define version 4.4
%define MonoPath /opt/mono

Summary: XSP built for Mono
Name: %{name}
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <tp@tbits.net>
License: GPL
Group: Productivity/Networking/Web/Utilities
Requires: pkgconfig mono-opt
BuildRequires: gcc libtool bison gettext make bzip2 autoconf automake libtool gcc-c++ patch mono-opt pkgconfig sqlite
%if 0%{?suse_version}
Requires: mono-opt-devel
BuildRequires: mono-opt-devel
%endif
BuildRoot: /tmp/buildroot
Source: https://github.com/mono/xsp/archive/%{version}.tar.gz

%description
XSP built for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup -q -n xsp-%{version}

%build
# Configure and make source
. %{MonoPath}/env.sh
./autogen.sh --prefix=%{MonoPath} --disable-docs
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
* Fri Aug 02 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
