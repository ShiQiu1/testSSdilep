from hists import *


"""
This contains the histogram
configuration. Do not create
other config files !!!
"""

#Signal diagrams

h_nTau  = Hist1D( hname  = "h_nTau",
                              xtitle = "Numer of #tau-leptons",
                              ytitle = "Events", 
                              nbins  = 5,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "signalComparison",
                              vexpr  = "self.store['ntau']",
                            )
                            
h_prongTau  = Hist1D( hname  = "h_prongTau",
                              xtitle = "Numer of #tau-leptons",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = 0,
                              xmax   = 4,
                              dir    = "signalComparison",
                              vexpr  = "self.chain.tau_ntrk",
                            )                            


h_decayType  = Hist1D( hname  = "h_decayType",
                              xtitle = "Decay type",
                              ytitle = "Events", 
                              nbins  = 6,
                              xmin   = 0,
                              xmax   = 6,
                              dir    = "decayType",
                              vexpr  = "self.store['decayType']",
                            )
                            
h_dilep_mCol  = Hist1D( hname  = "h_dilep_mCol",
                              xtitle = "m_{Col}(#lep_{lead},#lep_{sublead}) [GeV]",
                              ytitle = "Events / (20 GeV)", 
                              nbins  = 60,
                              xmin   = 0.0,
                              xmax   = 1200.,
                              dir    = "collinear",
                              vexpr  = "self.store['dilep_mCol']/GeV",
                            )                            

h_dilep_mCol_80  = Hist1D( hname  = "h_dilep_mCol_80",
                              xtitle = "m_{Col}(#lep_{lead},#lep_{sublead}) [GeV]",
                              ytitle = "Events / (10 GeV)", 
                              nbins  = 120,
                              xmin   = 0.0,
                              xmax   = 1200.,
                              dir    = "collinear",
                              vexpr  = "self.store['dilep_mCol_80']/GeV",
                            )
                            
h_dilep_mCol_60  = Hist1D( hname  = "h_dilep_mCol_60",
                              xtitle = "m_{Col}(#lep_{lead},#lep_{sublead}) [GeV]",
                              ytitle = "Events / (10 GeV)", 
                              nbins  = 120,
                              xmin   = 0.0,
                              xmax   = 1200.,
                              dir    = "collinear",
                              vexpr  = "self.store['dilep_mCol_60']/GeV",
                            )                            

# -------
# Charge flip
# -------

h_electrons_chargeflip  = Hist1D( hname  = "h_electrons_chargeflip",
                              xtitle = "????",
                              ytitle = "Events", 
                              nbins  = 72900,
                              xmin   = 0,
                              xmax   = 72900,
                              dir    = "event",
                              vexpr  = "self.store['CFtotBin']",
                            )
                            
h_taus_chargeflip  = Hist1D( hname  = "h_taus_chargeflip",
                              xtitle = "Charge flip variable, x = f(p_{T1},#eta_{1},p_{T2},#eta_{2})",
                              ytitle = "Events", 
                              nbins  = 784,
                              xmin   = 0,
                              xmax   =784,
                              dir    = "event",
                              vexpr  = "self.store['taus_CFtotBin']",
                            )                            
                            

h_oneProngedTauTruthCF_eta_pT  = Hist2D( hname      = "h_oneProngedTauTruthCF_eta_pT",
                              xtitle  = "p_{T}(#tau_{true}) [GeV]",
                              ytitle  = "abs(#eta_{T}(#tau_[true}))", 
                              nbinsx  = 200,
                              xmin    = 0.,
                              xmax    = 200.,
                              nbinsy  = 200,
                              ymin    = 0.,
                              ymax    = 2.5,
                              dir     = "event",
                              vexpr   = "( self.store['OneProngedTauCF_pT'] / GeV , self.store['OneProngedTauCF_eta']",
                          )  
                          
h_threeProngedTauTruthCF_eta_pT  = Hist2D( hname      = "h_threeProngedTauTruthCF_eta_pT",
                              xtitle  = "p_{T}(#tau_{true}) [GeV]",
                              ytitle  = "abs(#eta_{T}(#tau_[true}))", 
                              nbinsx  = 200,
                              xmin    = 0.,
                              xmax    = 200.,
                              nbinsy  = 200,
                              ymin    = 0.,
                              ymax    = 2.5,
                              dir     = "event",
                              vexpr   = "( self.store['ThreeProngedTauCF_pT'] / GeV , self.store['ThreeProngedTauCF_eta']",
                          )                           
                                                    
# -------
# event
# -------

################    TauMu event    ################################

h_tauMu_mTVis  = Hist1D( hname  = "h_tauMu_mTVis",
                              xtitle = "m_{vis}(#tau_{lead},#tau_{sublead}) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 1000.,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_mTVis']/GeV",
                            )
h_tauMu_mTtot  = Hist1D( hname  = "h_tauMu_mTtot",
                              xtitle = "m_{tot}(#tau_{lead},#tau_{sublead}, MET) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 1000.,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_mTtot']/GeV",
                            )


h_tauMu_chargeprod  = Hist1D( hname  = "h_tauMu_chargeprod",
                              xtitle = "q(#tau_{lead}) #timesq (#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_charge_product']",
                            )

h_tauMu_dphi  = Hist1D( hname  = "h_tauMu_dphi",
                              xtitle = "#Delta#phi(#tau_{lead},#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_dphi']",
                            )
                            
h_tauMu_mCol  = Hist1D( hname  = "h_tauMu_mCol",
                              xtitle = "m_{Col}(#tau_{lead},#tau_{sublead}) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 1000.,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_mCol']/GeV",
                            )                            

h_tauMu_deta  = Hist1D( hname  = "h_tauMu_deta",
                              xtitle = "#Delta#eta(#tau_{lead},#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['tauMu_deta']",
                            ) 


################    DiTau event    ################################

h_taus_mTVis  = Hist1D( hname  = "h_taus_mTVis",
                              xtitle = "m_{vis}(#tau_{lead},#tau_{sublead}) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 300.,
                              dir    = "event",
                              vexpr  = "self.store['taus_mTVis']/GeV",
                            )
