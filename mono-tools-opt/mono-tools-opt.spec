%define name mono-tools
%define version 3.10
%define MonoPath /opt/mono

Summary: A collection of tools for mono applications
Name: %{name}-opt
Version: %{version}
Release: 4.7
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: MIT
Group: Development/Tools
Source0: mono-tools-%{version}.tar.gz
Patch0: webdocfiles.patch
Patch1: docbrowser.patch
URL: http://www.mono-project.com/Main_Page
BuildRequires: gcc libtool bison gettext make bzip2 autoconf automake libtool gcc-c++ patch mono-opt pkgconfig sqlite libgdiplus shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt mono-libgdiplus-opt zip libwebkit-cil-opt nunit-opt nunit-opt-devel
%if 0%{?suse_version}
BuildRequires: mono-opt-devel
%endif
Requires: mono-opt >= 3.2 mono-libgdiplus-opt gnome-sharp2-opt libwebkit-cil-opt
%if 0%{?suse_version}
BuildRequires: libwebkitgtk-devel
%else
%if 0%{?centos_version} == 700
BuildRequires: webkitgtk3-devel
%else
BuildRequires: webkitgtk-devel
%endif
%endif

%description
Monotools are a number of tools for mono such as allowing monodoc to be run
independantly of monodevelop

%prep
%setup -q -n mono-tools-%{version}
%patch0 -p1
#%patch1 -p1
chmod 644 COPYING

%build
. %{MonoPath}/env.sh
sed -i "s#gmcs#mcs#g" configure
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;
%configure --libdir=%{MonoPath}/lib --prefix=%{MonoPath}
make 
# no smp flags - breaks the build

%install
. %{MonoPath}/env.sh
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{MonoPath}/bin
mv %{buildroot}/usr/bin/* %{buildroot}%{MonoPath}/bin
# TODO: could rename the .desktop files, locale files, man pages.
# but for the moment, we rather delete them than to have a conflict with other packages
rm -f %{buildroot}/usr/share/applications/gendarme-wizard.desktop
rm -f %{buildroot}/usr/share/applications/gsharp.desktop
rm -f %{buildroot}/usr/share/applications/monodoc.desktop
rm -f %{buildroot}/usr/share/icons/hicolor/16x16/apps/monodoc.png
rm -f %{buildroot}/usr/share/icons/hicolor/22x22/apps/monodoc.png
rm -f %{buildroot}/usr/share/icons/hicolor/24x24/apps/monodoc.png
rm -f %{buildroot}/usr/share/icons/hicolor/256x256/apps/monodoc.png
rm -f %{buildroot}/usr/share/icons/hicolor/32x32/apps/monodoc.png
rm -f %{buildroot}/usr/share/icons/hicolor/48x48/apps/monodoc.png
rm -f %{buildroot}/usr/share/locale/ca/LC_MESSAGES/mono-tools.mo
rm -f %{buildroot}/usr/share/locale/da/LC_MESSAGES/mono-tools.mo
rm -f %{buildroot}/usr/share/locale/es/LC_MESSAGES/mono-tools.mo
rm -f %{buildroot}/usr/share/locale/fr/LC_MESSAGES/mono-tools.mo
rm -f %{buildroot}/usr/share/locale/pt_BR/LC_MESSAGES/mono-tools.mo
rm -f %{buildroot}/usr/share/man/man1/create-native-map.1.gz
rm -f %{buildroot}/usr/share/man/man1/gd2i.1.gz
rm -f %{buildroot}/usr/share/man/man1/gendarme.1.gz
rm -f %{buildroot}/usr/share/man/man1/mperfmon.1.gz
rm -f %{buildroot}/usr/share/man/man1/mprof-decoder.1.gz
rm -f %{buildroot}/usr/share/man/man1/mprof-heap-viewer.1.gz
rm -f %{buildroot}/usr/share/man/man5/gendarme.5.gz
rm -f %{buildroot}/usr/share/pixmaps/gendarme.svg
rm -f %{buildroot}/usr/share/pixmaps/monodoc.png

rm -Rf %{buildroot}/usr/share/

%post

%postun

%files
%{MonoPath}

%changelog
* Sat May 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- version 3.10
* Thu Dec 05 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build, looseley based on https://apps.fedoraproject.org/packages/mono-tools-monodoc/sources/spec
