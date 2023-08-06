#!/bin/bash
# Copyright 2020 - RidgeRun LLC
# Author: Luis G. Leon Vega <luis.leon@ridgerun.com>
# Licenced under MIT
# Support: only Linux/MacOS with BASH

touch file_ok.txt
cat file_ok.txt
if [ "$?" -ne "0" ]; then
  exit 1
fi
exit 0