h_taus_mTtot  = Hist1D( hname  = "h_taus_mTtot",
                              xtitle = "m_{tot}(#tau_{lead},#tau_{sublead}, MET) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 300.,
                              dir    = "event",
                              vexpr  = "self.store['taus_mTtot']/GeV",
                            )


h_taus_chargeprod  = Hist1D( hname  = "h_taus_chargeprod",
                              xtitle = "q(#tau_{lead}) #timesq (#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['taus_charge_product']",
                            )

h_taus_dphi  = Hist1D( hname  = "h_taus_dphi",
                              xtitle = "#Delta#phi(#tau_{lead},#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['taus_dphi']",
                            )
                            
h_taus_mCol  = Hist1D( hname  = "h_taus_mCol",
                              xtitle = "m_{Col}(#tau_{lead},#tau_{sublead}) [GeV]",
                              ytitle = "Events / (2 GeV)", 
                              nbins  = 150,
                              xmin   = 0.0,
                              xmax   = 300.,
                              dir    = "event",
                              vexpr  = "self.store['taus_mCol']/GeV",
                            )                            

h_taus_deta  = Hist1D( hname  = "h_taus_deta",
                              xtitle = "#Delta#eta(#tau_{lead},#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['taus_deta']",
                            ) 
                            
#********    General event   ************************'   
                         
h_averageIntPerXing = Hist1D( hname  = "h_averageIntPerXing",
                              xtitle = "averageInteractionsPerCrossing",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.averageInteractionsPerCrossing",
                            )

h_actualIntPerXing = Hist1D( hname  = "h_actualIntPerXing",
                              xtitle = "actualInteractionsPerCrossing",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.actualInteractionsPerCrossing",
                            )

h_correct_mu = Hist1D( hname  = "h_correct_mu",
                              xtitle = "<#mu_{corr}>",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -0.5,
                              xmax   = 49.5,
                              dir    = "event",
                              vexpr  = "self.chain.correct_mu",
                            )

h_NPV = Hist1D( hname  = "h_NPV",
                              xtitle = "NPV",
                              ytitle = "Events", 
                              nbins  = 35,
                              xmin   = 0.,
                              xmax   = 35.0,
                              dir    = "event",
                              vexpr  = "self.chain.NPV",
                            )

h_nmuons = Hist1D( hname  = "h_nmuons",
                              xtitle = "N_{#mu}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.nmuon",
                            )

h_nelectrons = Hist1D( hname  = "h_nelectrons",
                              xtitle = "N_{e}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.nel",
                            )

h_nleptons = Hist1D( hname  = "h_nleptons",
                              xtitle = "N_{lep}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.store['nleptons']",
                            )

h_njets = Hist1D( hname  = "h_njets",
                              xtitle = "N_{jet}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.chain.njets",
                            )
h_nbjets = Hist1D( hname  = "h_nbjets",
                              xtitle = "N_{jet}",
                              ytitle = "Events", 
                              nbins  = 8,
                              xmin   = 0,
                              xmax   = 8,
                              dir    = "event",
                              vexpr  = "self.store['nbjets']",
                            )

h_muons_chargeprod  = Hist1D( hname  = "h_muons_chargeprod",
                              xtitle = "q(#mu_{lead}) #timesq (#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_muons_chargesum  = Hist1D( hname  = "h_muons_chargesum",
                              xtitle = "pair charge sum",
                              ytitle = "Events", 
                              nbins  = 6,
                              xmin   = -3,
                              xmax   = 3,
                              dir    = "event",
                              vexpr  = "self.store['charge_sum']",
                            )

h_muons_dphi  = Hist1D( hname  = "h_muons_dphi",
                              xtitle = "#Delta#phi(#mu_{lead},#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['muons_dphi']",
                            )

h_muons_deta  = Hist1D( hname  = "h_muons_deta",
                              xtitle = "#Delta#eta(#mu_{lead},#mu_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['muons_deta']",
                            )

h_muons_mVis  = Hist1D( hname  = "h_muons_mVis",
                              xtitle = "m_{vis}(#mu_{lead},#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_muons_mVisTot  = Hist1D( hname  = "h_muons_mVisTot",
                              xtitle = "m_{vis}(all leptons) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVisTot']/GeV",
                            )

