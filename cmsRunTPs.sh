#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node
source /cvmfs/cms.cern.ch/cmsset_default.sh  ## if a bash script, use .sh instead of .csh
### for case 1. EOS have the following line, otherwise remove this line in case 2.

lineNum=$4
i=0
while read line; do
  i=$(( i + 1 ))
  test $i = $lineNum && inFile=$line;
done <"$5"

cp ${1}/${2}.tgz .
tar -xf ${2}.tgz
rm ${2}.tgz
export $SCRAM_ARCH=slc7_amd64_gcc700
cd ${3}/src/
scramv1 b ProjectRename
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
export X509_USER_PROXY=/afs/cern.ch/user/l/lroberts/myproxy
cmsRun ${6} $inFile   #inputFile=$inFile
cp inputs131X.root ${7}inputs131X_${4}.root
rm inputs131X.root
cd ${_CONDOR_SCRATCH_DIR}
rm -rf ${3}
