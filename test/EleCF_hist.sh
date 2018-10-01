#!/bin/bash

## Batch

#INPATH_DATA="/afs/cern.ch/user/s/sarnling/Exot12_data/*.physics_Main.root,"
#INPATH_DATA_EXOT19="/eos/user/s/sarnling/DatatoRun/user.tadej.DiLepAna.EXOT19Data.v2.fakes.0027****.physics_Main.r1_tree.root/*,"
INPATH_MC="/afs/cern.ch/user/s/sarnling/Exot12_mc/*.root,"
INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
SCRIPT="j.plotter_CF.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA}  --sampletype="data" --samplename="ntuple_data_exot12" --events=-1 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA_EXOT19}  --sampletype="data" --samplename="ntuple_data_exot19" --events=500000 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH_MC}  --sampletype="mc" --samplename="ntuple_mc_exot12" --events=100000 #--config="sys:FF_DN"