h_muons_mTtot  = Hist1D( hname  = "h_muons_mTtot",
                              xtitle = "m^{tot}_{T}(#mu_{lead},#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )

h_muons_mTTot  = Hist1D( hname  = "h_muons_mTTot",
                              xtitle = "m^{tot}_{T}(all leptons + MET) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTTot']/GeV",
                            )

h_muons_pTH  = Hist1D( hname  = "h_muons_pTH",
                              xtitle = "p_T(SS_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['muons_pTH']/GeV",
                              )

h_muons_dR  = Hist1D( hname  = "h_muons_dR",
                              xtitle = "#DeltaR(SS_{lead})",
                              ytitle = "Events", 
                              nbins  = 60,
                              xmin   = 0.,
                              xmax   = 6.,
                              dir    = "event",
                              vexpr  = "self.store['muons_dR']",
                              )

h_mujet_dphi  = Hist1D( hname  = "h_mujet_dphi",
                              xtitle = "#Delta#phi(#mu_{lead},jet_{lead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['mujet_dphi']",
                            )

h_scdphi  = Hist1D( hname  = "h_scdphi",
                              xtitle = "#Sigma cos#Delta#phi",
                              ytitle = "Events", 
                              nbins  = 400,
                              xmin   = -2.,
                              xmax   = 2.,
                              dir    = "event",
                              vexpr  = "self.store['scdphi']",
                            )

h_electrons_chargeprod  = Hist1D( hname  = "h_electrons_chargeprod",
                              xtitle = "q(e_{lead}) #timesq (e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_electrons_dphi  = Hist1D( hname  = "h_electrons_dphi",
                              xtitle = "#Delta#phi(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['electrons_dphi']",
                            )

h_electrons_deta  = Hist1D( hname  = "h_electrons_deta",
                              xtitle = "#Delta#eta(e_{lead},e_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['electrons_deta']",
                            )

h_electrons_mVis  = Hist1D( hname  = "h_electrons_mVis",
                              xtitle = "m_{vis}(e_{lead},e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_electrons_mTtot  = Hist1D( hname  = "h_electrons_mTtot",
                              xtitle = "m^{tot}_{T}(e_{lead},e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )

h_ejet_dphi  = Hist1D( hname  = "h_ejet_dphi",
                              xtitle = "#Delta#phi(e_{lead},jet_{lead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['ejet_dphi']",
                            )
                            
# dilepton channel:

h_dilepton_chargeprod  = Hist1D( hname  = "h_dilepton_chargeprod",
                              xtitle = "q(l_{lead}) #timesq (l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_dilepton_dphi  = Hist1D( hname  = "h_dilepton_dphi",
                              xtitle = "#Delta#phi(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['dilepton_dphi']",
                            )
h_dilepton_dR  = Hist1D( hname  = "h_dilepton_dR",
                              xtitle = "#DeltaR(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "event",
                              vexpr  = "self.store['dilepton_dR']",
                            )
h_dilepton_pTH  = Hist1D( hname  = "h_dilepton_pTH",
                              xtitle = "p_{T}(l_{lead} + l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 5000,
                              xmin   = 0,
                              xmax   = 5000,
                              dir    = "event",
                              vexpr  = "self.store['pTH']/GeV",
                            )

h_dilepton_sumpT  = Hist1D( hname  = "h_dilepton_sumpT",
                              xtitle = "p_{T}(l_{lead}) + p_{T}(l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 7000,
                              xmin   = 0,
                              xmax   = 7000,
                              dir    = "event",
                              vexpr  = "self.store['sumpT']/GeV",
                            )

h_dilepton_deta  = Hist1D( hname  = "h_dilepton_deta",
                              xtitle = "#Delta#eta(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['dilepton_deta']",
                            )

h_dilepton_mTVis  = Hist1D( hname  = "h_dilepton_mVis",
                              xtitle = "m_{vis}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (20 GeV)", 
                              nbins  = 60,
                              xmin   = 0.0,
                              xmax   = 1200.,
                              dir    = "event",
                              vexpr  = "self.store['mTVis']/GeV",
                            )

h_dilepton_mTtot  = Hist1D( hname  = "h_dilepton_mTtot",
                              xtitle = "m^{tot}_{T}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (20 GeV)", 
                              nbins  = 60,
                              xmin   = 0.0,
                              xmax   = 1200.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )                            
                            

# mixed channel:

h_elemu_chargeprod  = Hist1D( hname  = "h_elemu_chargeprod",
                              xtitle = "q(l_{lead}) #timesq (l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 4,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "event",
                              vexpr  = "self.store['charge_product']",
                            )

h_elemu_dphi  = Hist1D( hname  = "h_elemu_dphi",
                              xtitle = "#Delta#phi(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['elemu_dphi']",
                            )
h_elemu_dR  = Hist1D( hname  = "h_elemu_dR",
                              xtitle = "#DeltaR(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "event",
                              vexpr  = "self.store['elemu_dR']",
                            )
h_elemu_pTH  = Hist1D( hname  = "h_elemu_pTH",
                              xtitle = "p_{T}(l_{lead} + l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 5000,
                              xmin   = 0,
                              xmax   = 5000,
                              dir    = "event",
                              vexpr  = "self.store['pTH']/GeV",
                            )

h_elemu_sumpT  = Hist1D( hname  = "h_elemu_sumpT",
                              xtitle = "p_{T}(l_{lead}) + p_{T}(l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 7000,
                              xmin   = 0,
                              xmax   = 7000,
                              dir    = "event",
                              vexpr  = "self.store['sumpT']/GeV",
                            )

h_elemu_deta  = Hist1D( hname  = "h_elemu_deta",
                              xtitle = "#Delta#eta(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['elemu_deta']",
                            )

h_elemu_mVis  = Hist1D( hname  = "h_elemu_mVis",
                              xtitle = "m_{vis}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )

h_elemu_mTtot  = Hist1D( hname  = "h_elemu_mTtot",
                              xtitle = "m^{tot}_{T}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mTtot']/GeV",
                            )

h_elejet_dphi  = Hist1D( hname  = "h_elejet_dphi",
                              xtitle = "#Delta#phi(ele,jet)",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['ele_jet_dphi']",
                            )

h_elejet_deta  = Hist1D( hname  = "h_elejet_deta",
                              xtitle = "#Delta#eta(ele,jet)",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['ele_jet_deta']",
                            )
h_elebjet_dphi  = Hist1D( hname  = "h_elebjet_dphi",
                              xtitle = "#Delta#phi(ele,bjet)",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['ele_bjet_dphi']",
                            )

h_elebjet_deta  = Hist1D( hname  = "h_elebjet_deta",
                              xtitle = "#Delta#eta(ele,jbet)",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['ele_bjet_deta']",
                            )

h_mujet_dphi  = Hist1D( hname  = "h_mujet_dphi",
                              xtitle = "#Delta#phi(#mu,jet)",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['mu_jet_dphi']",
                            )

h_mujet_deta  = Hist1D( hname  = "h_mujet_deta",
                              xtitle = "#Delta#eta(mu,jet)",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['mu_jet_deta']",
                            )
h_mubjet_dphi  = Hist1D( hname  = "h_mubjet_dphi",
                              xtitle = "#Delta#phi(#mu,bjet)",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['mu_bjet_dphi']",
                            )

h_mubjet_deta  = Hist1D( hname  = "h_mubjet_deta",
                              xtitle = "#Delta#eta(#mu,jbet)",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['mu_bjet_deta']",
                            )


#also adding OS variables for the three lepton case

h_OSelemu_dphi1  = Hist1D( hname  = "h_OSelemu_dphi1",
                              xtitle = "#Delta#phi(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['OSelemu_dphi1']",
                            )

h_OSelemu_deta1  = Hist1D( hname  = "h_OSelemu_deta",
                              xtitle = "#Delta#eta(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['OSelemu_deta1']",
                            )

h_OSelemu_mVis1  = Hist1D( hname  = "h_OSelemu_mVis1",
                              xtitle = "m_{vis}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['OSmVis1']/GeV",
                            )

h_OSelemu_mTtot1  = Hist1D( hname  = "h_OSelemu_mTtot1",
                              xtitle = "m^{tot}_{T}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['OSmTtot1']/GeV",
                            )

h_OSelemu_dphi2  = Hist1D( hname  = "h_OSelemu_dphi2",
                              xtitle = "#Delta#phi(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "event",
                              vexpr  = "self.store['OSelemu_dphi2']",
                            )

h_OSelemu_deta2  = Hist1D( hname  = "h_OSelemu_deta",
                              xtitle = "#Delta#eta(l_{lead},l_{sublead})",
                              ytitle = "Events", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['OSelemu_deta2']",
                            )

h_OSelemu_mVis2  = Hist1D( hname  = "h_OSelemu_mVis2",
                              xtitle = "m_{vis}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['OSmVis2']/GeV",
                            )

h_OSelemu_mTtot2  = Hist1D( hname  = "h_OSelemu_mTtot2",
                              xtitle = "m^{tot}_{T}(l_{lead},l_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['OSmTtot2']/GeV",
                            )
# -------
# jets
# -------
h_jetlead_pt  = Hist1D( hname  = "h_jetlead_pt",
                              xtitle = "p_{T}(jet_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "jets",
                              vexpr  = "self.store['jets'][0].tlv.Pt()/GeV",
                            )


# -------
# muons
# -------

# mulead
# ------
h_mulead_pt = Hist1D( hname  = "h_mulead_pt",
                              xtitle = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Pt() / GeV",
                            )

h_mulead_eta = Hist1D( hname  = "h_mulead_eta",
                              xtitle = "#eta(#mu_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Eta()",
                            )

h_mulead_phi = Hist1D( hname  = "h_mulead_phi",
                              xtitle = "#phi(#mu_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].tlv.Phi()",
                            )

h_mulead_trkd0 = Hist1D( hname  = "h_mulead_trkd0",
                              xtitle = "d^{trk}_{0}(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkd0",
                            )

h_mulead_trkd0sig = Hist1D( hname  = "h_mulead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (#mu_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkd0sig",
                            )

h_mulead_trkz0 = Hist1D( hname  = "h_mulead_trkz0",
                              xtitle = "z^{trk}_{0}(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkz0",
                            )

h_mulead_trkz0sintheta  = Hist1D( hname  = "h_mulead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(#mu_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].trkz0sintheta",
                            )

h_mulead_ptvarcone30  = Hist1D( hname  = "h_mulead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][0].ptvarcone30 / self.store['muons'][0].tlv.Pt()",
                            )

# musublead
# ---------
h_musublead_pt = Hist1D( hname  = "h_musublead_pt",
                              xtitle = "p_{T}(#mu_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Pt() / GeV",
                            )

h_musublead_eta = Hist1D( hname  = "h_musublead_eta",
                              xtitle = "#eta(#mu_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Eta()",
                            )

h_musublead_phi = Hist1D( hname  = "h_musublead_phi",
                              xtitle = "#phi(#mu_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].tlv.Phi()",
                            )

h_musublead_trkd0 = Hist1D( hname  = "h_musublead_trkd0",
                              xtitle = "d^{trk}_{0}(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkd0",
                            )

h_musublead_trkd0sig = Hist1D( hname  = "h_musublead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (#mu_{sublead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkd0sig",
                            )

h_musublead_trkz0 = Hist1D( hname  = "h_musublead_trkz0",
                              xtitle = "z^{trk}_{0}(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkz0",
                            )

h_musublead_trkz0sintheta  = Hist1D( hname  = "h_musublead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(#mu_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].trkz0sintheta",
                            )

h_musublead_ptvarcone30  = Hist1D( hname  = "h_musublead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{sublead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['muons'][1].ptvarcone30 / self.store['muons'][1].tlv.Pt()",
                            )

# ------------------
# Muon tag and probe
# ------------------
h_tag_pt = Hist1D( hname  = "h_tag_pt",
                              xtitle = "p_{T}(#mu_{tag}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['tag'].tlv.Pt() / GeV",
                            )

h_probe_pt = Hist1D( hname  = "h_probe_pt",
                              xtitle = "p_{T}(#mu_{probe}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['probe'].tlv.Pt() / GeV",
                            )

h_probe_ptiso = Hist1D( hname  = "h_probe_ptiso",
                              xtitle = "p_{T}(#mu_{probe}) + ptvarcone30 [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 1000,
                              xmin   = 0.0,
                              xmax   = 1000.0,
                              dir    = "muons",
                              vexpr  = "( self.store['probe'].tlv.Pt() + self.store['probe'].ptvarcone30 ) / GeV",
                            )

h_probe_ujet_pt = Hist1D( hname  = "h_probe_ujet_pt",
                              xtitle = "p_{T}(#mu_{probe} underlying jet) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2100,
                              xmin   = -100.0,
                              xmax   = 2000.0,
                              dir    = "muons",
                              vexpr  = "self.store['probe_ujet_pt']",
                            )

h_tag_ptvarcone30  = Hist1D( hname  = "h_tag_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{tag})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['tag'].ptvarcone30 / self.store['tag'].tlv.Pt()",
                            )
h_probe_ptvarcone30  = Hist1D( hname  = "h_probe_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(#mu_{probe})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "muons",
                              vexpr  = "self.store['probe'].ptvarcone30 / self.store['probe'].tlv.Pt()",
                            )

# -------
# MET
# -------
h_met_clus_et  = Hist1D( hname  = "h_met_clus_et",
                              xtitle = "E^{miss}_{T}(clus) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].tlv.Pt()/GeV",
                            )

h_met_clus_phi  = Hist1D( hname  = "h_met_clus_phi",
                              xtitle = "#phi(E^{miss}_{T}(clus))",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].tlv.Phi()",
                            )

h_met_trk_et  = Hist1D( hname  = "h_met_trk_et",
                              xtitle = "p^{miss}_{T}[GeV]",
                              ytitle = "Events / (20 GeV)", 
                              nbins  = 60,
                              xmin   = 0.,
                              xmax   = 1200.,
                              dir    = "met",
                              vexpr  = "self.store['met']/GeV",
                            )

h_met_trk_phi  = Hist1D( hname  = "h_met_trk_phi",
                              xtitle = "#phi(E^{miss}_{T}(trk))",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "met",
                              vexpr  = "self.store['met_trk'].tlv.Phi()",
                            )

h_met_clus_sumet  = Hist1D( hname  = "h_met_clus_sumet",
                              xtitle = "#Sigma E_{T}(clus) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_clus'].sumet/GeV",
                          )

h_met_trk_sumet  = Hist1D( hname  = "h_met_trk_sumet",
                              xtitle = "#Sigma E_{T}(trk) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.,
                              xmax   = 2000.,
                              dir    = "met",
                              vexpr  = "self.store['met_trk'].sumet/GeV",
                          )


# -------------
# Muon 2D hists
# -------------
h_mulead_ptiso_jetlead_pt  = Hist2D( hname      = "h_mulead_ptiso_jetlead_pt",
                              xtitle  = "p_{T}(#mu_{lead}) + ptvarcone30 [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "( self.store['muons'][0].tlv.Pt() + self.store['muons'][0].ptvarcone30 ) / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )


h_mulead_pt_mulead_iso  = Hist2D( hname      = "h_mulead_pt_mulead_iso",
                              xtitle  = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle  = "ptvarcone30(#mu_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "self.store['muons'][0].tlv.Pt() / GeV , self.store['muons'][0].ptvarcone30 / GeV",
                          )

h_mulead_pt_jetlead_pt  = Hist2D( hname      = "h_mulead_pt_jetlead_pt",
                              xtitle  = "p_{T}(#mu_{lead}) [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = " self.store['muons'][0].tlv.Pt() / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )

#-----------
# electrons
#-----------



# ele lead
# ------
h_elelead_pt = Hist1D( hname  = "h_elelead_pt",
                              xtitle = "p_{T}(e_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Pt() / GeV",
                            )

h_elelead_eta = Hist1D( hname  = "h_elelead_eta",
                              xtitle = "#eta(e_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Eta()",
                            )

h_elelead_phi = Hist1D( hname  = "h_elelead_phi",
                              xtitle = "#phi(e_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].tlv.Phi()",
                            )

h_elelead_trkd0 = Hist1D( hname  = "h_elelead_trkd0",
                              xtitle = "d^{trk}_{0}(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkd0",
                            )

h_elelead_trkd0sig = Hist1D( hname  = "h_elelead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (e_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkd0sig",
                            )

h_elelead_trkz0 = Hist1D( hname  = "h_elelead_trkz0",
                              xtitle = "z^{trk}_{0}(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkz0",
                            )

h_elelead_trkz0sintheta  = Hist1D( hname  = "h_elelead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(e_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].trkz0sintheta",
                            )

h_elelead_ptvarcone30  = Hist1D( hname  = "h_elelead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][0].ptvarcone30 / self.store['electrons'][0].tlv.Pt()",
                            )

# elesublead
# ---------
h_elesublead_pt = Hist1D( hname  = "h_elesublead_pt",
                              xtitle = "p_{T}(e_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Pt() / GeV",
                            )

h_elesublead_eta = Hist1D( hname  = "h_elesublead_eta",
                              xtitle = "#eta(e_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Eta()",
                            )

h_elesublead_phi = Hist1D( hname  = "h_elesublead_phi",
                              xtitle = "#phi(e_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].tlv.Phi()",
                            )

h_elesublead_trkd0 = Hist1D( hname  = "h_elesublead_trkd0",
                              xtitle = "d^{trk}_{0}(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkd0",
                            )

h_elesublead_trkd0sig = Hist1D( hname  = "h_elesublead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (e_{sublead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkd0sig",
                            )

h_elesublead_trkz0 = Hist1D( hname  = "h_elesublead_trkz0",
                              xtitle = "z^{trk}_{0}(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkz0",
                            )

h_elesublead_trkz0sintheta  = Hist1D( hname  = "h_elesublead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(e_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].trkz0sintheta",
                            )

h_elesublead_ptvarcone30  = Hist1D( hname  = "h_elesublead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{sublead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['electrons'][1].ptvarcone30 / self.store['electrons'][1].tlv.Pt()",
)

# -------------
# tag and probe
# -------------
h_eletag_pt = Hist1D( hname  = "h_eletag_pt",
                              xtitle = "p_{T}(e_{tag}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['tag'].tlv.Pt() / GeV",
                            )

h_eleprobe_pt = Hist1D( hname  = "h_eleprobe_pt",
                              xtitle = "p_{T}(e_{probe}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['probe'].tlv.Pt() / GeV",
                            )

h_eleprobe_ptiso = Hist1D( hname  = "h_eleprobe_ptiso",
                              xtitle = "p_{T}(e_{probe}) + ptvarcone30 [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 1000,
                              xmin   = 0.0,
                              xmax   = 1000.0,
                              dir    = "electrons",
                              vexpr  = "( self.store['probe'].tlv.Pt() + self.store['probe'].ptvarcone30 ) / GeV",
                            )

h_eleprobe_ujet_pt = Hist1D( hname  = "h_eleprobe_ujet_pt",
                              xtitle = "p_{T}(e_{probe} underlying jet) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2100,
                              xmin   = -100.0,
                              xmax   = 2000.0,
                              dir    = "electrons",
                              vexpr  = "self.store['probe_ujet_pt']",
                            )

h_eletag_ptvarcone30  = Hist1D( hname  = "h_eletag_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{tag})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['tag'].ptvarcone30 / self.store['tag'].tlv.Pt()",
                            )
h_eleprobe_ptvarcone30  = Hist1D( hname  = "h_eleprobe_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(e_{probe})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "electrons",
                              vexpr  = "self.store['probe'].ptvarcone30 / self.store['probe'].tlv.Pt()",
)

# --------
# 2D hists
# --------
h_elelead_ptiso_jetlead_pt  = Hist2D( hname      = "h_elelead_ptiso_jetlead_pt",
                              xtitle  = "p_{T}(e_{lead}) + ptvarcone30 [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "( self.store['electrons'][0].tlv.Pt() + self.store['electrons'][0].ptvarcone30 ) / GeV , self.store['jets'][0].tlv.Pt() / GeV",
                          )


h_elelead_pt_elelead_iso  = Hist2D( hname      = "h_elelead_pt_elelead_iso",
                              xtitle  = "p_{T}(e_{lead}) [GeV]",
                              ytitle  = "ptvarcone30(e_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = "self.store['electrons'][0].tlv.Pt() / GeV , self.store['electrons'][0].ptvarcone30 / GeV",
                          )

h_elelead_pt_jetlead_pt  = Hist2D( hname      = "h_elelead_pt_jetlead_pt",
                              xtitle  = "p_{T}(e_{lead}) [GeV]",
                              ytitle  = "p_{T}(jet_{lead}) [GeV]", 
                              nbinsx  = 1000,
                              xmin    = 0.,
                              xmax    = 1000.,
                              nbinsy  = 1000,
                              ymin    = 0.,
                              ymax    = 1000.,
                              dir     = "event",
                              vexpr   = " self.store['electrons'][0].tlv.Pt() / GeV , self.store['jets'][0].tlv.Pt() / GeV",

                          )


# ------------------------------
# mixed channel: leading lepton
# ------------------------------

# leading lepton
# ---------------

h_mulead_Origin_vs_Type  = Hist2D( hname      = "h_mulead_Origin_vs_Type",
                              xtitle  = "Type",
                              ytitle  = "Origin",
                              nbinsx  = 50,
                              xmin    = 0.,
                              xmax    = 50.,
                              nbinsy  = 50,
                              ymin    = 0.,
                              ymax    = 50.,
                              dir     = "event",
                              vexpr   = "self.store['muons'][0].truthType, self.store['muons'][0].truthOrigin",
                          )

h_elelead_Origin_vs_Type  = Hist2D( hname      = "h_elelead_Origin_vs_Type",
                              xtitle  = "Type",
                              ytitle  = "Origin",
                              nbinsx  = 50,
                              xmin    = 0.,
                              xmax    = 50.,
                              nbinsy  = 50,
                              ymin    = 0.,
                              ymax    = 50.,
                              dir     = "event",
                              vexpr   = "self.store['electrons'][0].truthType, self.store['electrons'][0].truthOrigin",
                          )

h_leplead_pt = Hist1D( hname  = "h_leplead_pt",
                              xtitle = "p_{T}(lep_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].tlv.Pt() / GeV",
                            )

h_leplead_eta = Hist1D( hname  = "h_leplead_eta",
                              xtitle = "#eta(lep_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].tlv.Eta()",
                            )

h_leplead_phi = Hist1D( hname  = "h_leplead_phi",
                              xtitle = "#phi(lep_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].tlv.Phi()",
                            )

h_leplead_trkd0 = Hist1D( hname  = "h_leplead_trkd0",
                              xtitle = "d^{trk}_{0}(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].trkd0",
                            )

h_leplead_trkd0sig = Hist1D( hname  = "h_leplead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (lep_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].trkd0sig",
                            )

h_leplead_trkz0 = Hist1D( hname  = "h_leplead_trkz0",
                              xtitle = "z^{trk}_{0}(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].trkz0",
                            )

h_leplead_trkz0sintheta  = Hist1D( hname  = "h_leplead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].trkz0sintheta",
                            )

h_leplead_ptvarcone30  = Hist1D( hname  = "h_leplead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(lep_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep1'].ptvarcone30 / self.store['lep1'].tlv.Pt()",
                            )

h_lep3_pt = Hist1D( hname  = "h_lep3_pt",
                              xtitle = "p_{T}(lep_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].tlv.Pt() / GeV",
                            )

h_lep3_eta = Hist1D( hname  = "h_lep3_eta",
                              xtitle = "#eta(lep_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].tlv.Eta()",
                            )

h_lep3_phi = Hist1D( hname  = "h_lep3_phi",
                              xtitle = "#phi(lep_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].tlv.Phi()",
                            )

h_lep3_trkd0 = Hist1D( hname  = "h_lep3_trkd0",
                              xtitle = "d^{trk}_{0}(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].trkd0",
                            )

h_lep3_trkd0sig = Hist1D( hname  = "h_lep3_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (lep_{lead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].trkd0sig",
                            )

h_lep3_trkz0 = Hist1D( hname  = "h_lep3_trkz0",
                              xtitle = "z^{trk}_{0}(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].trkz0",
                            )

h_lep3_trkz0sintheta  = Hist1D( hname  = "h_lep3_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(lep_{lead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].trkz0sintheta",
                            )

h_lep3_ptvarcone30  = Hist1D( hname  = "h_lep3_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(lep_{lead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep3'].ptvarcone30 / self.store['lep3'].tlv.Pt()",
                            )

# subleading lepton
# ------------------
h_lepsublead_pt = Hist1D( hname  = "h_lepsublead_pt",
                              xtitle = "p_{T}(lep_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].tlv.Pt() / GeV",
                            )

h_lepsublead_eta = Hist1D( hname  = "h_lepsublead_eta",
                              xtitle = "#eta(lep_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].tlv.Eta()",
                            )

h_lepsublead_phi = Hist1D( hname  = "h_lepsublead_phi",
                              xtitle = "#phi(lep_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].tlv.Phi()",
                            )

h_lepsublead_trkd0 = Hist1D( hname  = "h_lepsublead_trkd0",
                              xtitle = "d^{trk}_{0}(lep_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 80,
                              xmin   = -0.4,
                              xmax   = 0.4,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].trkd0",
                            )

h_lepsublead_trkd0sig = Hist1D( hname  = "h_lepsublead_trkd0sig",
                              xtitle = "d^{trk}_{0} / #sigma(d^{trk}_{0}) (lep_{sublead})",
                              ytitle = "Events / (0.01)", 
                              nbins  = 100,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].trkd0sig",
                            )

