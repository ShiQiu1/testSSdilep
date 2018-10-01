# This is a sample PBS script. It will request 1 processor on 1 node
# for 4 hours.
#   
#   Request 1 processors on 1 node 
#   
#PBS -l nodes=1:ppn=1


#PBS -l walltime=10:00:00
#
#   Request 4 gigabyte of memory per process
#
#PBS -l pmem=1gb
#!/bin/bash
STARTTIME=`date +%s`
date

#-------------------------------- ENV VARS -------------------------------
echo 
echo "Environment variables..."
echo " User name:   $USER"
echo " User home:   $HOME"
#echo " Queue name:  $PBS_O_QUEUE"
#echo " Job name:    $PBS_JOBNAME"
#echo " Job-id:      $PBS_JOBID"
echo " Task-id:     $PBS_ARRAYID"
#echo " Work dir:    $PBS_O_WORKDIR"
#echo " Submit host: $PBS_O_HOST"
#echo " Worker node: $HOSTNAME"
echo " Temp dir:    $TMPDIR"
echo " parameters passed: $*"
echo 

echo " SCRIPT:      $SCRIPT"
echo " OUTFILE:     $OUTFILE"
# echo " OUTPATH:     $OUTPATH"
echo " CONFIG:      $CONFIG"
echo " INTARBALL:   $INTARBALL"

echo
export 

MYDIR=Hist_${RANDOM}${RANDOM}

#-------------------------------- NODE CONFIG ------------------------------
echo "going to tmp node dir: $TMPDIR"
cd $TMPDIR

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "mkdir ${MYDIR}"
mkdir ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "cd ${MYDIR}"
cd ${MYDIR}

export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh --quiet
# source $AtlasSetup/scripts/asetup.sh AtlasOffline,21.0.7 --cmtconfig x86_64-slc6-gcc49-opt --nosave
. /ceph/grid/runtime/APPS/HEP/ATLAS-SITE
lsetup "root 6.08.06-x86_64-slc6-gcc62-opt"

## copy over working area
##echo "ls /data/fscutti"
##ls /data/fscutti

## copy over working area
echo "copying input tarball ${INTARBALL}..."
cp $INTARBALL .
date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"
echo "extracting input tarball..."
tar xzf *.tar.gz
date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"
echo "done setting working area"
ls -alh 

echo 
echo "setting up workarea..."
source ./setup.sh

echo 
echo "reading in config file '${CONFIG}', line ${PBS_ARRAYID}"
## READ IN CONFIG
line=`sed -n -e ${PBS_ARRAYID}p ${CONFIG}`
echo ${line}
arrIN=(${line//;/ });
SAMPLE=${arrIN[0]}
INPUT=${arrIN[1]}
SAMPLETYPE=${arrIN[2]}
CFG=${arrIN[3]}
echo "SAMPLE:     ${SAMPLE}"
echo "SAMPLETYPE: ${SAMPLETYPE}"
echo "INPUT:      ${INPUT}"
echo "CFG:        ${CFG}"


echo
echo "making a soft link locally..."
TMPINPUT="`mktemp ntuple.XXXXXXX`.root"
echo ln -s ${INPUT} ${TMPINPUT}
ln -s ${INPUT} ${TMPINPUT}

ls -alh


echo ""
echo "executing job..." 
echo ${SCRIPT1} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT1} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH1} ]; then mkdir -p ${OUTPATH1}; chmod a+rxw `dirname $OUTPATH1`; chmod a+rxw ${OUTPATH1}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH1}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH1}/${SAMPLE}.root
chmod a+wr ${OUTPATH1}/${SAMPLE}.root

if [[ ! -f "${OUTPATH1}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo ""
echo "executing job..." 
echo ${SCRIPT2} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT2} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH2} ]; then mkdir -p ${OUTPATH2}; chmod a+rxw `dirname $OUTPATH2`; chmod a+rxw ${OUTPATH2}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH2}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH2}/${SAMPLE}.root
chmod a+wr ${OUTPATH2}/${SAMPLE}.root

if [[ ! -f "${OUTPATH2}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo ""
echo "executing job..." 
echo ${SCRIPT3} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT3} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH3} ]; then mkdir -p ${OUTPATH3}; chmod a+rxw `dirname $OUTPATH3`; chmod a+rxw ${OUTPATH3}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH3}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH3}/${SAMPLE}.root
chmod a+wr ${OUTPATH3}/${SAMPLE}.root

if [[ ! -f "${OUTPATH3}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo ""
echo "executing job..." 
echo ${SCRIPT4} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT4} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH4} ]; then mkdir -p ${OUTPATH4}; chmod a+rxw `dirname $OUTPATH4`; chmod a+rxw ${OUTPATH4}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH4}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH4}/${SAMPLE}.root
chmod a+wr ${OUTPATH4}/${SAMPLE}.root

if [[ ! -f "${OUTPATH4}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo ""
echo "executing job..." 
echo ${SCRIPT5} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT5} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH5} ]; then mkdir -p ${OUTPATH5}; chmod a+rxw `dirname $OUTPATH5`; chmod a+rxw ${OUTPATH5}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH5}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH5}/${SAMPLE}.root
chmod a+wr ${OUTPATH5}/${SAMPLE}.root

if [[ ! -f "${OUTPATH5}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo ""
echo "executing job..." 
echo ${SCRIPT6} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"
${SCRIPT6} --input ${TMPINPUT} --sampletype ${SAMPLETYPE} --config "${CFG}" --samplename="ntuple"

ls -alh

echo "finished execution"

echo 
echo "preparing output dir..."

if [ ! -d ${OUTPATH6} ]; then mkdir -p ${OUTPATH6}; chmod a+rxw `dirname $OUTPATH6`; chmod a+rxw ${OUTPATH6}; fi

echo "copying output"
echo cp ${OUTFILE} ${OUTPATH6}/${SAMPLE}.root 
cp ${OUTFILE} ${OUTPATH6}/${SAMPLE}.root
chmod a+wr ${OUTPATH6}/${SAMPLE}.root

if [[ ! -f "${OUTPATH6}/${SAMPLE}.root" ]]; then
    echo "Out File not found!"
    exit 1
fi

echo "cd ${TMPDIR}"
cd ${TMPDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "rm -rf ${MYDIR}"
rm -rf ${MYDIR}

echo "ls ${TMPDIR} -la"
ls ${TMPDIR} -la

echo "finished job"

date
ENDTIME=`date +%s`
TOTALTIME=$(($ENDTIME-$STARTTIME))
echo "Total Time: ${TOTALTIME}s"







