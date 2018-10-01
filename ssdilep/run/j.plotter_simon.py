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
    
    '''
    loop += ssdilep.algs.vars.BuildTrigConfig(
        #required_triggers = ["HLT_mu26_imedium","HLT_mu26_ivarmedium", "HLT_mu50"],
        required_triggers = ["HLT_mu26_imedium","HLT_mu50"],
        #required_triggers = ["HLT_mu26_ivarmedium", "HLT_mu50"],
       key               = 'muons',
        )
   '''
    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_','tau_'],
        keys = ['muons','electrons_loose','jets','taus'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons_loose','jets','taus'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )
        
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='electrons_loose',
        )   
    
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='taus',
        )       

    ## build MET
    ## ---------------------------------------
    loop += ssdilep.algs.met.METCLUS(
        prefix='metFinalClus',
        key = 'met_clus',
        )

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')
   
   
   	## Presel cuts
   	##++++++++++++++++++++++++++++++++++++++ 
   # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllJetPt25')
   # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter')    
   # loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='JetCleaning') 
   
    ## muon cuts
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoMuons')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuLoose')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='MuNoFilterTT') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuEta247') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuZ0SinTheta05') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllMuIsoBound15') 
     
         
    ##Electron cut   
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleLHLoose')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='EleTT') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleEta247AndNotCrackRegion') 
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='AllEleZ0SinTheta05') 
         
		##Tau cuts
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoOSTau')
    
    ## initialize and/or decorate objects
    ## ---------------------------------------
    #loop += ssdilep.algs.vars.DiMuVars(key_muons='muons')
    #loop += ssdilep.algs.vars.DiEleVars(key_electrons='electrons_loose')
    #loop += ssdilep.algs.vars.TauVarsCollinearDimuon()    
    loop += ssdilep.algs.vars.DiTauHadVars() 
    #loop += ssdilep.algs.vars.TauHadEleVars() 
    
        
    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.Main_hists.hist_list
        
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------
    
    ## Z mass peak
    ## ---------------------------------------
    
    '''       
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'dimuon',
            plot_all     = True,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [ 
            ['TwoMuons',None],
             ],
            )   
              
		
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'TauEle',
            plot_all     = True,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [ 
            ['OSTauEle', None]                                 
              ],
            )             
    '''
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'TwoOSTau',
            plot_all     = True,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [ 
            ['noCut', None],
            ['TaudPhiLessThan95Pi', None],
            ['TaudPhiLessThan90Pi', None]                        
              ],
            )               
    
    
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    loop.run(chain, 0, config['events'],
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)