h_lepsublead_trkz0 = Hist1D( hname  = "h_lepsublead_trkz0",
                              xtitle = "z^{trk}_{0}(lep_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 40,
                              xmin   = -2,
                              xmax   = 2,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].trkz0",
                            )

h_lepsublead_trkz0sintheta  = Hist1D( hname  = "h_lepsublead_trkz0sintheta",
                              xtitle = "z^{trk}_{0}sin#theta(lep_{sublead}) [mm]",
                              ytitle = "Events / (0.01)", 
                              nbins  = 200,
                              xmin   = -1,
                              xmax   = 1,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].trkz0sintheta",
                            )

h_lepsublead_ptvarcone30  = Hist1D( hname  = "h_lepsublead_ptvarcone30",
                              xtitle = "ptvarcone30/p_{T}(lep_{sublead})",
                              ytitle = "Events / (0.001)", 
                              nbins  = 10000,
                              xmin   = 0.,
                              xmax   = 10.,
                              dir    = "elemu",
                              vexpr  = "self.store['lep2'].ptvarcone30 / self.store['lep1'].tlv.Pt()",
                            )

# ------------------------------
# SR2: 4 leptons
# ------------------------------

# lepton variables
# ---------------
h_lep1_pt = Hist1D( hname  = "h_lep1_pt",
                              xtitle = "p_{T}(lep1) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "leptons",
                              vexpr  = "self.store['lep1'].tlv.Pt() / GeV",
                            )

