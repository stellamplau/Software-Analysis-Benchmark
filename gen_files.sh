#!/bin/bash

dir="02.wo_Defects"
bmc_dir="bmc_"$dir
output_dir="output"
log_dir="log"

for file in $dir/*.c
do
  # TODO: chain these!
  filename=`basename $file`
  sed "s/#include\(.*\)$/\/\*\ #include\1\ \*\//" $file > $bmc_dir/$filename
  sed -i '1s;^;int idx,sink\;\nvoid *psink\;\ntypedef int intptr_t\;\n;' $bmc_dir/$filename
  sed -i '1s;^;int NULL\;\n;' $bmc_dir/$filename

  python file_gen.py $bmc_dir/$filename $output_dir $log_dir 2>> $log_dir/gen.err
done
