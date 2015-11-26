%global libname Newtonsoft.Json

# mono is without any packagable debuginfo
%global debug_package %{nil}

%bcond_with tests
%define publicname newtonsoft-json
%define _monodir /opt/mono
%define _monogacdir %{_monodir}/lib/mono/gac
Name:           %{publicname}-opt
Version:        7.0.1
Release:        1%{?dist}
Summary:        Popular high-performance JSON framework

# almost all files are licensed as MIT/X11, but BSD for LinqBridge.cs
# (and LGPLv2.1+ for Tools/7-Zip, not used)
License:        MIT and BSD
URL:            http://www.newtonsoft.com/json
Source0:        https://github.com/JamesNK/%{libname}/archive/%{version}.tar.gz#/%{publicname}-%{version}.tar.gz
Patch0:         %{publicname}-sign.patch
Patch1:         %{publicname}-tests-skip-samples.patch

#ExclusiveArch:  %{mono_arches}
BuildRequires:  mono-opt
BuildRequires:  nunit-opt

%description
%{libname} aka Json.NET is a popular high-performance JSON framework


%prep
%setup -qn%{libname}-%{version}
# E: wrong-script-interpreter
rm README.md
# sign the assembly to get a strong name, https://msdn.microsoft.com/en-us/library/xc31ft41.aspx
%patch0
. /opt/mono/env.sh
sn -k myKey.snk
# http://www.sturmnet.org/blog/2005/05/10/internalsvisibleto-sn
#sn -p myKey.snk myKey.pub
#token=`sn -tp myKey.pub |grep Token |sed -r 's,.*: (.*),\1,'`
#sed -i 's,PublicKey=.*",PublicKeyToken='${token}'",g' Src/%{libname}/Properties/AssemblyInfo.cs
#key=`sn -tp myKey.pub |tr -d '\n' |sed -r 's,.*Key:(.*)P.*,\1,'`
#sed -i -r 's,(PublicKey=).*",\1'${key}'",g' Src/%{libname}/Properties/AssemblyInfo.cs
sed -i /InternalsVisibleTo/d Src/%{libname}/Properties/AssemblyInfo.cs
%if %{with tests}
# skip files with unmet dependencies (FSharp etc.), FIXME use nuget
%patch1
sed -i /DiscriminatedUnionConverterTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Serialization.DependencyInjectionTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Serialization.FSharpTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Serialization.ImmutableCollectionsTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /TestObjects.Currency.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /TestObjects.Shape.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Schema.JsonSchemaBuilderTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Schema.JsonSchemaNodeTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
sed -i /Utilities.StringUtilsTests.cs/d Src/%{libname}.Tests/%{libname}.Tests.csproj
%endif


%build
. /opt/mono/env.sh
pushd Src/%{libname}
xbuild %{libname}.csproj


%install
. /opt/mono/env.sh
mkdir -p %{buildroot}/%{_monogacdir}
gacutil -i Src/%{libname}/bin/Debug/Net45/%{libname}.dll -f -package %{publicname} -root %{buildroot}/opt/mono/lib
# pkgconfig
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
cat <<EOT >>%{buildroot}/%{_libdir}/pkgconfig/%{name}.pc
Name: %{libname}
Description: %{summary}
Version: %{version}
Requires: 
Libs: -r:%{_monodir}/%{name}/%{libname}.dll
Libraries=%{_monodir}/%{name}/%{libname}.dll
EOT


%check
%if %{with tests}
pushd Src/%{libname}.Tests
# FIXME unmet dependencies prevent many tests (Linq, Utilities etc.)
xbuild %{libname}.Tests.csproj
nunit-console26 -labels -stoponerror bin\Debug\Net45\*.dll
#rm -r obj bin
%endif


%files
%doc Doc/license.txt
%doc *.md Doc/readme.txt
%{_monogacdir}/%{libname}
%{_monodir}/lib/mono/%{publicname}/%{libname}.dll
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Nov 26 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 7.0.1-2
- build for mono-opt
* Fri Oct 09 2015 Raphael Groner <projects.rg@smart.ms> - 7.0.1-1
- initial
