%define name sqlite
%define version 3.7.17
%define versionpath sqlite-autoconf-3071700

Summary: sqlite
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
Group: None
License: GPL
BuildRequires: ncurses-devel readline-devel gcc
#BuildRequires: /usr/bin/tclsh
Source: %{versionpath}.tar.gz
Buildroot: %{_tmppath}/%{name}-%{version}-root

%description
Sqlite built for OpenPetra standalone

%prep
%setup -q -n %{versionpath}

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
CPPFLAGS="-D SQLITE_ENABLE_COLUMN_METADATA"
%configure --disable-tcl \
           --enable-threadsafe \
           --enable-threads-override-locks
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=${RPM_BUILD_ROOT} install

%{__install} -D -m0644 sqlite3.1 %{buildroot}%{_mandir}/man1/sqlite3.1

rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}
rm -f $RPM_BUILD_ROOT/usr/include/sqlite3.h
rm -f $RPM_BUILD_ROOT/usr/include/sqlite3ext.h
rm -Rf $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu May 30 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- based on CentOS srpm