h_lep1_eta = Hist1D( hname  = "h_lep1_eta",
                              xtitle = "#eta(lep1)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "leptons",
                              vexpr  = "self.store['lep1'].tlv.Eta()",
                            )
h_lep1_phi = Hist1D( hname  = "h_lep1_phi",
                              xtitle = "#phi(lep1)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "leptons",
                              vexpr  = "self.store['lep1'].tlv.Phi()",
                            )
h_lep2_pt = Hist1D( hname  = "h_lep2_pt",
                              xtitle = "p_{T}(lep2) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "leptons",
                              vexpr  = "self.store['lep2'].tlv.Pt() / GeV",
                            )
h_lep2_eta = Hist1D( hname  = "h_lep2_eta",
                              xtitle = "#eta(lep2)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "leptons",
                              vexpr  = "self.store['lep2'].tlv.Eta()",
                            )
h_lep2_phi = Hist1D( hname  = "h_lep2_phi",
                              xtitle = "#phi(lep2)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "leptons",
                              vexpr  = "self.store['lep2'].tlv.Phi()",
                            )

h_lep3_pt = Hist1D( hname  = "h_lep3_pt",
                              xtitle = "p_{T}(lep3) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "leptons",
                              vexpr  = "self.store['lep3'].tlv.Pt() / GeV",
                            )

