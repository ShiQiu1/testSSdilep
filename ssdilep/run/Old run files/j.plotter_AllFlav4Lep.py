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
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']


    sys_FF_ele   = None
    sys_FF_mu   = None
    sys_trig = None
    sys_id   = None
    sys_iso  = None
    sys_reco = None
    sys_TTVA = None
    sys_CF = None
    sys_kfactor = None
    sys_beam = None
    sys_choice = None
    sys_pdf = None
    sys_pi = None
    sys_scale_z = None
    ## tree systematics
    treeSys = ""
    if systematic == 'EG_RESOLUTION_ALL_UP': treeSys = "EG_RESOLUTION_ALL__1up"
    elif systematic == 'EG_RESOLUTION_ALL_DN': treeSys = "EG_RESOLUTION_ALL__1down"
    elif systematic == 'EG_SCALE_ALLCORR_UP': treeSys = "EG_SCALE_ALLCORR__1up"
    elif systematic == 'EG_SCALE_ALLCORR_DN': treeSys = "EG_SCALE_ALLCORR__1down"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_UP': treeSys = "EG_SCALE_E4SCINTILLATOR__1up"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_DN': treeSys = "EG_SCALE_E4SCINTILLATOR__1down"
    elif systematic == 'MUON_ID_DN':treeSys= "MUON_ID__1down"
    elif systematic == 'MUON_ID_UP':treeSys= "MUON_ID__1up"
    elif systematic == 'MUON_MS_DN':treeSys= "MUON_MS__1down"
    elif systematic == 'MUON_MS_UP':treeSys= "MUON_MS__1up"
    elif systematic == 'MUON_RESBIAS_DN':treeSys= "MUON_SAGITTA_RESBIAS__1down"
    elif systematic == 'MUON_RESBIAS_UP':treeSys= "MUON_SAGITTA_RESBIAS__1up"
    elif systematic == 'MUON_RHO_DN':treeSys= "MUON_SAGITTA_RHO__1down"
    elif systematic == 'MUON_RHO_UP':treeSys= "MUON_SAGITTA_RHO__1up"
    elif systematic == 'MUON_SCALE_DN':treeSys= "MUON_SCALE__1down"
    elif systematic == 'MUON_SCALE_UP':treeSys= "MUON_SCALE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1down"
    else:
        treeSys = "nominal"
        if systematic == None: pass
        elif systematic == 'ELEFF_UP':      sys_FF_ele   = 'UP'
        elif systematic == 'ELEFF_DN':      sys_FF_ele   = 'DN'
        elif systematic == 'MUFF_UP':      sys_FF_mu   = 'UP'
        elif systematic == 'MUFF_DN':      sys_FF_mu   = 'DN'
        elif systematic == 'CF_UP':      sys_CF   = 'UP'
        elif systematic == 'CF_DN':      sys_CF   = 'DN'
        elif systematic == 'TRIG_UP':    sys_trig = 'UP'
        elif systematic == 'TRIG_DN':    sys_trig = 'DN'
        elif systematic == 'TRIG_UPSTAT': sys_trig= 'UPSTAT'
        elif systematic == 'TRIG_UPSYS':  sys_trig= 'UPSYS'
        elif systematic == 'TRIG_DNSTAT': sys_trig= 'DNSTAT'
        elif systematic == 'TRIG_DNSYS':  sys_trig= 'DNSYS'
        elif systematic == 'ID_UP':      sys_id   = 'UP'
        elif systematic == 'ID_DN':      sys_id   = 'DN'
        elif systematic == 'ID_UPSTAT': sys_id    = 'UPSTAT'
        elif systematic == 'ID_DNSTAT': sys_id    = 'DNSTAT'
        elif systematic == 'ID_UPSYS':  sys_id    = 'UPSYS'
        elif systematic == 'ID_DNSYS':  sys_id    = 'DNSYS'
        elif systematic == 'ISO_UP':    sys_iso   = 'UP'
        elif systematic == 'ISO_DN':    sys_iso   = 'DN'
        elif systematic == 'ISO_UPSTAT':     sys_iso   = 'UPSTAT'
        elif systematic == 'ISO_DNSTAT':     sys_iso   = 'DNSTAT'
        elif systematic == 'ISO_UPSYS':     sys_iso   = 'UPSYS'
        elif systematic == 'ISO_DNSYS':     sys_iso   = 'DNSYS'
        elif systematic == 'RECO_UP':    sys_reco  = 'UP'
        elif systematic == 'RECO_DN':    sys_reco  = 'DN'    
        elif systematic == 'RECO_UPSTAT':  sys_reco  = 'UPSTAT'
        elif systematic == 'RECO_DNSTAT':  sys_reco  = 'DNSTAT'    
        elif systematic == 'RECO_UPSYS':  sys_reco  = 'UPSYS'
        elif systematic == 'RECO_DNSYS':  sys_reco  = 'DNSYS'    
        elif systematic == 'TTVA_UPSTAT':  sys_TTVA  = 'UPSTAT'
        elif systematic == 'TTVA_DNSTAT':  sys_TTVA  = 'DNSTAT'    
        elif systematic == 'TTVA_UPSYS':  sys_TTVA  = 'UPSYS'
        elif systematic == 'TTVA_DNSYS':  sys_TTVA  = 'DNSYS'    
        elif systematic == 'BEAM_UP':    sys_beam  = 'UP'
        elif systematic == 'BEAM_DN':    sys_beam  = 'DN'    
        elif systematic == 'CHOICE_UP':  sys_choice  = 'UP'
        elif systematic == 'CHOICE_DN':  sys_choice  = 'DN'    
        elif systematic == 'PDF_UP':     sys_pdf  = 'UP'
        elif systematic == 'PDF_DN':     sys_pdf  = 'DN'    
        elif systematic == 'PI_UP':      sys_pi  = 'UP'
        elif systematic == 'PI_DN':      sys_pi  = 'DN'
        elif systematic == 'SCALE_Z_UP': sys_scale_z  = 'UP'
        elif systematic == 'SCALE_Z_DN': sys_scale_z  = 'DN'

    assert treeSys!="", "Invalid systematic %s!"%(systematic)

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
    loop += ssdilep.algs.vars.BuildLooseTightElectronsMuons(
        key_electrons='electrons',
        key_muons='muons',
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
    loop += ssdilep.algs.EvWeights.LPXKfactor(
        cutflow='presel',
        key='lpx_kfactor',
        sys_beam = sys_beam,
        sys_choice = sys_choice,
        sys_pdf = sys_pdf,
        sys_pi = sys_pi,
        sys_scale_z = sys_scale_z,
        doAssert = True,
        nominalTree = True if treeSys == "nominal" else False
        )

    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')

    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassTriggersDLT')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoTruthPairsFromDCH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='FourLeptons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ZeroTotalCharge')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoSSLeptonPairs')
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
    loop += ssdilep.algs.EvWeights.SuperGenericFakeFactor(
        key='SuperGenericFakeFactor',
        config_file_e=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
        config_file_m=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
        config_fileCHF=os.path.join(main_path,'ssdilep/data/chargeFlipRates-28-03-2017.root'),
        sys_FFe=sys_FF_ele,
        sys_FFm=sys_FF_mu,
        sys_id_e = sys_id,
        sys_iso_e = sys_iso,
        sys_reco_e = sys_reco,
        sys_reco_m = sys_reco,
        sys_iso_m = sys_iso,
        sys_TTVA_m = sys_TTVA,
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
            region       = 'CR2Relaxed',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2ZVeto',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2DeltaMass',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ],
            )

    #Fakes regions
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2Relaxed_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2ZVeto_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2DeltaMass_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsControlRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'CR2_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['IsControlRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ],
            )

    #Signal region
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2Relaxed',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['IsSignalRegion2',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2ZVeto',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2DeltaMass',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ],
            )

    #loop here for signal
    for channel in ["eeee","eeem","eemm","emem","emmm","mmmm"]:
        loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2Relaxed-signal-'+channel,
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter'+channel,None],
                           ['IsSignalRegion2',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ],
            )

        loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2ZVeto-signal-'+channel,
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter'+channel,None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ],
            )

        loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2DeltaMass-signal-'+channel,
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter'+channel,None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
        loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2-signal-'+channel,
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter'+channel,None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ],
            )

    #Fakes regions
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2Relaxed_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2ZVeto_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2DeltaMass_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsSignalRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ],
            )
    

    #validation regions
    
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2Relaxed',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2ZVeto',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2DeltaMass',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['FourTightLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
                           ],
            )

    #Fakes regions
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2Relaxed_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2ZVeto_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['ZVeto',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2DeltaMass_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'VR2_fakes',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['DCHFilter',None],
                           ['AtLeastOneLooseLep',['SuperGenericFakeFactor']],
                           ['IsValidationRegion2',None],
                           ['DeltaMassOverMass',None],
                           ['ZVeto',None],
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



