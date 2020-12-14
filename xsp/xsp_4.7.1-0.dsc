Hash: SHA512

Format: 3.0 (quilt)
Source: xsp
Binary: dh-xsp, mono-xsp4-base, mono-xsp4, mono-xsp, asp.net-examples, mono-apache-server4, mono-apache-server, mono-fpm-server, libfpm-helper0, mono-fastcgi-server4, mono-fastcgi-server
Architecture: any all
Version: 4.7.1-0
Maintainer: Debian Mono Group <pkg-mono-group@lists.alioth.debian.org>
Uploaders: Dylan R. E. Moonfire <debian@mfgames.com>, Mirco Bauer <meebey@debian.org>, Jo Shields <directhex@apebox.org>
Homepage: http://www.mono-project.com/ASP.NET
Standards-Version: 3.9.1
Vcs-Browser: http://git.debian.org/?p=pkg-mono/packages/xsp.git
Vcs-Git: git://git.debian.org/git/pkg-mono/packages/xsp.git
Build-Depends: debhelper (>= 7.0.50~), po-debconf, autotools-dev, cli-common-dev (>= 0.8~), mono-devel (>= 3), monodoc-base (>= 3), libnunit-cil-dev
Package-List:
 asp.net-examples deb web optional arch=all
 dh-xsp deb web optional arch=all
 libfpm-helper0 deb web optional arch=any
 mono-apache-server deb web optional arch=all
 mono-apache-server4 deb web optional arch=all
 mono-fastcgi-server deb web optional arch=all
 mono-fastcgi-server4 deb web optional arch=all
 mono-fpm-server deb web optional arch=all
 mono-xsp deb web optional arch=all
 mono-xsp4 deb web optional arch=all
 mono-xsp4-base deb web optional arch=all
Files:
 abc 1 xsp-4.7.1.tar.gz
 abc 1 xsp_4.7.1-0.debian.tar.xz
