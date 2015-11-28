%define name mono-xsp-opt
%define version 4.2
%define MonoPath /opt/mono
%define XSPGitReference e272a2c006211b6b03be2ef5bbb9e3f8fefd0768

Summary: XSP built for Mono
Name: %{name}
Version: %{version}
Release: 2
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Productivity/Networking/Web/Utilities
Requires: pkgconfig mono-opt mono-opt
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: bison
BuildRequires: gettext
BuildRequires: make
BuildRequires: bzip2
BuildRequires: autoconf >= 2.63
BuildRequires: automake >= 1.11
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: patch
BuildRequires: mono-opt
BuildRequires: pkgconfig
BuildRequires: sqlite >= 3.5
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
* Sat Nov 28 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.2-2
- newer version from Github
* Fri Jun 27 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- newer version from Github
* Fri Aug 02 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