h_lep3_eta = Hist1D( hname  = "h_lep3_eta",
                              xtitle = "#eta(lep3)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "leptons",
                              vexpr  = "self.store['lep3'].tlv.Eta()",
                            )
h_lep3_phi = Hist1D( hname  = "h_lep3_phi",
                              xtitle = "#phi(lep3)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "leptons",
                              vexpr  = "self.store['lep3'].tlv.Phi()",
                            )

h_lep4_pt = Hist1D( hname  = "h_lep4_pt",
                              xtitle = "p_{T}(lep4) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.0,
                              dir    = "leptons",
                              vexpr  = "self.store['lep4'].tlv.Pt() / GeV",
                            )

h_lep4_eta = Hist1D( hname  = "h_lep4_eta",
                              xtitle = "#eta(lep4)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "leptons",
                              vexpr  = "self.store['lep4'].tlv.Eta()",
                            )
h_lep4_phi = Hist1D( hname  = "h_lep4_phi",
                              xtitle = "#phi(lep4)",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "leptons",
                              vexpr  = "self.store['lep4'].tlv.Phi()",
                            )



# couple variables
# ---------------
h_PosCouple_mVis  = Hist1D( hname  = "h_PosCouple_mVis",
                              xtitle = "m_{vis}(++) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis1']/GeV",
                            )
