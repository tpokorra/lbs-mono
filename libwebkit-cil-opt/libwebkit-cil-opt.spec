%define name libwebkit-cil
%define version 0.3
# tarball based on ubuntu package
%define MonoPath /opt/mono

Summary: CLI binding for the WebKit library
Name: %{name}-opt
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: MIT
Group: Development/Tools
Source0: webkit-sharp-0.3.tar.bz2
BuildRequires: gcc libtool make bzip2 gcc-c++ patch mono-opt pkgconfig intltool gtk-sharp2-opt gnome-sharp2-opt
Requires: mono-opt >= 3.2 gnome-sharp2-opt
%if 0%{?suse_version}
BuildRequires: mono-opt-devel
BuildRequires: libwebkitgtk-devel
Requires: libwebkitgtk-1_0-0
Patch0: libwebkitgtk.patch
%else
%if 0%{?centos_version} == 700
Patch0: centos7.patch
BuildRequires: webkitgtk3-devel
Requires: webkitgtk3
%else
BuildRequires: webkitgtk-devel
Requires: webkitgtk
%endif
%endif

%description
WebKit is a web content engine, derived from KHTML and KJS from KDE, and
used primarily in Apple's Safari browser.  It is made to be embedded in
other applications, such as mail readers, or web browsers.
.
This package provides the webkit-sharp assembly that allows CLI programs to
use WebKit library.

%prep
%setup -q -n webkit-sharp-%{version}
%if 0%{?suse_version}
%patch0 -p1
%endif
%if 0%{?centos_version} == 700
%patch0 -p1
%endif

%build
. %{MonoPath}/env.sh
CSC=%{MonoPath}/bin/mcs ./configure --prefix=%{MonoPath}

%install
. %{MonoPath}/env.sh
make DESTDIR=%{buildroot} install

%post

%postun

%files
%{MonoPath}

%changelog
* Thu Dec 19 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
