import calendar
import time
import sys
import os

print('\nSTART\n')
ts = calendar.timegm(time.gmtime())

""" Parsing cmd line args """
jobName      = str( sys.argv[1] )    # 1st arg is job name ie TTBar
fileListName = str( sys.argv[2] )    # 2nd arg is file containing list of input files
outputDir    = str( sys.argv[3] )  #dat["outputFolder"]

jobCfg = "/eos/user/l/lroberts/P2_Jets/CMSSW_14_0_0_pre3/src/FastPUPPI/NtupleProducer/python/runInputs131X.py" #"/afs/cern.ch/user/l/lroberts/jetStudies/CMSSW_12_5_2_patch1/src/condor/runPerformanceNTuple.py"
jobScript = f"{os.getcwd()}/cmsRunTPs.sh"
rel = "CMSSW_14_0_0_pre3"

fileList = open(fileListName,"r").readlines()
rootDir = os.environ["CMSSW_BASE"] + "/src/FastPUPPI/condor/jobs/"
# jobDir = rootDir + jobName + "_" + str(ts) + "/"

jobDir = f"{rootDir}/{jobName}_{str(ts)}"
# CREATE REQUIRED DIRECTORIES
os.system(f"mkdir {jobDir}")
os.system(f"mkdir {jobDir}/info")
os.system(f"mkdir {jobDir}/data")

ret = 0
while ret == 0:
   # ret = os.system("mkdir " + jobDir)
   ret = os.chdir(os.environ["CMSSW_BASE"]+"/../")
   print('Tarballing ' + rel + "/...")
   ret = os.system("tar --exclude='perfTuple.root' --exclude='.tgz' --exclude='perfNano.root'  --exclude='.git' -zcf " + jobName + ".tgz " + rel)
   print( 'Done tarballing!')
   ret = os.system(f"mv {jobName}.tgz {jobDir}")
   ret = os.chdir(rootDir)

   with open(f"{jobDir}/{jobName}.jdl", 'w') as jdl:
      jdl.write("universe = vanilla\n")
      jdl.write("x509userproxy = /afs/cern.ch/user/l/lroberts/myproxy\n")
      # jdl.write("Transfer_Input_Files = /afs/cern.ch/user/l/lroberts/myproxy")
      jdl.write(f"Executable = {jobScript}\n")
      jdl.write("Should_Transfer_Files = YES\n")
      jdl.write("WhenToTransferOutput = ON_EXIT\n")
      jdl.write(f"Transfer_Input_Files = {jobScript}, {jobCfg}\n")
      jdl.write(f"Output = {jobDir}/$(ProcId).o\n")
      jdl.write(f"Error = {jobDir}/$(ProcId).e\n")
      jdl.write(f"Log = {jobDir}/$(ProcId).l\n")
      jdl.write(f"Arguments = {jobDir} {jobName} {rel} $(ProcId) {fileListName} {jobCfg} {outputDir}\n")
      jdl.write(f"+MaxRuntime = 28800\n")
      jdl.write(f"on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n")
      jdl.write(f"max_retries = 3\n")
      #jdl.write('requirements = (OpSysAndVer =?= "CentOS7")\n') #require centOS7 for correct architecture
      jdl.write(f"Queue {str(len(fileList))}\n")


   os.system(f"condor_submit --spool {jobDir}/{jobName}.jdl")
   sys.exit(0)

print("Submission failed.")
sys.exit(1)