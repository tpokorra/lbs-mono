#!/bin/bash

# for CentOS5, we need to install the required packages manually
if [ ! -z "`cat /etc/redhat-release | grep 'CentOS release 5'`" ]
then
  yum -y install gcc libtool gettext make bzip2 automake gcc-c++ pkgconfig freetype-devel glib2-devel libjpeg-devel libtiff-devel libungif-devel libpng-devel fontconfig-devel cairo-devel giflib-devel libexif-devel zlib-devel libXrender-devel fontconfig-devel
fi
