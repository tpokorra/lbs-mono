%define name libgdiplus
%define version 2.10.9

Summary: libgdiplus
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
Group: None
License: GPL
BuildRequires: gcc libtool gettext make bzip2 automake gcc-c++ pkgconfig
BuildRequires:  freetype-devel glib2-devel libjpeg-devel libtiff-devel
BuildRequires:  libungif-devel libpng-devel fontconfig-devel
BuildRequires:  cairo-devel giflib-devel libexif-devel
BuildRequires:  zlib-devel
BuildRequires: libXrender-devel fontconfig-devel

Source: libgdiplus-%{version}.tar.bz2
# Patch for linking against libpng 1.5 (BZ #843330)
# https://github.com/mono/libgdiplus/commit/506df13e6e1c9915c248305e47f0b67549732566
Patch0:         libgdiplus-2.10.9-libpng15.patch
# https://github.com/mono/libgdiplus/commit/1fa831c7440f1985d2b730211bbf8a059c10a63b
Patch1:         libgdiplus-2.10.9-tests.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-root

%description
libgdiplus

%prep
%setup -q -n libgdiplus-%{version}
%patch0 -p1 -b .libpng15
%patch1 -p1 -b .tests

%build
./configure --disable-static

%if 0%{?rhel} < 6
# fix for CentOS5: see http://stackoverflow.com/a/17526455/1632368 to avoid: X--tag=CC: command not found
mv pixman/libtool pixman/libtool.old
cp libtool pixman/libtool
%endif

make

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README TODO AUTHORS ChangeLog
/usr/local/lib/lib*.so*
/usr/local/lib/pkgconfig/libgdiplus.pc

%post

%changelog
* Sat Jun 22 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- initial build

