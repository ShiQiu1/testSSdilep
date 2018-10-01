#!/bin/bash


#INPATH_DATA="/afs/cern.ch/work/s/sarnling/DataTau/DatatoRun/user.kkarppin.DiLep.TEST.v1.dilepton.00311481.physics_Main.v01_tree.root/*.root,"
#INPATH_MC="/afs/cern.ch/work/s/sarnling/ZtautauMC/ZMC*.root,"
INPATH_DATA="/eos/user/s/sarnling/SUSY3Data/*.root,"
INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
SCRIPT="j.plotter_CF_tauMu.py"


python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA}  --sampletype="data" --samplename="ntuple_data_tau" --events=-1 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_MC}  --sampletype="mc" --samplename="ntuple_mc_tauMu" --events=4000000 #--config="sys:FF_DN"


