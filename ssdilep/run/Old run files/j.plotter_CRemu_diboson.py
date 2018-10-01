#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
e/mu diboson CR
"""

## std modules
import os,re

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import ssdilep

GeV = 1000.0


#_____________________________________________________________________________
def analyze(config):
  
    ##-------------------------------------------------------------------------
    ## setup
    ##-------------------------------------------------------------------------
    config['tree']       = 'physics/nominal'
    config['do_var_log'] = True
    main_path = os.getenv('MAIN')
    
    ## build chain
    chain = ROOT.TChain(config['tree'])
    for fn in config['input']: chain.Add(fn)

    ##-------------------------------------------------------------------------
    ## systematics 
    ##-------------------------------------------------------------------------
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']

    sys_ff    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_ff    = 'up'
    elif systematic == 'FF_DN':      sys_ff    = 'dn'
    else: 
        assert False, "Invalid systematic %s!"%(systematic)


    ##-------------------------------------------------------------------------
    ## event loop
    ##-------------------------------------------------------------------------
    loop = pyframe.core.EventLoop(name='ssdilep',
                                  sampletype=config['sampletype'],
                                  samplename=config['samplename'],
                                  outfile=config['samplename']+".root",
                                  quiet=False,
                                  )
    
    ## configure the list of triggers 
    ## with eventual prescales and puts a
    ## trig list to the store for later cutflow
    ## ---------------------------------------
    loop += ssdilep.algs.vars.BuildTrigConfig(
        required_triggers = ["HLT_e17_lhloose_nod0_mu14"],
        key = 'leptons_dilepton',
        )
    
    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_'],
        keys = ['muons','electrons','jets'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons','jets'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='electrons',
        )
    loop += ssdilep.algs.vars.BuildLooseElectrons(
        key_electrons='electrons',
        )
    ## build MET
    ## ---------------------------------------
    loop += ssdilep.algs.met.METCLUS(
        prefix='metFinalClus',
        key = 'met_clus',
        )
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')

    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.ThreeLepVars(key_electrons='electrons_loose',key_muons='muons')   
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++

    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ThreeLeptons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneTotalCharge')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 


    loop += ssdilep.algs.EvWeights.OneOrTwoBjetsSF(
            key='OneOrTwoBjetsSF',
            )    

    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )
    loop +=  ssdilep.algs.EvWeights.EleTrigSF(
            trig_list =  ["HLT_e17_lhloose_nod0_mu14"],
            key       = "EleTrigSF",
            scale     = None,
            )

    loop += ssdilep.algs.EvWeights.ChargeFlipEleSF(
            key='ChargeFlipEleSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
            chargeFlipSF=True,
            )
    
    #Muon trigger efficiency implementation
    """
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Tight",
            mu_sublead_type = "Loose",
            key             = "EffCorrTL",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Tight",
            key             = "EffCorrLT",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Loose",
            key             = "EffCorrLL",
            scale           = None,
    """
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele0RecoSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele1RecoSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele0AllSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele1AllSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu0RecoSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu1RecoSF",
            scale         = None,
            )


    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu0AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu1AllSF",
            scale         = None,
            )



    #implementation of electron fake factors

    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-27-03-2017.root'),
            ele_index=0,
            key='Ele0FF',
            sys=None,
            )

    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-27-03-2017.root'),
            ele_index=1,
            key='Ele1FF',
            sys=None,
            )

    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-27-03-2017.root'),
            ele_index=2,
            key='Ele2FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_v9.root'),
            mu_index=0,
            key='Mu0FF',
            scale=sys_ff,
            )

    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_v9.root'),
            mu_index=1,
            key='Mu1FF',
            scale=sys_ff,
            )

    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_v9.root'),
            mu_index=2,
            key='Mu2FF',
            scale=sys_ff,
            )


    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.ThreeLepMain_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## OS CR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuTTL',['Ele0AllSF','Ele1AllSF','Mu0RecoSF','Mu0FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuTLL',['Ele0AllSF','Ele1RecoSF', 'Ele1FF','Mu0RecoSF', 'Mu0FF']],
                           ],
            )


    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuLLL',['Ele0RecoSF', 'Ele0FF','Ele1RecoSF', 'Ele1FF','Mu0RecoSF', 'Mu0FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuLTL',['Ele0RecoSF', 'Ele0FF', 'Ele1AllSF','Mu0RecoSF', 'Mu0FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuLLT',['Ele0RecoSF', 'Ele0FF','Ele1RecoSF', 'Ele1FF','Mu0AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuLTT',['Ele0RecoSF', 'Ele0FF', 'Ele1AllSF', 'Mu0AllSF']],                                                                                                                    ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEEMu_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoElectronsOneMuon',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EEMuTLT',['Ele0AllSF','Ele1RecoSF', 'Ele1FF','Mu0AllSF']], 
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuTTT',['Ele0AllSF','Mu0AllSF','Mu1AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuTTL',['Ele0AllSF','Mu0AllSF','Mu1RecoSF', 'Mu1FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuTLL',['Ele0AllSF','Mu0RecoSF', 'Mu0FF', 'Mu1RecoSF', 'Mu1FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuLLL',['Ele0RecoSF', 'Ele0FF', 'Mu0RecoSF', 'Mu0FF', 'Mu1RecoSF', 'Mu1FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuLTL',['Ele0RecoSF', 'Ele0FF','Mu0AllSF','Mu1RecoSF', 'Mu1FF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuLLT',['Ele0RecoSF', 'Ele0FF', 'Mu0RecoSF', 'Mu0FF','Mu1AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuLTT',['Ele0RecoSF', 'Ele0FF','Mu0AllSF','Mu1AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRdibosonEMuMu_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['TwoMuonsOneElectron',None],
                           ['OSPairInZWindow',None],
                           ['SSMassBelow200',None],
                           ['EMuMuTLT',['Ele0AllSF','Mu0RecoSF', 'Mu0FF','Mu1AllSF']],
                           ],
            )

    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    min_entry = int(config.get('min_entry') if ('min_entry' in config.keys()) else  0)
    max_entry = int(config.get('max_entry') if ('max_entry' in config.keys()) else -1)
    print min_entry," ",max_entry
    loop.run(chain, 
            min_entry = min_entry,
            max_entry = max_entry,
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)