h_NegCouple_mVis  = Hist1D( hname  = "h_NegCouple_mVis",
                              xtitle = "m_{vis}(--) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis2']/GeV",
                            )

h_PosCouple_dR  = Hist1D( hname  = "h_PosCouple_dR",
                              xtitle = "#DeltaR_{vis}(++)",
                              ytitle = "Events", 
                              nbins  = 20,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "event",
                              vexpr  = "self.store['leps_dR1']",
                            )
h_PosCouple_Pt  = Hist1D( hname  = "h_PosCouple_Pt",
                              xtitle = "#p_T(++) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0,
                              xmax   = 2000,
                              dir    = "event",
                              vexpr  = "self.store['pTH1']/GeV",
                            )
h_NegCouple_dR  = Hist1D( hname  = "h_NegCouple_dR",
                              xtitle = "#DeltaR_{vis}(--)",
                              ytitle = "Events", 
                              nbins  = 20,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "event",
                              vexpr  = "self.store['leps_dR2']",
                            )
h_NegCouple_Pt  = Hist1D( hname  = "h_NegCouple_Pt",
                              xtitle = "#p_T(--) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0,
                              xmax   = 2000,
                              dir    = "event",
                              vexpr  = "self.store['pTH2']/GeV",
                            )

h_Couples_mVis  = Hist1D( hname  = "h_Couples_mVis",
                              xtitle = "(m_{vis}(++) + m_{vis}(--))/2 [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mVis']/GeV",
                            )


