#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EvWeights.py:
weights applied
to the event
"""

from math import sqrt
from array import array
from copy import copy
# logging
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# ROOT
import ROOT
import metaroot

#std
import itertools
from itertools import combinations
from copy import copy
# pyframe
import pyframe

# pyutils
import rootutils

GeV = 1000.0

#------------------------------------------------------------------------------
class TrigPresc(pyframe.core.Algorithm):
    """
    Algorithm to unprescale data
    Applies the prescale according to a specific list of triggers
    """
    #__________________________________________________________________________
    def __init__(self, 
          cutflow     = None,
          #use_avg     = None,
          key         = None):
        pyframe.core.Algorithm.__init__(self, name="TrigPresc", isfilter=True)
        self.cutflow     = cutflow
        #self.use_avg     = use_avg
        self.key         = key
    #__________________________________________________________________________
    def execute(self, weight):
        trigpresc = 1.0
        
        # luminosity weighted prescales
        presc_dict = {
            "HLT_mu20_L1MU15"     : 354.153, 
            "HLT_mu24"            : 47.64, 
            "HLT_mu50"            : 1.0,
            #"HLT_mu26_imedium"    : 1.943,
            "HLT_mu26_ivarmedium" : 1.098,
            }

        if "data" in self.sampletype:
          ineff_list = []
          for trig in self.store["reqTrig"]: 
            #if trig in self.store["passTrig"].keys(): 
            for mu in self.store["muons"]:
              if mu.tlv.Pt()>=self.store["SingleMuTrigSlice"][trig][0] and mu.tlv.Pt()<self.store["SingleMuTrigSlice"][trig][1]:
                ineff_list.append(1. - 1. / presc_dict[trig])

          if ineff_list:
            tot_ineff = 1.0
            for ineff in ineff_list: tot_ineff *= ineff
            trigpresc -= tot_ineff
        
        trigpresc = 1. / trigpresc

        if self.key: 
          self.store[self.key] = trigpresc
        self.set_weight(trigpresc*weight)
        return True

class SuperGenericFakeFactor(pyframe.core.Algorithm):
    """
    SuperGenericFakeFactor
    """
    #__________________________________________________________________________
    def __init__(self, name="SuperGenericFakeFactor",
            key            = None,
            sys_FFe        = None,
            sys_FFm        = None,
            config_file_e  = None,
            config_file_m  = None,
            config_fileCHF = None,
            sys_id_e       = None,
            sys_iso_e      = None,
            sys_reco_e     = None,
            sys_reco_m     = None,
            sys_iso_m      = None,
            sys_TTVA_m     = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.sys_FFe           = sys_FFe
        self.sys_FFm           = sys_FFm
        self.config_file_e     = config_file_e
        self.config_file_m     = config_file_m
        self.config_fileCHF    = config_fileCHF
        self.sys_id_e          = sys_id_e
        self.sys_iso_e         = sys_iso_e
        self.sys_reco_e        = sys_reco_e
        self.sys_reco_m        = sys_reco_m
        self.sys_iso_m         = sys_iso_m
        self.sys_TTVA_m        = sys_TTVA_m

        assert key, "Must provide key for storing mu reco sf"
        assert config_file_e, "Must provide config file!"
        assert config_file_m, "Must provide config file!"
        assert config_fileCHF, "Must provide config file!"
    #_________________________________________________________________________
    def initialize(self):

      f = ROOT.TFile.Open(self.config_file_e)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file_e)
      
      if self.sys_FFe=="UP":
        h_ff = f.Get("FFup")
      elif self.sys_FFe=="DN":
        h_ff = f.Get("FFdn")
      else:
        h_ff = f.Get("FF")
      assert h_ff, "Failed to get 'h_ff' from %s"%(self.config_file_e)

      self.h_ff = h_ff.Clone()
      self.h_ff.SetDirectory(0)
      f.Close()

      f = ROOT.TFile.Open(self.config_file_m)
      assert f, "Failed to open fake-factor config file: %s"%(self.config_file_m)
      
      g_ff = f.Get("g_ff_stat_sys")

      assert g_ff, "Failed to get 'h_ff' from %s"%(self.config_file_m)

      self.g_ff = g_ff.Clone()
      f.Close()

      fchf = ROOT.TFile.Open(self.config_fileCHF)
      assert fchf, "Failed to open charge-flip config file: %s"%(self.config_fileCHF)

      h_etaFunc = fchf.Get("etaFunc")
      assert h_etaFunc, "Failed to get 'h_etaFunc' from %s"%(self.config_fileCHF)
      h_ptFunc = fchf.Get("ptFunc")
      assert h_ptFunc, "Failed to get 'h_ptFunc' from %s"%(self.config_fileCHF)

      h_etaRateMC = fchf.Get("MCEtaRate")
      assert h_etaRateMC, "Failed to get 'h_etaRateMC' from %s"%(self.config_fileCHF)
      h_ptRateMC = fchf.Get("MCPtRate")
      assert h_ptRateMC, "Failed to get 'h_ptRateMC' from %s"%(self.config_fileCHF)

      h_etaRateData = fchf.Get("dataEtaRate")
      assert h_etaRateData, "Failed to get 'h_etaRateData' from %s"%(self.config_fileCHF)
      h_ptRateData = fchf.Get("dataPtRate")
      assert h_ptRateData, "Failed to get 'h_ptRateData' from %s"%(self.config_fileCHF)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)

      self.h_etaRateMC = h_etaRateMC.Clone()
      self.h_ptRateMC  = h_ptRateMC.Clone()
      self.h_etaRateMC.SetDirectory(0)
      self.h_ptRateMC.SetDirectory(0)

      self.h_etaRateData = h_etaRateData.Clone()
      self.h_ptRateData  = h_ptRateData.Clone()
      self.h_etaRateData.SetDirectory(0)
      self.h_ptRateData.SetDirectory(0)
      fchf.Clone()

      self.isoLevels = [
      "isolLoose",
      "isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]

      #Electron
      self.id_sys_e = 0
      if self.sys_id_e == "UP":
        self.id_sys_e = 2
      elif self.sys_id_e == "DN":
        self.id_sys_e = 1

      self.iso_sys_e = 0
      if self.sys_iso_e == "UP":
        self.iso_sys_e = 2
      elif self.sys_iso_e == "DN":
        self.iso_sys_e = 1

      self.reco_sys_e = 0
      if self.sys_reco_e == "UP":
        self.reco_sys_e = 2
      elif self.sys_reco_e == "DN":
        self.reco_sys_e = 1

      #Muon
      self.reco_sys_m = 0
      if self.sys_reco_m == "UPSTAT":
        self.reco_sys_m = 4
      elif self.sys_reco_m == "UPSYS":
        self.reco_sys_m = 8
      elif self.sys_reco_m == "DNSTAT":
        self.reco_sys_m = 3
      elif self.sys_reco_m == "DNSYS":
        self.reco_sys_m = 7

      self.iso_sys_m=0
      if self.sys_iso_m ==   "UPSTAT":
        self.iso_sys_m= 2
      elif self.sys_iso_m == "UPSYS":
        self.iso_sys_m= 4
      elif self.sys_iso_m == "DNSTAT":
        self.iso_sys_m= 1
      elif self.sys_iso_m == "DNSYS":
        self.iso_sys_m= 3

      self.TTVA_sys_m=0
      if self.sys_TTVA_m ==   "UPSTAT":
        self.TTVA_sys_m= 2
      elif self.sys_TTVA_m == "UPSYS":
        self.TTVA_sys_m= 4
      elif self.sys_TTVA_m == "DNSTAT":
        self.TTVA_sys_m= 1
      elif self.sys_TTVA_m == "DNSYS":
        self.TTVA_sys_m= 3

    #_________________________________________________________________________
    def execute(self, weight):

      if "mc" in self.sampletype and self.chain.mcChannelNumber in range(306538,306560):
          if len(self.store['muons_tight']) != len(self.store['muons']) or len(self.store['electrons_loose']) != len(self.store['electrons_tight']) :
              if self.key:
                self.store[self.key] = 0.
                return True

      sf = 1.0
      if len(self.store['muons_tight']) != len(self.store['muons']) or len(self.store['electrons_loose']) != len(self.store['electrons_tight']):
        sf = -1.0
      muons = self.store['muons']
      electrons = self.store['electrons_loose']

      for ele in electrons:
        if (ele.isIsolated_Loose and ele.LHMedium) :
          if "mc" in self.sampletype : 
            sf *= getattr(ele,"IsoEff_SF_"   + self.IDLevels[1] + self.isoLevels[0] ).at(self.iso_sys_e)
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[1][0:-3] ).at(self.id_sys_e)
            sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys_e)
            ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
            etaBin = self.h_etaFunc.FindBin( abs( ele.caloCluster_eta ) )
            if ptBin==self.h_ptFunc.GetNbinsX()+1:
              ptBin -= 1 
            if ele.electronType() in [2,3]:
              sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
            elif ele.electronType() in [1]:
              probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
              probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
              sf *= ( 1 - probData )/( 1 - probMC )
          else :
            pass
        else :
          sf *= -self.h_ff.GetBinContent( self.h_ff.FindBin( ele.tlv.Pt()/GeV, abs( ele.caloCluster_eta ) ) )
          if "mc" in self.sampletype :
            sf *= getattr(ele,"PIDEff_SF_LH" + self.IDLevels[0][0:-3] ).at(self.id_sys_e)
            sf *= getattr(ele,"RecoEff_SF").at(self.reco_sys_e)
          else :
            pass

      for muon in muons:
        if (muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig <= 3.0) :
          if "mc" in self.sampletype : 
            sf *= getattr(muon,"_".join(["IsoEff","SF","Iso"+"FixedCutTightTrackOnly"])).at(self.iso_sys_m)
            sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys_m)
            sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys_m)
          else :
            pass
        else :
          ff_mu = 0.
          eff_up_mu = 0.
          eff_dn_mu = 0.
          for ibin_mu in xrange(1,self.g_ff.GetN()):
            edlow = self.g_ff.GetX()[ibin_mu] - self.g_ff.GetEXlow()[ibin_mu]
            edhi  = self.g_ff.GetX()[ibin_mu] + self.g_ff.GetEXhigh()[ibin_mu]
            if muon.tlv.Pt()/GeV>=edlow and muon.tlv.Pt()/GeV<edhi:
              ff_mu = self.g_ff.GetY()[ibin_mu]
              eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
              eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
              break
          if self.sys_FFm == 'UP': ff_mu +=eff_up_mu
          if self.sys_FFm == 'DN': ff_mu -=eff_dn_mu
          sf *= -ff_mu
          if "mc" in self.sampletype :
            sf *= getattr(muon,"_".join(["RecoEff","SF","Reco"+"Medium"])).at(self.reco_sys_m)
            sf *= getattr(muon,"_".join(["TTVAEff","SF"])).at(self.TTVA_sys_m)
          else :
            pass

      if self.key: 
        self.store[self.key] = sf
      return True

#------------------------------------------------------------------------------                                                                                                   
class SignalReWeighting(pyframe.core.Algorithm):
    """                                                                                                                                                                            
    SignalReWeighting

    """
    #__________________________________________________________________________                                                                                                    
    def __init__(self, name="SignalReWeighting",
                 BR_index=None,
                 key=None,
                 sys=None,
                 ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.BR_index          = BR_index
        self.key               = key

        assert key, "Must provide key for applying Signal Reweighting"
    #_________________________________________________________________________                                                                                                     
    def initialize(self):
      pass
    #_________________________________________________________________________                                                                                                     
    def execute(self, weight):
      sf=1.0
      if (("mc" in self.sampletype) and (self.chain.mcChannelNumber in range(306538,306560))):
          sf=0
          #now we want to select normalization accordingly to the BR we want to set
          # 0 BR: 100% to electrons  --> pdgID branch 44
          # 1 BR: 100% BR to muons   -->              52
          # 2 BR: 50% ee 50% mm      -->              48
          # 3 BR: 50% em 50% em      -->              48
          # 4 BR: 50% ee 50% em      -->              46
          # 5 BR: 50% mm 50% em      -->              50
          if((self.chain.HLpp_Daughters.size()==2 and self.chain.HLmm_Daughters.size()==2) or (self.chain.HRpp_Daughters.size()==2 and self.chain.HRmm_Daughters.size()==2)):

              pdgId_branchL = []
              pdgId_branchR = []
              
              for pdgId_Lpp in self.chain.HLpp_Daughters: pdgId_branchL += [abs(pdgId_Lpp)]
              for pdgId_Lmm in self.chain.HLmm_Daughters: pdgId_branchL += [abs(pdgId_Lmm)]
              for pdgId_Rpp in self.chain.HRpp_Daughters: pdgId_branchR += [abs(pdgId_Rpp)]
              for pdgId_Rmm in self.chain.HRmm_Daughters: pdgId_branchR += [abs(pdgId_Rmm)]

              channel_flavour = array('d',[44,52,48,48,46,50])
              BR = array('d',[16,16,8,4,4,4])

              #additional check for the ambiguous channel
              if(len(pdgId_branchL)==4):
                  if(pdgId_branchL[0]+pdgId_branchL[1]+pdgId_branchL[2]+pdgId_branchL[3] == channel_flavour[self.BR_index]):
                      if(self.BR_index == 2 and (pdgId_branchL[0]+pdgId_branchL[1] == 22)): 
                          sf=BR[self.BR_index]
                      if(self.BR_index == 3 and (pdgId_branchL[0]+pdgId_branchL[1] == 24)): 
                          sf=BR[self.BR_index]
                      else: 
                          sf=BR[self.BR_index]
                      if(self.BR_index==0 and sf!=16.0): print "NOOO"    
                      #print self.BR_index
                       #   print sf
              elif(len(pdgId_branchR)==4):
                  if(pdgId_branchR[0]+pdgId_branchR[1]+pdgId_branchR[2]+pdgId_branchR[3] == channel_flavour[self.BR_index]):
                      if(self.BR_index == 2 and (pdgId_branchR[0]+pdgId_branchR[1] == 22)):  sf=BR[self.BR_index]
                      if(self.BR_index == 3 and (pdgId_branchR[0]+pdgId_branchR[1] == 24)):  sf=BR[self.BR_index]
                      else:  sf=BR[self.BR_index]

              else: 
                  print "Warning, I'm putting this event weight to zero"
                  sf=0

          else: print "SignalReWeighting: Something strange with this event, no daughters from DCH!"
          
      if self.key:
        self.store[self.key] = sf
      return True


#------------------------------------------------------------------------------
class Pileup(pyframe.core.Algorithm):
    """
    multiply event weight by pileup weight

    if 'key' is specified the pileup weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="Pileup", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wpileup = self.chain.weight_pileup
            if self.key: self.store[self.key] = wpileup
            self.set_weight(wpileup*weight)
        return True


