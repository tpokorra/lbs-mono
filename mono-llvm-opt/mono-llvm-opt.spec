%define name mono-llvm-opt
%define version 4.2.1
%define MonoPath /opt/mono
%define GITREVISION 38603e0a3d6448b0b9edeb1a06ea78501515cec8

Summary: Mono LLVM
Name: %{name}
Version: %{version}
Release: 5
Url: http://www.mono-project.com/docs/advanced/mono-llvm/
License: NCSA
Group: Development/Languages/Mono
BuildRequires: bison gettext make bzip2 automake patch dos2unix libgdiplus python
%if 0%{?rhel} < 6
BuildRequires: python26
%else
BuildRequires: python >= 2.5
%endif
%if 0%{?rhel} < 7
# need newer gcc version
BuildRequires: devtoolset-2-gcc >= 4.7 devtoolset-2-gcc-c++ devtoolset-2-binutils
%else
BuildRequires: gcc >= 4.7 gcc-c++ libtool
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
# need to use python26
%define PYTHON --with-python=/usr/bin/python26
%endif

# Configure and make source
./configure --prefix=%{MonoPath} --enable-optimized --enable-targets=host %{PYTHON}
make

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
* Tue Nov 24 2015 Timotheus Pokorra <timotheus.pokorra@solidcharity.com> - 4.2.1-5
- update to latest Mono LLVM from Github, required for Mono 4.2
* Thu Aug 14 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono LLVM 3.6.99

