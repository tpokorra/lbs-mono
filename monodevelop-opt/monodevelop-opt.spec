%define name monodevelop-opt
%define version 5.10.0
%define tarballpath 5.10
%define fileversion 5.10.0.871
%define MonoPath /opt/mono
%define MonoDevelopPath /opt/monodevelop

Summary: MonoDevelop
Name: %{name}
Version: %{version}
Release: 4 
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: none
BuildRequires: automake autoconf libtool mono-opt >= 3.12 libgdiplus pkgconfig shared-mime-info intltool gtk-sharp2-opt gnome-sharp2-opt nuget-opt
BuildRequires: nunit-opt >= 2.6.3 nunit-opt-devel
BuildRequires: cmake git
BuildRequires: libssh2-devel
BuildRequires: newtonsoft-json-opt
Requires: mono-opt >= 4.2 libgdiplus pkgconfig gnome-sharp2-opt gtk-sharp2-opt mono-libgdiplus-opt mono-tools-opt
BuildRoot: /tmp/buildroot
Source: monodevelop-%{fileversion}.tar.bz2
Patch:  downgrade_to_mvc3.patch
Patch1: monodevelop-5.10-no_nuget_packages.patch

%description
MonoDevelop

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n monodevelop-%{tarballpath}
%patch -p1
%patch1 -p1

%build
# Configure and make source
. %{MonoPath}/env.sh
for f in tests/TestRunner/TestRunner.csproj tests/UserInterfaceTests/UserInterfaceTests.csproj src/addins/NUnit/NUnitRunner/NUnitRunner.csproj src/addins/NUnit/MonoDevelop.NUnit.csproj external/nrefactory/ICSharpCode.NRefactory.Tests/ICSharpCode.NRefactory.Tests.csproj
do 
  echo $f
  sed -i "s#<HintPath>.*nunit\.#<HintPath>/opt/mono/lib/mono/nunit/nunit.#g" $f
done
for f in tests/UserInterfaceTests/UserInterfaceTests.csproj
do
  sed -i "s#<HintPath>.*Newtonsoft\.Json\.dll#<HintPath>/opt/mono/lib/mono/newtonsoft-json/Newtonsoft.Json.dll#g" $f
done
%configure --prefix=%{MonoDevelopPath} --libdir=/opt/mono/lib --disable-update-mimedb
cd ./external/libgit2sharp/Lib/CustomBuildTasks
xbuild CustomBuildTasks.csproj
mv bin/Debug/* .
cd ../../../../
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
find %{buildroot} -iname "*.dll.so" -exec rm '{}' ';'
mkdir -p %{buildroot}/usr/share/icons
mkdir -p %{buildroot}/usr/share/applications
mv %{buildroot}/usr/share/applications/monodevelop.desktop %{buildroot}/usr/share/applications/monodevelop-opt.desktop
mv %{buildroot}/usr/share/icons/hicolor/16x16/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/16x16/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/22x22/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/22x22/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/24x24/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/24x24/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/32x32/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/32x32/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/48x48/apps/monodevelop.png %{buildroot}/usr/share/icons/hicolor/48x48/apps/monodevelop-opt.png
mv %{buildroot}/usr/share/icons/hicolor/scalable/apps/monodevelop.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/monodevelop-opt.svg
sed -i 's/Exec=monodevelop/Exec=monodevelop-opt/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
sed -i 's/Name=MonoDevelop/Name=MonoDevelop %{version}/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
sed -i 's/Icon=monodevelop/Icon=monodevelop-opt/g' %{buildroot}/usr/share/applications/monodevelop-opt.desktop
mkdir -p %{buildroot}/usr/bin
echo ". /opt/mono/env.sh; exec /opt/monodevelop/bin/monodevelop \"$@\"" > %{buildroot}/usr/bin/monodevelop-opt
echo ". /opt/mono/env.sh; MONO_EXEC=\"exec -a mdtool mono-sgen\"; EXE_PATH=\"/opt/monodevelop/lib/monodevelop/bin/mdtool.exe\"; $MONO_EXEC $MONO_OPTIONS \"$EXE_PATH\" \"$@\"" > %{buildroot}/usr/bin/mdtool-opt
chmod a+x %{buildroot}/usr/bin/monodevelop-opt
chmod a+x %{buildroot}/usr/bin/mdtool-opt
rm %{buildroot}/usr/bin/monodevelop
rm %{buildroot}/usr/bin/mdtool

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoDevelopPath}
/usr/bin/monodevelop-opt
/usr/bin/mdtool-opt
/usr/share/applications/monodevelop-opt.desktop
/usr/share/icons/hicolor/16x16/apps/monodevelop-opt.png
/usr/share/icons/hicolor/22x22/apps/monodevelop-opt.png
/usr/share/icons/hicolor/24x24/apps/monodevelop-opt.png
/usr/share/icons/hicolor/32x32/apps/monodevelop-opt.png
/usr/share/icons/hicolor/48x48/apps/monodevelop-opt.png
/usr/share/icons/hicolor/scalable/apps/monodevelop-opt.svg
/usr/share/man/man1/mdtool.1.gz
/usr/share/man/man1/monodevelop.1.gz
/usr/share/mime/packages/monodevelop.xml

%changelog
* Wed Nov 25 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 5.10.0-4
- build 5.10.0.871
* Thu Oct 08 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 5.9.6.23
* Thu Apr 23 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 5.9
* Sat May 31 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build 5.0.0
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

