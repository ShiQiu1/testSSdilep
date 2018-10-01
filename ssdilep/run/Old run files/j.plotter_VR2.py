#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
j.postprocessor.py
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
    """
    loop += ssdilep.algs.vars.BuildTrigConfig(
        required_triggers = ["HLT_2e17_lhloose","HLT_e17_lhloose_nod0_mu14","HLT_2mu14"],
        key = 'electrons',
        )
    """
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

    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassTriggersDLT')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoTruthPairsFromDCH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='FourLeptons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ZeroTotalCharge')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 

    loop += ssdilep.algs.vars.SR2ChannelFlavour()

    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.MultiLeptonVars(key_muons='muons', key_electrons='electrons_loose')   

    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )
    """
    loop +=  ssdilep.algs.EvWeights.EleTrigSF(
            trig_list =  ["HLT_2e17_lhloose"],
            key       = "EleTrigSF",
            scale     = None,
            )
    """
        
    loop += ssdilep.algs.EvWeights.ChargeFlipEleSF(
            key='ChargeFlipEleSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-12-01-2017.root'),
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
            ele_index      = 0,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele0AllSF",
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
            ele_index      = 1,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele1AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele2RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele2AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele3RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele3AllSF",
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
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu0AllSF",
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
            mu_index      = 1,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu1AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu2RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu2AllSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu3RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu3AllSF",
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
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-27-03-2017.root'),
            ele_index=3,
            key='Ele3FF',
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
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_v9.root'),
            mu_index=3,
            key='Mu3FF',
            scale=sys_ff,
            )

    #Set Signal weight per couple: 
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=0,
        key='SRWeight0',
        sys=None,
        )
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=1,
        key='SRWeight1',
        sys=None,
        )
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=2,
        key='SRWeight2',
        sys=None,
        )
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=3,
        key='SRWeight3',
        sys=None,
        )
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=4,
        key='SRWeight4',
        sys=None,
        )
    loop += ssdilep.algs.EvWeights.SignalReWeighting(
        BR_index=5,
        key='SRWeight5',
        sys=None,
        )

    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.SR2Variables_hists.hist_list
    #hist_list += ssdilep.hists.PtOnly_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTTTL',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3RecoSF','Ele3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTTLT',['Ele0AllSF','Ele1AllSF','Ele2RecoSF','Ele3AllSF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTLTT',['Ele0AllSF','Ele1RecoSF','Ele2AllSF','Ele3AllSF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleLTTT',['Ele0RecoSF','Ele1RecoSF','Ele2AllSF','Ele3AllSF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTTLL',['Ele0AllSF','Ele1AllSF','Ele2RecoSF','Ele3RecoSF','Ele2FF','Ele3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTLTL',['Ele0AllSF','Ele1RecoSF','Ele2AllSF','Ele3RecoSF','Ele1FF','Ele3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleLLTT',['Ele0RecoSF','Ele1RecoSF','Ele2AllSF','Ele3AllSF','Ele0FF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleLTLT',['Ele0RecoSF','Ele1AllSF','Ele2RecoSF','Ele3AllSF','Ele0FF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleLTTL',['Ele0RecoSF','Ele1AllSF','Ele2AllSF','Ele3RecoSF','Ele0FF','Ele3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEE_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',None],
                           ['EleTLLT',['Ele0AllSF','Ele1RecoSF','Ele2RecoSF','Ele3AllSF','Ele1FF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTTTL',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3RecoSF','Mu3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTTLT',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Mu3AllSF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTLTT',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Mu3AllSF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuLTTT',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Mu3AllSF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTTLL',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Mu3RecoSF','Mu2FF','Mu3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTLTL',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Mu3RecoSF','Mu1FF','Mu3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuLLTT',['Mu0RecoSF','Mu1RecoSF','Mu2AllSF','Mu3AllSF','Mu0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuLTLT',['Mu0RecoSF','Mu1AllSF','Mu2RecoSF','Mu3AllSF','Mu0FF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuLTTL',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Mu3RecoSF','Mu0FF','Mu3FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMMM_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',None],
                           ['MuMuMuMuTLLT',['Mu0AllSF','Mu1RecoSF','Mu2RecoSF','Mu3AllSF','Mu1FF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTTTL',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTTLT',['Ele0AllSF','Ele1AllSF','Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTLTT',['Ele0AllSF','Ele1RecoSF','Mu0AllSF','Mu1AllSF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuLTTT',['Ele0RecoSF','Ele1AllSF','Mu0AllSF','Mu1AllSF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTTLL',['Ele0AllSF','Ele1AllSF','Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTLTL',['Ele0AllSF','Ele1RecoSF','Mu0AllSF','Mu1RecoSF','Ele1FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuLLTT',['Ele0RecoSF','Ele1RecoSF','Mu0AllSF','Mu1AllSF','Ele0FF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuLTLT',['Ele0RecoSF','Ele1AllSF','Mu0RecoSF','Mu1AllSF','Ele0FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuLTTL',['Ele0RecoSF','Ele1AllSF','Mu0AllSF','Mu1RecoSF','Ele0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEMUMU_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',None],
                           ['EEMuMuTLLT',['Ele0AllSF','Ele1RecoSF','Mu0RecoSF','Mu1AllSF','Ele1FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTTTL',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTTLT',['Ele0AllSF','Ele1AllSF','Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTLTT',['Ele0AllSF','Ele1RecoSF','Mu0AllSF','Mu1AllSF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuLTTT',['Ele0RecoSF','Ele1AllSF','Mu0AllSF','Mu1AllSF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTTLL',['Ele0AllSF','Ele1AllSF','Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTLTL',['Ele0AllSF','Ele1RecoSF','Mu0AllSF','Mu1RecoSF','Ele1FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuLLTT',['Ele0RecoSF','Ele1RecoSF','Mu0AllSF','Mu1AllSF','Ele0FF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuLTLT',['Ele0RecoSF','Ele1AllSF','Mu0RecoSF','Mu1AllSF','Ele0FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuLTTL',['Ele0RecoSF','Ele1AllSF','Mu0AllSF','Mu1RecoSF','Ele0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EMUEMU_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',None],
                           ['EEMuMuTLLT',['Ele0AllSF','Ele1RecoSF','Mu0RecoSF','Mu1AllSF','Ele1FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTTTL',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0RecoSF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTTLT',['Ele0AllSF','Ele1AllSF','Ele2RecoSF','Mu0AllSF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTLTT',['Ele0AllSF','Ele1RecoSF','Ele2AllSF','Mu0AllSF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuLTTT',['Ele0RecoSF','Ele1AllSF','Ele2AllSF','Mu0AllSF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTTLL',['Ele0AllSF','Ele1AllSF','Ele2RecoSF','Mu0RecoSF','Ele2FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTLTL',['Ele0AllSF','Ele1RecoSF','Ele2AllSF','Mu0RecoSF','Ele1FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuLLTT',['Ele0RecoSF','Ele1RecoSF','Ele2AllSF','Mu0AllSF','Ele0FF','Ele1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuLTLT',['Ele0RecoSF','Ele1AllSF','Ele2RecoSF','Mu0AllSF','Ele0FF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuLTTL',['Ele0RecoSF','Ele1AllSF','Ele2AllSF','Mu0RecoSF','Ele0FF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2EEEM_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',None],
                           ['EEEMuTLLT',['Ele0AllSF','Ele1RecoSF','Ele2RecoSF','Mu0AllSF','Ele1FF','Ele2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0AllSF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTTTL',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0RecoSF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTTLT',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Ele0AllSF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTLTT',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Ele0AllSF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_LTTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuLTTT',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Ele0AllSF','Mu0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TTLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTTLL',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Ele0RecoSF','Mu2FF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TLTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTLTL',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Ele0RecoSF','Mu1FF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_LLTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuLLTT',['Mu0RecoSF','Mu1RecoSF','Mu2AllSF','Ele0AllSF','Mu0FF','Mu1FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_LTLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuLTLT',['Mu0RecoSF','Mu1AllSF','Mu2RecoSF','Ele0AllSF','Mu0FF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_LTTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuLTTL',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Ele0RecoSF','Mu0FF','Ele0FF']],
                           ['IsControlRegion2',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2MMEM_TLLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',None],
                           ['MuMuEMuTLLT',['Mu0AllSF','Mu1RecoSF','Mu2RecoSF','Ele0AllSF','Mu1FF','Mu2FF']],
                           ['IsControlRegion2',None],
                           ],
            )

    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
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



