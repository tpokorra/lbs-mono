%define name mod_mono-opt
%define version 3.12
%define MonoPath /opt/mono

Summary: mod_mono built for Mono
Name: %{name}
Version: %{version}
Release: 1
Packager: Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
Group: Productivity/Networking/Web/Utilities
License: GPL
Requires: pkgconfig mono-opt mono-xsp-opt
BuildRequires: gcc libtool bison gettext make bzip2 automake libtool gcc-c++ patch mono-opt
%if 0%{?suse_version}
BuildRequires: apache2-devel, pkg-config
Requires: apache2
%else
BuildRequires: httpd-devel
Requires: httpd
%endif
BuildRoot: /tmp/buildroot
Source: mod_mono-%{version}.tar.gz

%description
mod_mono built for Mono

%prep
[ -d $RPM_BUILD_ROOT ] && [ "/" != "$RPM_BUILD_ROOT" ] && rm -rf $RPM_BUILD_ROOT
%setup -q -n mod_mono-%{version}

%build
# Configure and make source
. /opt/mono/env.sh
./configure --prefix=%{MonoPath} --disable-docs
make

%install
rm -rf %{buildroot}
. /opt/mono/env.sh
make DESTDIR=%{buildroot} install

%clean
# Clean up after ourselves, but be careful in case someone sets a bad buildroot
[ -d %{buildroot} ] && [ "/" != "%{buildroot}" ] && rm -rf %{buildroot}

%files
%{MonoPath}
%if 0%{?suse_version}
/etc/apache2/mod_mono.conf
/usr/%{_lib}/apache2/mod_mono.so
/usr/%{_lib}/apache2/mod_mono.so.0.0.0
%else
/etc/httpd/conf/mod_mono.conf
/usr/%{_lib}/httpd/modules/mod_mono.so
/usr/%{_lib}/httpd/modules/mod_mono.so.0.0.0
%endif

%post
%if 0%{?suse_version}
echo "MonoServerPath %{MonoPath}/bin/mod-mono-server4" >> /etc/apache2/conf.d/mod_mono.conf
echo "include /etc/apache2/conf.d/mod_mono.conf" >> /etc/apache2/httpd.conf
%else
echo "MonoServerPath %{MonoPath}/bin/mod-mono-server4" >> /etc/httpd/conf/mod_mono.conf
echo "include /etc/httpd/conf/mod_mono.conf" >> /etc/httpd/conf/httpd.conf
%endif

%changelog
* Tue Nov 19 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- fixes for OpenSUSE
* Sat Jul 13 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- build for distributions with newer Apache
* Sat May 25 2013 Timotheus Pokorra <timotheus.pokorra@solidcharity.com>
- First build
