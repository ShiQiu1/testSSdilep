#!/bin/bash

#INPATH_MC="/eos/user/s/sarnling/SignalSample600/ntupleFast.root"
INPATH_MC="/eos/user/s/sarnling/SignalSample600/ntupleFull.root"


INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
SCRIPT="j.plotter_signal_tau.py"


python ${INSCRIPT}/${SCRIPT} --input "/eos/user/s/sarnling/SignalSample600/ntupleFast.root"  --sampletype="mc" --samplename="ntuple_signal_tau_fast" --events=-1 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input "/eos/user/s/sarnling/SignalSample600/ntupleFull.root"  --sampletype="mc" --samplename="ntuple_signal_tau_full" --events=-1 #--config="sys:FF_DN"


