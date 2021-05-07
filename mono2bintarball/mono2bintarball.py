#!/usr/bin/python3

import os
import shutil
from pathlib import Path

# pkgs_cur.txt is the output of: dpkg-query -f '${Package}\n' -W
# as it has been executed on the destination server
f = open("pkgs_target.txt", "r")
dstPackages = []
for line in f:
  dstPackages.append(line.strip())

stream = os.popen("mono --version | head -1 | awk '{print $5}'")
mono_version = stream.read().strip()
outpath=('%s/mono-%s' % (Path.home(),mono_version,))

if os.path.exists(outpath):
    print("please delete the output path first")
    exit()

# pkgs_mono.txt is from apt install, section: "The following NEW packages will be installed"
# when installing: apt install mono-xsp4 mono-fastcgi-server4 ca-certificates-mono
f = open("pkgs_mono.txt", "r")
for line in f:
  for pkgName in line.split():
    if pkgName in dstPackages:
        continue
    print(pkgName)
    stream = os.popen('dpkg -L %s' % (pkgName,))
    output = stream.read().split('\n')
    for installedfile in output:
      directory = outpath + os.path.dirname(installedfile)
      if not os.path.exists(directory):
        os.makedirs(directory)
      if os.path.islink(installedfile):
        shutil.copy2(installedfile, directory, follow_symlinks=False)   
      elif os.path.isfile(installedfile): 
        print('  ' + installedfile)
        shutil.copy2(installedfile, directory)

# copy aot cache as well
os.system("cp -R /usr/lib/mono %s/usr/lib" % (outpath,))

# copy config files as well
os.system("mkdir -p %s/usr/etc/ && cp -R /etc/mono/ %s/usr/etc/" % (outpath,outpath,))

tarfile=("%s/%s/mono-%s.bin.tar.gz" % (Path.home(),"tarball",mono_version,))
os.system("tar -C %s -czf %s %s" % (os.path.dirname(outpath),tarfile,os.path.basename(outpath)))
os.popen("ln -s %s %s/mono" % (outpath,Path.home(),))
print("see result in " + tarfile)

