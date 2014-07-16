%define name monodevelop-nightly
%define version 0.1
%define fileversion 0.1
%define MonoPath /opt/mono
%define MonoDevelopPath /opt/monodevelop

Summary: MonoDevelop
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: none
BuildRequires: automake autoconf libtool mono-opt-nightly >= 3.0 mono-opt-nightly-devel libgdiplus pkgconfig shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt
Requires: mono-opt >= 3.0 mono-opt-devel libgdiplus pkgconfig gnome-sharp2-opt gtk-sharp2-opt mono-libgdiplus-opt mono-tools-opt
BuildRoot: /tmp/buildroot
Source: monodevelop-%{fileversion}.tar.bz2

%description
MonoDevelop

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n monodevelop-%{fileversion}

%build
# Configure and make source
. %{MonoPath}/env.sh
./configure --prefix=%{MonoDevelopPath}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# make && make install overwrites the buildinfo (https://github.com/mono/monodevelop/blob/master/main/src/core/MonoDevelop.Core/MonoDevelop.Core.csproj#L577)
# so we use the buildinfo that comes with the tarball
cp -f buildinfo %{buildroot}/%{MonoDevelopPath}/lib/monodevelop/bin/
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
mkdir -p %{buildroot}/usr/share/icons
mkdir -p %{buildroot}/usr/share/applications
cp -R %{buildroot}/%{MonoDevelopPath}/share/applications/monodevelop.desktop %{buildroot}/usr/share/applications/monodevelop-opt.desktop
cp -R %{buildroot}/%{MonoDevelopPath}/share/icons/* %{buildroot}/usr/share/icons
mv %{buildroot}/usr/share/icons/hicolor/16x16/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/16x16/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/22x22/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/22x22/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/24x24/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/24x24/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/32x32/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/32x32/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/48x48/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/scalable/apps/monodevelop.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/monodevelop-opt.svg
sed -i 's/Exec=monodevelop/Exec=monodevelop-opt/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
sed -i 's/Name=MonoDevelop/Name=MonoDevelop 4/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
sed -i 's/Icon=monodevelop/Icon=monodevelop-opt/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
mkdir -p %{buildroot}/usr/bin
echo "export PATH=/opt/mono/bin:$PATH;export LD_LIBRARY_PATH=/opt/mono/lib:$LD_LIBRARY_PATH; exec /opt/monodevelop/bin/monodevelop \"$@\"" > %{buildroot}/usr/bin/monodevelop-opt
chmod a+x %{buildroot}/usr/bin/monodevelop-opt

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoDevelopPath}
/usr/bin/monodevelop-opt
/usr/share/applications/monodevelop-opt.desktop
/usr/share/icons/hicolor/16x16/apps/monodevelop-opt.png
/usr/share/icons/hicolor/22x22/apps/monodevelop-opt.png
/usr/share/icons/hicolor/24x24/apps/monodevelop-opt.png
/usr/share/icons/hicolor/32x32/apps/monodevelop-opt.png
/usr/share/icons/hicolor/48x48/apps/monodevelop-opt.png
/usr/share/icons/hicolor/scalable/apps/monodevelop-opt.svg

%changelog
* Fri May 23 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.2.5
* Wed Apr 09 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- pass parameters to monodevelop, so that files are opened. fixes Bug 18879
* Mon Mar 03 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.2.3
* Thu Dec 19 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.2.2
* Sat Nov 16 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.2
* Fri Oct 25 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.0.13
* Mon Jul 29 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.0.12
* Mon Jul 29 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 4.0.10
* Wed Jul 17 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build