#------------------------------------------------------------------------------
class MCEventWeight(pyframe.core.Algorithm):
    """
    multiply event weight by MC weight

    if 'key' is specified the MC weight will be put in the store
    """
    #__________________________________________________________________________
    def __init__(self, cutflow=None,key=None):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)
        self.cutflow = cutflow
        self.key = key
    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
            wmc = self.chain.mcEventWeight
            if self.key: self.store[self.key] = wmc
            self.set_weight(wmc*weight)
        return True


#------------------------------------------------------------------------------
class LPXKfactor(pyframe.core.Algorithm):
    """
    multiply event weight by Kfactor from LPX tool

    """
  #__________________________________________________________________________
    def __init__(self, 
                 cutflow=None,
                 key=None,
                 sys_beam=None,
                 sys_choice=None,
                 sys_pdf=None,
                 sys_pi=None,
                 sys_scale_z=None,
                 doAssert=True,
                 nominalTree=True
                 ):
        pyframe.core.Algorithm.__init__(self, name="MCEventWeight", isfilter=True)

        self.cutflow = cutflow
        self.key = key
        self.sys_beam = sys_beam
        self.sys_choice = sys_choice
        self.sys_pdf = sys_pdf
        self.sys_pi = sys_pi
        self.sys_scale_z = sys_scale_z
        self.doAssert = doAssert
        self.nominalTree = nominalTree

        self.kfactorSys = 0
        if self.sys_beam == "DN":
          self.kfactorSys = 3
        elif self.sys_beam == "UP":
          self.kfactorSys = 4

        elif self.sys_choice == "DN":
          self.kfactorSys = 5
        elif self.sys_choice == "UP":
          self.kfactorSys = 6

        elif self.sys_pdf == "DN":
          self.kfactorSys = 16
        elif self.sys_pdf == "UP":
          self.kfactorSys = 17

        elif self.sys_pi == "DN":
          self.kfactorSys = 18
        elif self.sys_pi == "UP":
          self.kfactorSys = 19

        elif self.sys_scale_z == "DN":
          self.kfactorSys = 23
        elif self.sys_scale_z == "UP":
          self.kfactorSys = 24


    #__________________________________________________________________________
    def execute(self, weight):
        if "mc" in self.sampletype: 
          if self.nominalTree:
            lpxk = self.chain.LPXKfactorVec.at(self.kfactorSys)
            if self.key: self.store[self.key] = lpxk
            self.set_weight(lpxk*weight)

            if self.doAssert:
              assert self.chain.LPXKfactorVecNames.at(3)=="LPX_KFACTOR_BEAM_ENERGY__1down", "LPX_KFACTOR_BEAM_ENERGY__1down"
              assert self.chain.LPXKfactorVecNames.at(4)=="LPX_KFACTOR_BEAM_ENERGY__1up", "LPX_KFACTOR_BEAM_ENERGY__1up"
              assert self.chain.LPXKfactorVecNames.at(5)=="LPX_KFACTOR_CHOICE_HERAPDF20", "LPX_KFACTOR_CHOICE_HERAPDF20"
              assert self.chain.LPXKfactorVecNames.at(6)=="LPX_KFACTOR_CHOICE_NNPDF30", "LPX_KFACTOR_CHOICE_NNPDF30"
              assert self.chain.LPXKfactorVecNames.at(16)=="LPX_KFACTOR_PDF__1down", "LPX_KFACTOR_PDF__1down"
              assert self.chain.LPXKfactorVecNames.at(17)=="LPX_KFACTOR_PDF__1up", "LPX_KFACTOR_PDF__1up"
              assert self.chain.LPXKfactorVecNames.at(18)=="LPX_KFACTOR_PI__1down", "LPX_KFACTOR_PI__1down"
              assert self.chain.LPXKfactorVecNames.at(19)=="LPX_KFACTOR_PI__1up", "LPX_KFACTOR_PI__1up"
              assert self.chain.LPXKfactorVecNames.at(23)=="LPX_KFACTOR_SCALE_Z__1down", "LPX_KFACTOR_SCALE_Z__1down"
              assert self.chain.LPXKfactorVecNames.at(24)=="LPX_KFACTOR_SCALE_Z__1up", "LPX_KFACTOR_SCALE_Z__1up"
          else:
            lpxk = self.chain.LPXKfactor
            if self.key: self.store[self.key] = lpxk
            self.set_weight(lpxk*weight)            

        return True



