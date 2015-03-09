%define name mono-llvm-opt
%define version 3.6.99
%define MonoPath /opt/mono
%define GITREVISION e656caccc7dfb5c51c208906f0e176f0973f030f

Summary: Mono LLVM
Name: %{name}
Version: %{version}
Release: %{release}
Url: http://www.mono-project.com/docs/advanced/mono-llvm/
License: NCSA
Group: Development/Languages/Mono
BuildRequires: gcc libtool bison gettext make bzip2 automake gcc-c++ patch dos2unix libgdiplus python
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
# Configure and make source
./configure --prefix=%{MonoPath} --enable-optimized --enable-targets=host
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
* Thu Aug 14 2014 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- Building Mono LLVM 3.6.99
