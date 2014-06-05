%define name automake
%define version 1.13
%define api_version 1.13

Summary: automake
Name: %{name}
Version: %{version}
Release: 99
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
Group: None
License: GPL
Requires: perl, autoconf >= 2.69
BuildRequires: autoconf >= 2.69
Buildrequires:  bison
Source: automake-%{version}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
autoconf

%prep
%setup -q -n automake-%{version}

%build
./configure --prefix=%{_prefix}
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall
rm -Rf  ${RPM_BUILD_ROOT}/usr/share/aclocal
rm -Rf  ${RPM_BUILD_ROOT}/usr/share/doc/automake
rm -Rf  ${RPM_BUILD_ROOT}/usr/share/man/man1/aclocal*
rm -Rf  ${RPM_BUILD_ROOT}/usr/share/man/man1/automake*
# we do not want a dependancy on perl(TAP::Parser)
rm -f ${RPM_BUILD_ROOT}/usr/share/automake-1.13/tap-driver.pl
rm -f ${RPM_BUILD_ROOT}/usr/share/automake-1.13/tap-driver.sh
rm -f ${RPM_BUILD_ROOT}/usr/share/automake-1.13/test-driver

# create this dir empty so we can own it
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/aclocal
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc AUTHORS README THANKS NEWS
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%dir %{_datadir}/aclocal

%post

%changelog
* Thu May 30 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- based on CentOS srpm
