jobName="regConeSingNeutMaskSizes"
inputFiles="$PWD/inputData/singNeut.list"
outputDir="/shared/scratch/wq22321/regCone/maskSizes/singneut/"

python3 condorSub.py "$jobName" "$inputFiles" "$outputDir"