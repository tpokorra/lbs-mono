%define name gtk-sharp2-opt
%define version 2.12.26
%define MonoPath /opt/mono

Summary: gtk sharp for Mono
Name: %{name}
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: none
Requires: mono-opt >= 3.0 glib2 gtk2 libglade2
BuildRequires: gcc libtool gettext make automake gcc-c++ mono-opt >= 3.0 glib2-devel gtk2-devel libglade2-devel dos2unix
%if 0%{?suse_version}
BuildRequires: mono-opt-devel
%endif
BuildRoot: /tmp/buildroot
Source: gtk-sharp-%{version}.tar.gz

%description
Mono

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n gtk-sharp-%{version}

%build
# Configure and make source
export PKG_CONFIG_PATH=%{MonoPath}/lib/pkgconfig/:$PKG_CONFIG_PATH
export PATH=%{MonoPath}/bin:$PATH
./configure --prefix=%{MonoPath}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
for f in %{buildroot}%{MonoPath}/bin/gapi2*
do
  dos2unix $f
done
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
find %{buildroot} -iname "*.exe.so" -exec rm '{}' ';'

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%changelog
* Wed Nov 25 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- update to 2.12.26
* Wed Jul 17 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- initial version

