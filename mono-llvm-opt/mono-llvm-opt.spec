%define name mono-llvm-opt
%define version 4.2.1
%define MonoPath /opt/mono
%define GITREVISION 38603e0a3d6448b0b9edeb1a06ea78501515cec8

Summary: Mono LLVM
Name: %{name}
Version: %{version}
Release: 2
Url: http://www.mono-project.com/docs/advanced/mono-llvm/
License: NCSA
Group: Development/Languages/Mono
BuildRequires: gcc >= 4.7
BuildRequires: libtool bison gettext make bzip2 automake gcc-c++ patch dos2unix libgdiplus python
%if 0%{?rhel} < 6
BuildRequires: python26
%else
BuildRequires: python >= 2.5
%endif
if 0%{?rhel} < 7
# need newer gcc version
BuildRequires: devtoolset-2
%endif

BuildRoot: /tmp/buildroot
Source: %{GITREVISION}.tar.gz

%description
Mono LLVM backend

%package devel
License:      NCSA
Group:        Development/Languages/Mono
Summary:      Development files for Mono LLVM
Requires:     %{name} = %{version}
%description devel
Development files for Mono LLVM backend

%prep
%setup -q -n llvm-%{GITREVISION}

%build

%if 0%{?rhel} < 7
# we need a newer gcc
PATH=/opt/rh/devtoolset-2/root/usr/bin:$PATH
CC=/opt/rh/devtoolset-2/root/usr/bin/gcc
CPP=/opt/rh/devtoolset-2/root/usr/bin/cpp
CXX=/opt/rh/devtoolset-2/root/usr/bin/c++
%endif

%if 0%{?rhel} < 6
# need to make python26 the default
mv /usr/bin/python /usr/bin/python25.bak
ln -s /usr/bin/python26 /usr/bin/python
%endif

# Configure and make source
./configure --prefix=%{MonoPath} --enable-optimized --enable-targets=host
make

%if 0%{?rhel} < 6
# need to restore python25 for rpm signing
rm -f /usr/bin/python
mv /usr/bin/python25.bak /usr/bin/python
%endif

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
chmod a-x %{buildroot}/opt/mono/lib/*.a

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%exclude %{MonoPath}/include
%exclude %{MonoPath}/lib/*.a
%exclude %{MonoPath}/lib/*.so
%{MonoPath}

%files devel
%defattr(-,root,root,-)
%{MonoPath}/include
%{MonoPath}/lib/*.so
%{MonoPath}/lib/*.a

%changelog
* Tue Nov 24 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.2.1-2
- update to latest Mono LLVM from Github, required for Mono 4.2
* Thu Aug 14 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono LLVM 3.6.99

