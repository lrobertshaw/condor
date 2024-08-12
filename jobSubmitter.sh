jobName="variousMassCutsTTbar"
inputFiles="/eos/user/l/lroberts/P2_Jets/InputData/CMSSW14/TTbar/"
# outputDir="/eos/user/l/lroberts/P2_Jets/WideCone/working_dir/jetMassStudies/hh4b/"

python3 condorSub.py "$jobName" "$inputFiles" #"$outputDir"