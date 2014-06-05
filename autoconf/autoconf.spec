%define name autoconf
%define version 2.69

Summary: autoconf
Name: %{name}
Version: %{version}
Release: 99
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
Group: None
License: GPL
Requires: gawk, m4, mktemp, perl, textutils, imake
BuildRequires: sed, m4, emacs
Source: autoconf-2.69.tar.gz
Buildroot:      %{_tmppath}/%{name}-%{version}-root

%description
autoconf

%prep
%setup -q -n autoconf-%{version}

%build
%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf
%{_datadir}/emacs/site-lisp
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO

%post

%changelog
* Thu May 30 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- based on CentOS srpm
