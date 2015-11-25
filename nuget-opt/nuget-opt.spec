#
# spec file for package nuget
#
# Copyright (c) 2014 Xamarin, Inc (http://www.xamarin.com)
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%define tarballversion 2.8.7+md510+dhx1
%define MonoPath /opt/mono/

Name:           nuget-opt
Version:        2.8.7
Release:        2
Summary:        Package manager for NuGet repositories
License:        MIT
Group:          Development/Libraries/Other
Url:            http://nuget.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        nuget_%{tarballversion}.orig.tar.bz2
Source1:	nuget-core.pc
Source2:	nuget.sh
Source3:	nuget-build-minimal.sh
Patch0:		nuget-fix_xdt_hintpath.patch
BuildRequires:  mono-opt
%if 0%{?suse_version}
BuildRequires:  mono-opt-devel
%endif
BuildArch:      noarch

%description
NuGet is the package manager for the Microsoft
development platform including .NET. The NuGet client
tools provide the ability to produce and consume
packages. The NuGet Gallery is the central package
repository used by all package authors and consumers.

%prep
%setup -n nuget-git
sed -i "s/\r//g" src/Core/Core.csproj
%patch0 -p1

# fix compile with Mono4
find . -name "*.sln" -print -exec sed -i 's/Format Version 10.00/Format Version 11.00/g' {} \;
find . -name "*.csproj" -print -exec sed -i 's#ToolsVersion="3.5"#ToolsVersion="4.0"#g; s#<TargetFrameworkVersion>.*</TargetFrameworkVersion>##g; s#<PropertyGroup>#<PropertyGroup><TargetFrameworkVersion>v4.5</TargetFrameworkVersion>#g' {} \;

%build
. %{MonoPath}/env.sh
%{?exp_env}
%{?env_options}
chmod a+x %{SOURCE3}
%{SOURCE3}

%install
%{?env_options}
%{__mkdir_p} %{buildroot}%{MonoPath}/lib/nuget
%{__mkdir_p} %{buildroot}%{MonoPath}/lib/pkgconfig
%{__mkdir_p} %{buildroot}%{MonoPath}/bin
%{__install} -m0644 %{SOURCE1} %{buildroot}%{MonoPath}/lib/pkgconfig/
%{__install} -m0755 %{SOURCE2} %{buildroot}%{MonoPath}/bin/nuget
sed -i -e 's/cli/mono/' %{buildroot}%{MonoPath}/bin/*
%{__install} -m0755 src/CommandLine/bin/Release/NuGet.Core.dll %{buildroot}%{MonoPath}/lib/nuget/
%{__install} -m0755 xdt/XmlTransform/bin/Debug/Microsoft.Web.XmlTransform.dll %{buildroot}%{MonoPath}/lib/nuget/
%{__install} -m0755 src/CommandLine/bin/Release/NuGet.exe %{buildroot}%{MonoPath}/lib/nuget/

%files
%defattr(-,root,root)
%{MonoPath}/lib/nuget
%{MonoPath}/lib/pkgconfig/nuget-core.pc
%{MonoPath}/bin/*

%changelog
* Wed Nov 25 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.7-2
- new release 2.8.7

* Thu Apr 23 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-2
- build with mono-opt

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-1
- build with Mono4

* Thu Apr 16 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 2.8.3-0
- copy from Xamarin nuget spec
