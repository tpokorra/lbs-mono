%define name mono-llvm-opt
%define version 3.6.99
%define MonoPath /opt/mono

Summary: Mono LLVM
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
License: GPL
Group: Development/Languages/Mono
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch dos2unix libgdiplus
BuildRoot: /tmp/buildroot
Source: mono-llvm.tar.bz2

%description
Mono LLVM

%prep
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}
%setup -q -n mono-llvm

%build
# Configure and make source
./configure --prefix=%{MonoPath}
make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{MonoPath}

%changelog
* Thu Aug 14 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono LLVM
