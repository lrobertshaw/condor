jobName="Phase2Spring24_SingleNeutrino_PU200"
inputFiles="/eos/cms/store/cmst3/group/l1tr/FastPUPPI/14_2_X/fpinputs_140X/v0/SingleNeutrino_PU200/"

python3 condorSub.py "$jobName" "$inputFiles"
