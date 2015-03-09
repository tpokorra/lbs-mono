#!/bin/bash

# for CentOS5, we need to install the required packages manually
if [ ! -z "`cat /etc/redhat-release | grep 'CentOS release 5'`" ]
then
  yum -y install sed m4 emacs
fi
