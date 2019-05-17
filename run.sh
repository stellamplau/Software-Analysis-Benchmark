#!/bin/bash

run_dir="output_02.wo_Defects"
log_dir="log"

for file in $run_dir/*.c
do
  filename=`basename $file .c`
  echo $filename
  ./cerberus --bmc=true $file > $log_dir/$filename".log" 2>$log_dir/$filename".err" &
done
