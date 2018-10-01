#!/bin/bash


#INPATH_DATA="/afs/cern.ch/work/s/sarnling/DataTau/DatatoRun/user.kkarppin.DiLep.TEST.v1.dilepton.00311481.physics_Main.v01_tree.root/*.root,"
INPATH_DATA="/eos/user/s/sarnling/SUSY3Data/*.root,"
#INPATH_MC="/afs/cern.ch/work/s/sarnling/ZtautauMC/ZMC*.root,"

INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
SCRIPT="j.plotter_CF_tau.py"


python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA}  --sampletype="data" --samplename="ntuple_data_tau_new" --events=-1 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_MC}  --sampletype="mc" --samplename="ntuple_mc_tau_CF_final" --events=-1 #--config="sys:FF_DN"


