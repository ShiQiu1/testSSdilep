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
    config['do_var_log'] = False
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

    sys_FF    = None
    sys_CF    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_FF    = 'UP'
    elif systematic == 'FF_DN':      sys_FF    = 'DN'
    elif systematic == 'CF_UP':      sys_CF    = 'UP'
    elif systematic == 'CF_DN':      sys_CF    = 'DN'
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
    
    ## build and pt-sort objects
    ## ---------------------------------------
    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_','tau_'],
        keys = ['muons','electrons','jets','taus'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons','jets','taus'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='electrons',
        )
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='taus',
        )
    
    ''''    
    loop += ssdilep.algs.vars.BuildLooseElectrons(
        key_electrons='electrons',
        )
    loop += ssdilep.algs.vars.BuildLooseAndTightMuons(
        key_muons='muons',
        )
    '''
        
    ## build MET
    ## ---------------------------------------

        
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )
    
 
    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    #loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')

    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='atLeastFourLeptons_pT50')
    

    
    #loop += ssdilep.algs.vars.SR2ChannelFlavour()
    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.SignalComparisonVars (key_taus='taus') 
    loop += ssdilep.algs.vars.DiLeptonVars(key_taus='taus')
    loop += ssdilep.algs.vars.TauMuVars(key_taus='taus')
     
    
    ## configure histograms
    ## ---------------------------------------
    '''
    hist_list = []
    hist_list += ssdilep.hists.Main_hists.hist_list
    '''
    
    hist_list = []
    hist_list += ssdilep.hists.SR2Variables_hists.hist_list
    
    
    

    ##     Kinematics plots
    ## ---------------------------------------
    
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'FourLeptons',
            plot_all = True,
            do_var_check = False,
            hist_list    = hist_list,
            cut_flow = [
               ['noCut',None],
               ['MultiLeptondPhiMoreThan005Pi', None],
                             ],
            )
            
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'TwoLeptons',
            plot_all = True,
            do_var_check = False,
            hist_list    = ssdilep.hists.DiLeptonMain_hists.hist_list,
            cut_flow = [
               ['noCut',None],
               ['diLeptondPhiMoreThan005Pi', None],
                            ],
            )            
            
    loop += ssdilep.algs.algs.PlotAlg(
            region   = 'SignalComparison',
            plot_all = True,
            do_var_check = False,
            hist_list    = ssdilep.hists.SignalComparison_hists.hist_list,
            cut_flow = [
               ['noCut',None],
                            ],
            )  
        
        
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    min_entry = int(config.get('min_entry') if ('min_entry' in config.keys()) else  0)
    max_entry = int(config.get('events') if ('events' in config.keys()) else -1)
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


