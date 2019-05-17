log_dir="log"

for file in $log_dir/*.log
do
  filename=`basename $file .log`
  logfile=$log_dir/$filename.log
  errfile=$log_dir/$filename.err
  if grep -q "No errors found" $logfile 
  then
    echo $filename "RESULT: UNSAT"
  elif grep -q "Error(s) found" $logfile 
  then
    sat_msg=$(grep -A 1 "Error(s) found" $logfile | grep -v "Error(s) found" | sed "s/(\(.*\),\(.*\))/\2/")
    echo $filename "RESULT: SAT: " $sat_msg
  elif grep -q "(Failure" $errfile 
  then
    err_msg=$(grep '(Failure' $errfile | sed 's/.*Failure\ "\(.*\)".*/\1/')
    echo $filename "ERROR: "$err_msg
  elif grep -q "error:" $errfile 
  then
    err_msg=$(grep 'error: ' $errfile | sed 's/.*error: \(.*\).*/\1/')
    echo $filename "ERROR: " $err_msg
  elif [ ! -s $errfile ]
  then
    echo $filename "ERROR: (timeout)"
  else 
    echo $filename "ERROR: (unknown)"
  fi
done