#------------------------------------------------------------------------------                                                                                                   
class OneOrTwoBjetsSF(pyframe.core.Algorithm):
    """                                                                                                                                                                            
    OneOrTwoBjetsSF                                                                                                                                                                
    """
    #__________________________________________________________________________                                                                                                    
    def __init__(self, name="OneOrTwoBjetsSF",
            key            = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key

        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________                                                                                                     
    def initialize(self):
      pass
    #_________________________________________________________________________                                                                                                     
    def execute(self, weight):
      sf=1.0
      if "mc" in self.sampletype:
          jets = self.store['jets']
          for jet in jets:
              if jet.isFix77:
                  sf *= getattr(jet,"jvtSF").at(0)
                  sf *= getattr(jet,"SFFix77").at(0)

      if self.key:
        self.store[self.key] = sf
      return True

#------------------------------------------------------------------------------                                                                                                   
class ChargeFlipEleSF(pyframe.core.Algorithm):
    """ 
    ChargeFlipEleSF 
    """
    #__________________________________________________________________________                                                                                                      
    def __init__(self, name="ChargeFlipEleSF",
            key            = None,
            chargeFlipSF   = None,
            config_fileCHF = None,
            sys_CF         = None,
            ):

        pyframe.core.Algorithm.__init__(self, name=name)
        self.key               = key
        self.chargeFlipSF      = chargeFlipSF
        self.config_fileCHF    = config_fileCHF
        self.sys_CF            = sys_CF

        assert config_fileCHF, "Must provide a charge-flip config file!"
        assert key, "Must provide key for storing ele reco sf"
    #_________________________________________________________________________                                                                                                     
    
    def initialize(self):

      fchf = ROOT.TFile.Open(self.config_fileCHF)
      assert fchf, "Failed to open charge-flip config file: %s"%(self.config_fileCHF)

      h_etaFunc = fchf.Get("etaFunc")
      assert h_etaFunc, "Failed to get 'h_etaFunc' from %s"%(self.config_fileCHF)
      h_ptFunc = fchf.Get("ptFunc")
      assert h_ptFunc, "Failed to get 'h_ptFunc' from %s"%(self.config_fileCHF)

      h_etaRateMC = fchf.Get("MCEtaRate")
      assert h_etaRateMC, "Failed to get 'h_etaRateMC' from %s"%(self.config_fileCHF)
      h_ptRateMC = fchf.Get("MCPtRate")
      assert h_ptRateMC, "Failed to get 'h_ptRateMC' from %s"%(self.config_fileCHF)

      h_etaRateData = fchf.Get("dataEtaRate")
      assert h_etaRateData, "Failed to get 'h_etaRateData' from %s"%(self.config_fileCHF)
      h_ptRateData = fchf.Get("dataPtRate")
      assert h_ptRateData, "Failed to get 'h_ptRateData' from %s"%(self.config_fileCHF)

      self.h_etaFunc = h_etaFunc.Clone()
      self.h_ptFunc  = h_ptFunc.Clone()
      self.h_etaFunc.SetDirectory(0)
      self.h_ptFunc.SetDirectory(0)

      self.h_etaRateMC = h_etaRateMC.Clone()
      self.h_ptRateMC  = h_ptRateMC.Clone()
      self.h_etaRateMC.SetDirectory(0)
      self.h_ptRateMC.SetDirectory(0)

      self.h_etaRateData = h_etaRateData.Clone()
      self.h_ptRateData  = h_ptRateData.Clone()
      self.h_etaRateData.SetDirectory(0)
      self.h_ptRateData.SetDirectory(0)
      fchf.Clone()

    #_________________________________________________________________________                                                                                                       
    def execute(self, weight):
        sf=1.0
 
        if "mc" in self.sampletype:
            electrons = self.store['electrons_loose']
            for ele in electrons:
                if self.chargeFlipSF:
                    ptBin  = self.h_ptFunc.FindBin( ele.tlv.Pt()/GeV )
                    etaBin = self.h_etaFunc.FindBin( abs(ele.caloCluster_eta ) )
                    if ptBin==self.h_ptFunc.GetNbinsX()+1:
                        ptBin -= 1 
                    if ele.electronType() in [2,3]:
                        if self.sys_CF == None:
                            sf *= self.h_ptFunc.GetBinContent( ptBin ) * self.h_etaFunc.GetBinContent( etaBin )                
                        elif self.sys_CF == "UP":            
                            sf *= (self.h_ptFunc.GetBinContent( ptBin )+self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )+self.h_etaFunc.GetBinError( etaBin ))               
                        elif self.sys_CF == "DN":
                            sf *= (self.h_ptFunc.GetBinContent( ptBin )-self.h_ptFunc.GetBinError( ptBin )) * (self.h_etaFunc.GetBinContent( etaBin )-self.h_etaFunc.GetBinError( etaBin ))
                    elif ele.electronType() in [1]:
                        probMC   = 0
                        probData = 0
                        if self.sys_CF == None:
                            probMC   = self.h_ptRateMC.GetBinContent( ptBin )   * self.h_etaRateMC.GetBinContent( etaBin )
                            probData = self.h_ptRateData.GetBinContent( ptBin ) * self.h_etaRateData.GetBinContent( etaBin )
                        elif self.sys_CF == "UP":
                            probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  -self.h_ptRateMC.GetBinError( ptBin )) *  (self.h_etaRateMC.GetBinContent( etaBin )  -self.h_etaRateMC.GetBinError( etaBin ))
                            probData = (self.h_ptRateData.GetBinContent( ptBin )+self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )+self.h_etaRateData.GetBinError( etaBin ))
                        elif self.sys_CF == "DN":
                            probMC   = (self.h_ptRateMC.GetBinContent( ptBin )  +self.h_ptRateMC.GetBinError( ptBin )) * (self.h_etaRateMC.GetBinContent( etaBin )  +self.h_etaRateMC.GetBinError( etaBin ))
                            probData = (self.h_ptRateData.GetBinContent( ptBin )-self.h_ptRateData.GetBinError( ptBin )) * (self.h_etaRateData.GetBinContent( etaBin )-self.h_etaRateData.GetBinError( etaBin ))
                        sf *= ( 1 - probData )/( 1 - probMC )
    
        if self.key:
          self.store[self.key] = sf
        return True

