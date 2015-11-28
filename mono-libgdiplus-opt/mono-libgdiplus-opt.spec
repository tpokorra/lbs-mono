%define name mono-libgdiplus-opt
%define version 4.2
%define MonoPath /opt/mono

Summary: links for libgdiplus for Mono
Name: %{name}
Version: %{version}
Release: 3 
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development
Requires: pkgconfig mono-opt libgdiplus
%if 0%{?suse_version}
Requires: liberation-fonts
%else
Requires: liberation-mono-fonts
%endif

BuildRequires: mono-opt libgdiplus
BuildRoot: /tmp/buildroot

%description
links for libgdiplus for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{MonoPath}/lib/
f=`find /usr -name libgdiplus.so.0`
if [ -f $f ]
then
  ln -sf ../../..$f $RPM_BUILD_ROOT/%{MonoPath}/lib/libgdiplus.so
fi

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}/lib/libgdiplus.so

%post

%changelog
* Tue Nov 19 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- OpenSUSE has a different name for liberation-mono-fonts
* Thu Jul 11 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
