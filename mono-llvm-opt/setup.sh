#!/bin/bash

# for CentOS5, we need to install the required packages manually
if [ ! -z "`cat /etc/redhat-release | grep 'CentOS release 5'`" ]
then
  yum -y install gcc libtool bison gettext make bzip2 automake gcc-c++ patch dos2unix libgdiplus python26
fi
