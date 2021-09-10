#!/bin/bash
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $SCRIPT_PATH
export MONO_PATH=$SCRIPT_PATH/usr/
export MONO_GAC_PREFIX=$SCRIPT_PATH/usr/
export PATH=$SCRIPT_PATH/usr/bin:$PATH

if [ -w "$MONO_PATH/bin/fastcgi-mono-server4" ]
then
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/fastcgi-mono-server4
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/xsp4
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/mcs
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/csharp
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/cert-sync
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/certmgr
  sed "s#/usr/#\$MONO_PATH/#g" -i $MONO_PATH/bin/mozroots
fi
