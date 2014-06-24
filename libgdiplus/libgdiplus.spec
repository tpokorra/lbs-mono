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
Buildroot:      %{_tmppath}/%{name}-%{version}-root

%description
libgdiplus

%prep
%setup -q -n libgdiplus-%{version}

%build
./configure --disable-static
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
