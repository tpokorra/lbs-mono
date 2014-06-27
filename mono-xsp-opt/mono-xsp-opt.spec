%define name mono-xsp-opt
%define version 3.0.99
%define MonoPath /opt/mono
%define XSPGitReference 8a31bc625727594d42f94173768bee5cf8afd0a4

Summary: XSP built for Mono
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Productivity/Networking/Web/Utilities
Requires: pkgconfig mono-opt mono-opt-devel
BuildRequires: gcc libtool bison gettext make bzip2 autoconf automake libtool gcc-c++ patch mono-opt mono-opt-devel pkgconfig sqlite which
BuildRoot: /tmp/buildroot
Source: %{XSPGitReference}.tar.gz

%description
XSP built for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup -q -n xsp-%{XSPGitReference}

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
* Fri Jun 27 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- newer version from Github
* Fri Aug 02 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
