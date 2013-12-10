#!/bin/sh
# script for execution of deployed applications
#
# Sets up the MCR environment for the current $ARCH and executes 
# the specified command.
#

MCRROOT='/usr/local/MATLAB/MATLAB_Compiler_Runtime/v716'

exe_name=$0
exe_dir=`dirname "$0"`
func=$1
shift

# Save stdout and stderr of FD's
exec 5>&1
exec 6>&2

STDOUTLOG=${func}-stdout.log
STDERRLOG=${func}-stderr.log

# Redirect into files
exec 1>$STDOUTLOG
exec 2>$STDERRLOG

echo "-----------------------------------------------------"

echo "$MCRROOT"

if [ "x${MCRROOT}" = "x" ]; then
  echo Usage:
  echo    $0 \<deployedMCRroot\> args
  echo 'Please specify location of MCR within <galaxy-dist>/tools/psysound/run_psysound3Compiled.sh'
else

  echo Setting up environment variables
  echo ---
  LD_LIBRARY_PATH=.:${MCRROOT}/runtime/glnxa64 ;
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/bin/glnxa64 ;
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRROOT}/sys/os/glnxa64;
  MCRJRE=${MCRROOT}/sys/java/jre/glnxa64/jre/lib/amd64 ;
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE}/native_threads ; 
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE}/server ;
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE}/client ;
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${MCRJRE} ;  
  XAPPLRESDIR=${MCRROOT}/X11/app-defaults ;
  export LD_LIBRARY_PATH;
  export XAPPLRESDIR;
  echo LD_LIBRARY_PATH is ${LD_LIBRARY_PATH};

  args=
  while [ $# -gt 0 ]; do
      token=`echo "$1" | sed 's/ /\\\\ /g'`   # Add blackslash before each blank
      args="${args} ${token}" 
      shift
  done

echo "calling: ${exe_dir}/psysound3Compiled $func $args"
eval "${exe_dir}/psysound3Compiled $func $args"

# Restore stdout and stderr
exec 1>&5
exec 2>&6


if [[ -s $STDERRLOG ]] ; then
an error was logged. report it to stderr and prepend it to stdout
  cat $STDERRLOG>&2
  echo "<b>">&1
  cat $STDERRLOG>&1
  echo "</b> <br>">&1
  cat $STDOUTLOG>&1
 #cleanup
  rm $STDERRLOG
else
  echo "Job completed successfully">&1
fi

#cleanup
rm $STDOUTLOG

fi
exit