h_mOS1  = Hist1D( hname  = "h_mOS1",
                              xtitle = "(m_{OS1} [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mOS1']/GeV",
                            )
h_mOS2  = Hist1D( hname  = "h_mOS2",
                              xtitle = "(m_{OS2} [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mOS2']/GeV",
                            )
h_mOS3  = Hist1D( hname  = "h_mOS3",
                              xtitle = "(m_{OS3} [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mOS3']/GeV",
                            )
h_mOS4 = Hist1D( hname  = "h_mOS4",
                              xtitle = "(m_{OS4} [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['mOS4']/GeV",
                            )


h_Couples_FullMass  = Hist1D( hname  = "h_Couples_FullMass",
                              xtitle = "m_{vis}(++) + m_{vis}(--) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 2000,
                              xmin   = 0.0,
                              xmax   = 2000.,
                              dir    = "event",
                              vexpr  = "self.store['FullMass']/GeV",
                            )
h_Couples_dR  = Hist1D( hname  = "h_Couples_dR",
                              xtitle = "#DeltaR_{vis}",
                              ytitle = "Events", 
                              nbins  = 20,
                              xmin   = 0,
                              xmax   = 5,
                              dir    = "event",
                              vexpr  = "self.store['pairs_dR']",
                            )
h_Couples_dEta  = Hist1D( hname  = "h_Couples_dEta",
                              xtitle = "#Delta#eta_{vis}",
                              ytitle = "Events", 
                              nbins  = 100,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "event",
                              vexpr  = "self.store['pairs_deta']",
                            )
h_Couples_dPhi  = Hist1D( hname  = "h_Couples_dPhi",
                              xtitle = "#Delta#phi_{vis}",
                              ytitle = "Events", 
                              nbins  = 100,
                              xmin   = -3.5,
                              xmax   = 3.5,
                              dir    = "event",
                              vexpr  = "self.store['pairs_dphi']",
                            )
h_Couples_dM  = Hist1D( hname  = "h_Couples_dM",
                              xtitle = "#DeltaM(pair_{++}-pair_{--}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 400,
                              xmin   = -400,
                              xmax   = 400,
                              dir    = "event",
                              vexpr  = "self.store['dmVis']/GeV",
                            )
h_Couples_dMOverM  = Hist1D( hname  = "h_Couples_dMOverM",
                              xtitle = "#DeltaM(pair_{++}-pair_{--})/M [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 1000,
                              xmin   = -1.5,
                              xmax   = 1.5,
                              dir    = "event",
                              vexpr  = "self.store['dmOverM']",
                            )
h_Couples_dMOverAlphaMBeta  = Hist1D( hname  = "h_Couples_dMOverAlphaMBeta",
                              xtitle = "#DeltaM/ #alpha M^{#beta} [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 7000,
                              xmin   = -7,
                              xmax   = 7,
                              dir    = "event",
                              vexpr  = "self.store['dmOverAlphaMBeta']",
                            )
h_NegMassVsPosMass  = Hist2D( hname      = "h_NegMassVsPosMass",
                              xtitle  = "m_{++} [GeV]",
                              ytitle  = "m_{--} [GeV]",
                              nbinsx  = 2000,
                              xmin    = 0.,
                              xmax    = 2000.,
                              nbinsy  = 2000,
                              ymin    = 0.,
                              ymax    = 2000.,
                              dir     = "event",
                              vexpr   = "self.store['mVis1']/GeV , self.store['mVis2']/GeV",
                          )

# -------
# Taus
# -------

# taulead
# ------
h_taulead_pt = Hist1D( hname  = "h_taulead_pt",
                              xtitle = "p_{T}(#tau_{lead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 200,
                              xmin   = 0.0,
                              xmax   = 200.,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][0].tlv.Pt() / GeV",
                            )

h_taulead_eta = Hist1D( hname  = "h_taulead_eta",
                              xtitle = "#eta(#tau_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][0].tlv.Eta()",
                            )

h_taulead_phi = Hist1D( hname  = "h_taulead_phi",
                              xtitle = "#phi(#tau_{lead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][0].tlv.Phi()",
                            )


                            
h_taulead_ntrk  = Hist1D( hname  = "h_taulead_ntrk",
                              xtitle = "ntrk(#tau_{lead})",
                              ytitle = "Events", 
                              nbins  = 3,
                              xmin   = 1.,
                              xmax   = 4.,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][0].ntrk",
                            )         

# tausublead
# ---------
h_tausublead_pt = Hist1D( hname  = "h_tausublead_pt",
                              xtitle = "p_{T}(#tau_{sublead}) [GeV]",
                              ytitle = "Events / (1 GeV)", 
                              nbins  = 200,
                              xmin   = 0.0,
                              xmax   = 200,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][1].tlv.Pt() / GeV",
                            )

h_tausublead_eta = Hist1D( hname  = "h_tausublead_eta",
                              xtitle = "#eta(#tau_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 50,
                              xmin   = -2.5,
                              xmax   = 2.5,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][1].tlv.Eta()",
                            )

h_tausublead_phi = Hist1D( hname  = "h_tausublead_phi",
                              xtitle = "#phi(#tau_{sublead})",
                              ytitle = "Events / (0.1)", 
                              nbins  = 64,
                              xmin   = -3.2,
                              xmax   = 3.2,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][1].tlv.Phi()",
                            )

                            
h_tausublead_ntrk  = Hist1D( hname  = "h_tausublead_ntrk",
                              xtitle = "ntrk(#tau_{sublead})",
                              ytitle = "Events", 
                              nbins  = 3,
                              xmin   = 1.,
                              xmax   = 4.,
                              dir    = "taus",
                              vexpr  = "self.store['taus'][1].ntrk",
                            )                            
                          
                          
# EOF
