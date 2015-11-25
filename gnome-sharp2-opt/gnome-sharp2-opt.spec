%define name gnome-sharp2-opt
%define version 2.24.2
%define MonoPath /opt/mono

Summary: gnome sharp for Mono
Name: %{name}
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: none
Requires: mono-opt >= 3.0 glib2 gtk2 libglade2 gtk-sharp2-opt libgnomecanvas libgnome libgnomeui
BuildRequires: gcc libtool gettext make automake gcc-c++ mono-opt >= 3.0 glib2-devel gtk2-devel libglade2-devel gtk-sharp2-opt libgnomecanvas-devel libgnome-devel libgnomeui-devel
%if 0%{?suse_version}
BuildRequires: mono-opt-devel
%endif
BuildRoot: /tmp/buildroot
Source: gnome-sharp-%{version}.tar.gz

%description
gnome sharp

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n gnome-sharp-%{version}

%build
# Configure and make source
export PKG_CONFIG_PATH=%{MonoPath}/lib/pkgconfig/:$PKG_CONFIG_PATH
export PATH=%{MonoPath}/bin:$PATH
./configure --prefix=%{MonoPath}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
find %{buildroot} -iname "*.exe.so" -exec rm '{}' ';'

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}

%changelog
* Thu Jul 18 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- initial version

