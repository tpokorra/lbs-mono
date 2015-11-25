%global debug_package %{nil}
%define MonoPath /opt/mono

Name:           nunit-opt
Version:        2.6.3
Release:        3
Summary:        Unit test framework for CLI
License:        MIT
Group:          Development/Libraries
Url:            http://www.nunit.org/
Source0:        nunit_%{version}+dfsg.orig.tar.gz
#Source0:        http://launchpad.net/nunitv2/trunk/%{version}/+download/NUnit-%{version}-src.zip
Source1:        nunit.pc
Source2:        nunit-gui.sh
Source3:        nunit-console.sh
BuildRequires:  libgdiplus mono-libgdiplus-opt
%if 0%{?suse_version}
BuildRequires:  mono-opt-devel
%endif

%description
NUnit is a unit testing framework for all .NET languages. It serves the
same purpose as JUnit does in the Java world. It supports test
categories, testing for exceptions and writing test results in plain
text or XML.
.
NUnit targets the CLI (Common Language Infrastructure) and supports Mono and
the Microsoft .NET Framework.

%package        devel
Summary:        Development files for NUnit
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
 
%description devel
Development files for %{name}.

%prep
%setup -qn NUnit-%{version}

%build

. %{MonoPath}/env.sh

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%{?exp_env}
%{?env_options}
xbuild /property:Configuration=Debug ./src/NUnitCore/core/nunit.core.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitCore/interfaces/nunit.core.interfaces.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitFramework/framework/nunit.framework.dll.csproj
xbuild /property:Configuration=Debug ./src/NUnitMocks/mocks/nunit.mocks.csproj
xbuild /property:Configuration=Debug ./src/ClientUtilities/util/nunit.util.dll.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console/nunit-console.csproj
xbuild /property:Configuration=Debug ./src/ConsoleRunner/nunit-console-exe/nunit-console.exe.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui/nunit-gui.csproj
xbuild /property:Configuration=Debug ./src/GuiComponents/UiKit/nunit.uikit.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiException/UiException/nunit.uiexception.dll.csproj
xbuild /property:Configuration=Debug ./src/GuiRunner/nunit-gui-exe/nunit-gui.exe.csproj

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{MonoPath}/lib/nunit
%{__mkdir_p} %{buildroot}%{MonoPath}/lib/pkgconfig
%{__mkdir_p} %{buildroot}%{MonoPath}/bin
%{__install} -m0644 %{SOURCE1} %{buildroot}%{MonoPath}/lib/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{MonoPath}/bin/`basename -s .sh %{SOURCE2}`-2.6
%{__install} -m0755 %{SOURCE3} %{buildroot}%{MonoPath}/bin/`basename -s .sh %{SOURCE3}`-2.6
sed -i -e 's/cli/mono/' %{buildroot}%{MonoPath}/bin/*
%{__install} -m0644 src/ConsoleRunner/nunit-console-exe/App.config %{buildroot}%{MonoPath}/lib/nunit/nunit-console.exe.config
%{__install} -m0644 src/GuiRunner/nunit-gui-exe/App.config %{buildroot}%{MonoPath}/lib/nunit/nunit.exe.config
find %{_builddir}/%{?buildsubdir} -name \*.dll -exec %{__install} \-m0755 "{}" "%{buildroot}%{MonoPath}/lib/nunit/" \;
find %{_builddir}/%{?buildsubdir} -name \*.exe -exec %{__install} \-m0755 "{}" "%{buildroot}%{MonoPath}/lib/nunit/" \;
. %{MonoPath}/env.sh
for i in nunit-console-runner.dll nunit.core.dll nunit.core.interfaces.dll nunit.framework.dll nunit.mocks.dll nunit.util.dll ; do
    gacutil -i %{buildroot}%{MonoPath}/lib/nunit/$i -package nunit -root %{buildroot}%{MonoPath}/lib
    rm -f %{buildroot}%{MonoPath}/lib/nunit/$i
done

%files
%defattr(-,root,root)
%{MonoPath}/lib/mono/gac/nunit*
%{MonoPath}/lib/mono/nunit
%{MonoPath}/lib/nunit
%{MonoPath}/bin

%files devel
%defattr(-,root,root,-)
%{MonoPath}/lib/pkgconfig/nunit.pc

%changelog
* Thu Apr 23 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-3
- build with mono-opt

* Tue Apr 21 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> - 2.6.3-2
- Split nunit.pc into devel package
- Use upstream zip source
- Add ExclusiveArch

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.6.3-0
- copy from Xamarin NUnit spec