#------------------------------------------------------------------------------                                                                                                   
class EleTrigSF(pyframe.core.Algorithm):
    """
    Implementation of electron trigger scale factors

    """
    #__________________________________________________________________________
    def __init__(self, name="EleTrigSF",
            trig_list      = None,
            key            = None,
            scale           = None,
            sys_trig       = None,     
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.trig_list         = trig_list
        self.key               = key
        self.scale             = scale
        self.sys_trig          = sys_trig

        assert key, "Must provide key for storing ele trig sf"
    #_________________________________________________________________________
    def initialize(self):

      self.isoLevels = [
      "",
      "_isolLoose",
      "_isolTight",
      ]
      self.IDLevels = [
      "LooseAndBLayerLLH",
      "MediumLLH",
      "TightLLH",
      ]
      if not self.trig_list: self.trig_list = "HLT_2e17lhloose"

      
      self.trig_sys = 0
      if self.sys_trig == "UP":
        self.trig_sys = 2
      elif self.sys_trig == "DN":
        self.trig_sys = 1


    #_________________________________________________________________________
    def execute(self, weight):

      sf = 1.0
      electrons = self.store['electrons_loose']

      if(len(electrons)==0 or "mc" not in self.sampletype):
          if self.key:
              self.store[self.key] = sf
          return True

      #first loop on electrons to see if the pass the tight criteria requirements
      is_TightOrLoose = []
      for ele in electrons:
          if(ele.LHMedium and ele.isIsolated_Loose):
              is_TightOrLoose.append(1)
          else: is_TightOrLoose.append(0)
                 
      SFTight = "TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_MediumLLH_isolLoose"
      SFLoose = "TrigEff_SF_DI_E_2015_e17_lhloose_2016_e17_lhloose_LooseAndBLayerLLH"
      EffTight = "TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_MediumLLH_isolLoose"
      EffLoose = "TrigMCEff_DI_E_2015_e17_lhloose_2016_e17_lhloose_LooseAndBLayerLLH"


      if(len(electrons)==2):
          for ele in range(len(electrons)):
              if(is_TightOrLoose[ele] ==1): sf *= getattr(electrons[0],SFTight).at(self.trig_sys)
              if(is_TightOrLoose[ele] ==0): sf *= getattr(electrons[1],SFLoose).at(self.trig_sys)

          if self.key:
              self.store[self.key] = sf
          return True

      elif(len(electrons)==3):
          P2passD  = 0
          P2passMC = 0
          P3passD  = 1
          P3passMC = 1
          for pair in itertools.combinations(electrons,2) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * (1-e3*SF3)
              combinationProbMC = 1 # e1     * e2     * (1-e3    )
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(self.trig_sys)*getattr(elePass,EffTight).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffTight).at(self.trig_sys)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffLoose).at(self.trig_sys)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(self.trig_sys)**getattr(elePass,EffTight).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(self.trig_sys)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(self.trig_sys)
                      break
              P2passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
              P2passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
          for ele in electrons:
              if ele.LHMedium and ele.isIsolated_Loose:
                  P3passD  *= getattr(ele,SFTight).at(self.trig_sys)*getattr(elePass,EffTight).at(self.trig_sys)
                  P3passMC *= getattr(ele,EffTight).at(self.trig_sys)
              else:
                  P3passD  *= getattr(ele,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys)
                  P3passMC *= getattr(ele,EffLoose).at(self.trig_sys)
           
          if(P2passD==0 and P2passMC==0 and P3passD==0 and P3passMC ==0):
              print "No SF available for these leptons"
              sf == 0
              
          else : sf = (P2passD+P3passD)/(P2passMC+P3passMC)
          if self.key: 
              self.store[self.key] = sf
          return True

      elif(len(electrons)==4):
          P2passD  = 0
          P2passMC = 0
          P3passD  = 1
          P3passMC = 1
          P4passD  = 1
          P4passMC = 1
          for pair in itertools.combinations(electrons,2) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * (1-e3*SF3) * (1-e4*SF4)
              combinationProbMC = 1 # e1     * e2     * (1-e3    ) * (1-e4    )
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(self.trig_sys)*getattr(elePass,EffTight).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffTight).at(self.trig_sys)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffLoose).at(self.trig_sys)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(self.trig_sys)**getattr(elePass,EffTight).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(self.trig_sys)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(self.trig_sys)
                      break
              P2passD  += combinationProbD   # a*b*(1-c)*(1-d) + a*c*(1-b)*(1-d) + b*c*(1-d)*(1-a) etc. 
              P2passMC += combinationProbMC  # a*b*(1-c)*(1-d) + a*c*(1-b)*(1-d) + b*c*(1-d)*(1-a) + etc
          for pair in itertools.combinations(electrons,3) :
              combinationProbD  = 1 # e1*SF1 * e2*SF2 * e3*SF3 * (1-e4*SF4)
              combinationProbMC = 1 # e1     * e2     * e3     * (1-e4)
              for eleFail in electrons:
                  if eleFail not in pair:
                      for elePass in pair:
                          if elePass.LHMedium and elePass.isIsolated_Loose:
                              combinationProbD  *= getattr(elePass,SFTight).at(self.trig_sys)*getattr(elePass,EffTight).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffTight).at(self.trig_sys)
                          else:
                              combinationProbD  *= getattr(elePass,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys)
                              combinationProbMC *= getattr(elePass,EffLoose).at(self.trig_sys)
                      if eleFail.LHMedium and eleFail.isIsolated_Loose:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFTight).at(self.trig_sys)**getattr(elePass,EffTight).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffTight).at(self.trig_sys)                  
                      else:
                          combinationProbD  *= 1 - ( getattr(eleFail,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys))
                          combinationProbMC *= 1 -   getattr(eleFail,EffLoose).at(self.trig_sys)
                      break
              P3passD  += combinationProbD   # a*b*(1-c) + a*c*(1-b) + b*c*(1-d) 
              P3passMC += combinationProbMC  # a*b*(1-c) + a*c*(1-b) + b*c*(1-d)
          for ele in electrons:
              if ele.LHMedium and ele.isIsolated_Loose:
                  P4passD  *= getattr(ele,SFTight).at(self.trig_sys)*getattr(elePass,EffTight).at(self.trig_sys)
                  P4passMC *= getattr(ele,EffTight).at(self.trig_sys)
              else:
                  P4passD  *= getattr(ele,SFLoose).at(self.trig_sys)*getattr(elePass,EffLoose).at(self.trig_sys)
                  P4passMC *= getattr(ele,EffLoose).at(self.trig_sys)
           
          if(P2passD==0 and P2passMC==0 and P3passD==0 and P3passMC ==0 and P4passMC==0 and P4passD==0):
              print "No sf available for this event"
              sf == 0
              
          else : sf = (P2passD+P3passD+P4passD)/(P2passMC+P3passMC+P4passMC)
          if self.key: 
              self.store[self.key] = sf
          return True



