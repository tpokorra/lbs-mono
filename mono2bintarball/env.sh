#!/bin/bash
SCRIPT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export MONO_PATH=$SCRIPT_PATH/usr/
export MONO_GAC_PREFIX=$SCRIPT_PATH/usr/
export PATH=$SCRIPT_PATH/usr/bin:$PATH
