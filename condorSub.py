import calendar
import time
import sys
import os

print('\nSTART\n')
ts = calendar.timegm(time.gmtime())

ev_types = {
   "TTbar": {
      "inputFiles" : "/afs/cern.ch/user/l/lroberts/jetStudies/CMSSW_12_5_2_patch1/src/condor/fileListTTbar.list",
      "jobName" : "TTbar",
      "outputFolder" : "/eos/user/l/lroberts/outputFiles/seedSize/TTbar/"
   },
   "singNeut": {
      "inputFiles" : "/afs/cern.ch/user/l/lroberts/jetStudies/CMSSW_12_5_2_patch1/src/condor/fileListSingNeut.list",
      "jobName" : "singNeut",
      "outputFolder" : "/eos/user/l/lroberts/outputFiles/seedSize/singNeut/" #"/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/lroberts/outputFiles/jets16/SingNeut/"
   }
}

try:
   dat = ev_types[str(sys.argv[1])]
except:
   print("Invalid event type, valid event types: {}".format(str(ev_types.keys())))


# job level configurables
fileListName = dat["inputFiles"]   #"/afs/cern.ch/user/l/lroberts/jetStudies/CMSSW_12_5_2_patch1/src/condor/fileListTTbar.list"
jobName = dat["jobName"]   #"singNeutData"
jobCfg = "/afs/cern.ch/user/l/lroberts/jetStudies/CMSSW_12_5_2_patch1/src/condor/runPerformanceNTuple.py"

fileList = open(fileListName,"r").readlines()

jobScript = "cmsRun.sh"
rel = "CMSSW_12_5_2_patch1"
rootDir = os.environ["CMSSW_BASE"] + "/src/condor/"
#eosDir = "/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/lroberts/condor/" + jobName + "_" + str(ts) + "/"
jobDir = rootDir + jobName + "_" + str(ts) + "/"
ret = 0

while ret == 0:
   ret = os.system("mkdir " + jobDir)
   ret = os.chdir(os.environ["CMSSW_BASE"]+"/../")
   print('Tarballing ' + rel + "/...")
   ret = os.system("tar --exclude='perfTuple.root' --exclude='perfNano.root'  --exclude='.git' -zcf " + jobName + ".tgz " + rel)
   print( 'Done!')
   ret = os.system("mv " + jobName + ".tgz " + jobDir) 
   ret = os.chdir(rootDir)

   with open(jobDir + jobName + '.jdl', 'w') as jdl:
      jdl.write("universe = vanilla\n")
      #jdl.write("x509userproxy = $ENV(X509_USER_PROXY)\n")
      jdl.write("Executable = " + jobScript + "\n")
      jdl.write("Should_Transfer_Files = YES\n")
      jdl.write("WhenToTransferOutput = ON_EXIT\n")
      jdl.write("Transfer_Input_Files = " + jobScript + ", " + jobCfg + "\n")
      jdl.write("Output = "    + jobDir + "$(ProcId).o\n")
      jdl.write("Error = "     + jobDir + "$(ProcId).e\n")
      jdl.write("Log = "       + jobDir + "$(ProcId).l\n")
      jdl.write("Arguments = " + jobDir + " " + jobName + " " + rel + " " + " $(ProcId) " + fileListName + " " + jobCfg + " " + dat["outputFolder"] + "\n")
      jdl.write("+MaxRuntime = 28800\n")
      jdl.write("on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)\n")
      jdl.write("max_retries = 3\n")
      jdl.write('requirements = (OpSysAndVer =?= "CentOS7")\n') #jdl.write("requirements = Machine =!= LastRemoteHost\n")
      jdl.write("Queue " + str(len(fileList)) + "\n")

   os.system("condor_submit " + jobDir + jobName + ".jdl")
   print (str(len(fileList)) + " jobs submitted.")
   print ("\nYour jobs:")
   os.system("condor_q")
   print("")
   sys.exit(0)

print("Submission failed.")
sys.exit(1)