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
    loop += ssdilep.algs.vars.BuildTrigConfig(
        #required_triggers = ["HLT_2e17_lhloose"],
        #key = 'electrons',
        required_triggers = ["HLT_mu26_ivarmedium", "HLT_mu50"],
        key               = 'muons',
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
    #loop += ssdilep.algs.vars.DiEleVars(key_electrons='electrons_loose')   
    loop += ssdilep.algs.vars.DiMuVars(key_muons='muons')

   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OddOSElectrons') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllElePt30') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleLHLoose') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleEta247AndNotCrackRegion') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleZ0SinTheta05') 
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleTrkd0Sig5') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllJetPt25') 
    
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllPairsM20')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuMedium')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuZ0SinTheta05')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuIsoBound15')

    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OddSSPairs')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OddSSMuons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 

    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )
    #loop +=  ssdilep.algs.EvWeights.EleTrigSF(
    #        trig_list =  ["HLT_2e17_lhloose"],
    #        key       = "EleTrigSF",
    #        scale     = None,
    #        )

    loop += ssdilep.algs.EvWeights.MuTrigSF(
            trig_list     = ["HLT_mu26_ivarmedium_OR_HLT_mu50"],
            mu_reco       = "Medium",
            mu_iso        = "FixedCutTightTrackOnly",
            key           = "MuTrigSF",
            scale         = None,
            )

    #loop += ssdilep.algs.EvWeights.ChargeFlipEleSF(
    #        key='ChargeFlipEleSF',
    #        config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-12-01-2017.root'),
    #        chargeFlipSF=True,
    #        )
    
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
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=0,
            key='Ele0FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=1,
            key='Ele1FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=2,
            key='Ele2FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
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

    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.SR1Muons_hists.hist_list
    #hist_list += ssdilep.hists.PtOnly_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## Inclusive MuMu SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMu_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuTT',['Mu0AllSF','Mu1AllSF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMu_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuTL',['Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMu_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuLT',['Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMu_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuLL',['Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    ## Inclusive MuMuE SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTTT',['Ele0AllSF','Mu0AllSF','Mu1AllSF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTTL',['Ele0AllSF','Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTLT',['Ele0AllSF','Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLTT',['Ele0RecoSF','Mu0AllSF','Mu1AllSF','Ele0FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTLL',['Ele0AllSF','Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLTL',['Ele0RecoSF','Mu0AllSF','Mu1RecoSF','Ele0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLLT',['Ele0RecoSF','Mu0RecoSF','Mu1AllSF','Ele0FF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuE_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLLL',['Ele0RecoSF','Mu0RecoSF','Mu1RecoSF','Ele0FF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    ## Inclusive EEMu SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTTL',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTLT',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLTT',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTLL',['Mu0AllSF','Mu1RecoSF','Mu2RecoSF','Mu1FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLTL',['Mu0RecoSF','Mu1AllSF','Mu2RecoSF','Mu0FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLLT',['Mu0RecoSF','Mu1RecoSF','Mu2AllSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1MuMuMu_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLLL',['Mu0RecoSF','Mu1RecoSF','Mu2RecoSF','Mu0FF','Mu1FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ],
            )

    ## Targeted MuMu SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMu_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuTT',['Mu0AllSF','Mu1AllSF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMu_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuTL',['Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMu_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuLT',['Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMu_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuLL',['Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )

    ## Targeted MuMuE SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTTT',['Ele0AllSF','Mu0AllSF','Mu1AllSF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTTL',['Ele0AllSF','Mu0AllSF','Mu1RecoSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTLT',['Ele0AllSF','Mu0RecoSF','Mu1AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLTT',['Ele0RecoSF','Mu0AllSF','Mu1AllSF','Ele0FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuTLL',['Ele0AllSF','Mu0RecoSF','Mu1RecoSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLTL',['Ele0RecoSF','Mu0AllSF','Mu1RecoSF','Ele0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLLT',['Ele0RecoSF','Mu0RecoSF','Mu1AllSF','Ele0FF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuE_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['EMuMuLLL',['Ele0RecoSF','Mu0RecoSF','Mu1RecoSF','Ele0FF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )

    ## Targeted: EEMu SR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_TTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_TTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTTL',['Mu0AllSF','Mu1AllSF','Mu2RecoSF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_TLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTLT',['Mu0AllSF','Mu1RecoSF','Mu2AllSF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_LTT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLTT',['Mu0RecoSF','Mu1AllSF','Mu2AllSF','Mu0FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_TLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuTLL',['Mu0AllSF','Mu1RecoSF','Mu2RecoSF','Mu1FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_LTL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLTL',['Mu0RecoSF','Mu1AllSF','Mu2RecoSF','Mu0FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_LLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLLT',['Mu0RecoSF','Mu1RecoSF','Mu2AllSF','Mu0FF','Mu1FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR1BMuMuMu_LLL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['SingleMuPassAndMatch',['MuTrigSF']],
                           ['MuMuMuLLL',['Mu0RecoSF','Mu1RecoSF','Mu2RecoSF','Mu0FF','Mu1FF','Mu2FF']],
                           ['SSMassAbove200GeV',None],
                           ['pTHAbove100',None],
                           ['MuonDRBelow35',None],
                           ['mTTotAbove250',None],
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