#------------------------------------------------------------------------------
class MuTrigSF(pyframe.core.Algorithm):
    """
    Muon trigger scale factor (OR of signle muon triggers)
    """
    #__________________________________________________________________________
    def __init__(self, name="MuTrigSF",
            trig_list   = None,
            match_all   = False,
            mu_iso      = None,
            mu_reco     = None,
            key         = None,
            sys_trig    = None,
            ):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.trig_list   = trig_list # if for some reason a different list is needed
        self.match_all   = match_all
        self.mu_iso      = mu_iso
        self.mu_reco     = mu_reco
        self.key         = key
        self.sys_trig    = sys_trig

        assert key, "Must provide key for storing mu reco sf"
    #_________________________________________________________________________
    def initialize(self):
      
        self.trig_sys=0
        if self.sys_trig == "UPSTAT":
            self.trig_sys = 2
        elif self.sys_trig == "UPSYS":
            self.trig_sys = 4
        elif self.sys_trig == "DNSTAT":
            self.trig_sys = 1
        elif self.sys_trig == "DNSYS":
            self.trig_sys = 3

        if not self.mu_reco:      self.mu_reco = "Loose"
        if not self.mu_iso:       self.mu_iso  = "FixedCutTightTrackOnly"
      
        if "Not" in self.mu_iso:  self.mu_iso  = "Loose"
        if "Not" in self.mu_reco: self.mu_reco = "Loose"

        if not self.trig_list: self.trig_list = self.store["reqTrig"]

    #_________________________________________________________________________
    def execute(self, weight):
        trig_sf=1.0
        if "mc" in self.sampletype: 
          muons = self.store['muons']
          
          eff_data_chain = 1.0 
          eff_mc_chain   = 1.0
          
          for i,m in enumerate(muons):
          
            eff_data_muon = 1.0 
            eff_mc_muon   = 1.0

            if m.isTruthMatchedToMuon: 
              for trig in self.trig_list:
                
                sf_muon  = getattr(m,"_".join(["TrigEff","SF",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at(self.trig_sys)
                eff_muon = getattr(m,"_".join(["TrigMCEff",trig,"Reco"+self.mu_reco,"Iso"+self.mu_iso])).at(0)
                
                # EXOT12 for v1 ntuples
                #sf_muon  = getattr(m,"_".join(["TrigEff","SF",self.mu_reco,self.mu_iso])).at(0)
                #eff_muon = getattr(m,"_".join(["TrigMCEff",self.mu_reco,self.mu_iso])).at(0)
                
                eff_data_muon *= 1 - sf_muon * eff_muon
                eff_mc_muon   *= 1 - eff_muon
              
              eff_data_muon = ( 1 - eff_data_muon )
              eff_mc_muon   = ( 1 - eff_mc_muon )
              
              if self.match_all:
                eff_data_chain *= eff_data_muon
                eff_mc_chain   *= eff_mc_muon
              else:
                eff_data_chain *= 1. - eff_data_muon
                eff_mc_chain   *= 1. - eff_mc_muon
          
          if not self.match_all: 
            eff_data_chain = ( 1 - eff_data_chain )
            eff_mc_chain   = ( 1 - eff_mc_chain )
          
          if eff_mc_chain > 0:
            trig_sf = eff_data_chain / eff_mc_chain
          
          #if self.scale: pass
       
        if self.key: 
          self.store[self.key] = trig_sf
        return True

#------------------------------------------------------------------------------
class EffCorrPair(pyframe.core.Algorithm):
    """
    Applies trigger efficiency correction for muon pairs
    """
    #__________________________________________________________________________
    def __init__(self, name="EffCorrector",
            config_file     = None,
            mu_lead_type    = None,
            mu_sublead_type = None,
            key             = None,
            scale           = None
            ):
        pyframe.core.Algorithm.__init__(self,name=name)
        self.config_file     = config_file
        self.mu_lead_type    = mu_lead_type
        self.mu_sublead_type = mu_sublead_type
        self.key             = key
        self.scale           = scale
        
        assert config_file, "Must provide config file!"
        assert key, "Must provide key for storing fakefactor"
    #_________________________________________________________________________
    def initialize(self):
        f = ROOT.TFile.Open(self.config_file)
        assert f, "Failed to open config file for efficiency correction: %s"%(self.config_file)

        g_loose_eff = f.Get("g_loose_eff")
        g_tight_eff = f.Get("g_tight_eff")
        
        assert self.mu_lead_type in ["Loose","Tight"], "mu_lead_type not Loose or Tight"
        assert self.mu_sublead_type in ["Loose","Tight"], "mu_sublead_type not Loose or Tight"
        
        assert g_loose_eff, "Failed to get 'g_loose_eff' from %s"%(self.config_file)
        assert g_tight_eff, "Failed to get 'g_tight_eff' from %s"%(self.config_file)
        
        self.g_loose_eff = g_loose_eff.Clone()
        self.g_tight_eff = g_tight_eff.Clone()
        f.Close()
    #_________________________________________________________________________
    def execute(self, weight):
        #muons = self.store['muons']

        # check particular quality 
        # of muons in the SS pair
        muons = [self.store['muon1'],self.store['muon2']]
         
        if len(self.store['muons'])>2:
          for i in xrange(3,len(self.store['muons'])+1):
            muons.append(self.store['muon%d'%i])

        mu_lead    = muons[0]
        mu_sublead = muons[1]
        
        pt_lead    = mu_lead.tlv.Pt()/GeV  
        pt_sublead = mu_sublead.tlv.Pt()/GeV  
       
        g_lead_eff    = None
        g_sublead_eff = None

        if self.mu_lead_type == "Loose":      g_lead_eff = self.g_loose_eff
        elif self.mu_lead_type == "Tight":    g_lead_eff = self.g_tight_eff
        
        if self.mu_sublead_type == "Loose":   g_sublead_eff = self.g_loose_eff
        elif self.mu_sublead_type == "Tight": g_sublead_eff = self.g_tight_eff

        eff_lead = 0.0
        eff_sublead = 0.0
        eff_lead_tight = 0.0
        eff_sublead_tight = 0.0

        for ibin_lead in xrange(1,g_lead_eff.GetN()):
          for ibin_sublead in xrange(1,g_sublead_eff.GetN()):
          
            edlow_lead = g_lead_eff.GetX()[ibin_lead] - g_lead_eff.GetEXlow()[ibin_lead]
            edhi_lead  = g_lead_eff.GetX()[ibin_lead] + g_lead_eff.GetEXhigh()[ibin_lead]
            if pt_lead>=edlow_lead and pt_lead<edhi_lead: 
              eff_lead = g_lead_eff.GetY()[ibin_lead]
              eff_lead_tight = self.g_tight_eff.GetY()[ibin_lead]
              
            edlow_sublead = g_sublead_eff.GetX()[ibin_sublead] - g_sublead_eff.GetEXlow()[ibin_sublead]
            edhi_sublead  = g_sublead_eff.GetX()[ibin_sublead] + g_sublead_eff.GetEXhigh()[ibin_sublead]
            if pt_sublead>=edlow_sublead and pt_sublead<edhi_sublead: 
              eff_sublead = g_sublead_eff.GetY()[ibin_sublead]
              eff_sublead_tight = self.g_tight_eff.GetY()[ibin_sublead]
         
         
        ineff_others = 1.0 

        for m in muons[2:]:
          muon_is_loose    = bool(not m.isIsolated_FixedCutTightTrackOnly and m.trkd0sig<10.)
          muon_is_tight    = bool(m.isIsolated_FixedCutTightTrackOnly and m.trkd0sig<3.)
          
          pt_other    = m.tlv.Pt()/GeV  
          eff_other   = 0.0
          g_other_eff = None
          
          if muon_is_loose:
            g_other_eff = self.g_loose_eff
          elif muon_is_tight:
            g_other_eff = self.g_tight_eff
          else: continue
         
          for ibin_other in xrange(1,g_other_eff.GetN()):
            
              edlow_other = g_other_eff.GetX()[ibin_other] - g_other_eff.GetEXlow()[ibin_other]
              edhi_other  = g_other_eff.GetX()[ibin_other] + g_other_eff.GetEXhigh()[ibin_other]
              if pt_other>=edlow_other and pt_other<edhi_other: 
                eff_other = g_other_eff.GetY()[ibin_other]
                
              ineff_others *= (1 - eff_other)
        
        num_pair_eff = 1 - ( 1 - eff_lead_tight ) * ( 1 - eff_sublead_tight ) * ineff_others
        den_pair_eff = 1 - ( 1 - eff_lead ) * ( 1 - eff_sublead ) * ineff_others
       
       
        corr_eff = 1.0
        if den_pair_eff != 0:
          corr_eff =  num_pair_eff / den_pair_eff

        # error bars are asymmetric
        #eff_up_mu = self.g_ff.GetEYhigh()[ibin_mu]
        #eff_dn_mu = self.g_ff.GetEYlow()[ibin_mu]
        
        if self.scale == 'up': pass
        if self.scale == 'dn': pass
       
        if self.key: 
          self.store[self.key] = corr_eff

        return True


# EOF
