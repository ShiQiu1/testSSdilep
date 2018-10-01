#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import os
from itertools import combinations
from copy import copy, deepcopy
from types import MethodType

import pyframe
import ROOT
from array import array

GeV = 1000.0

import logging
log = logging.getLogger(__name__)

def fatal(message):
    sys.exit("Fatal error in %s: %s" % (__file__, message))

#------------------------------------------------------------------------------
class BuildTrigConfig(pyframe.core.Algorithm):
    """
    Algorithm to configure the trigger chain
    """
    #__________________________________________________________________________
    def __init__(self, 
          cutflow           = None,
          required_triggers = None,
          key               = None):
        pyframe.core.Algorithm.__init__(self, name="TrigConfig", isfilter=True)
        self.cutflow           = cutflow
        self.required_triggers = required_triggers
        self.key               = key
    
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize trigger config for %s...' % self.key)

    #__________________________________________________________________________
    def execute(self, weight):
        
      assert len(self.chain.passedTriggers) == len(self.chain.triggerPrescales), "ERROR: # passed triggers != # trigger prescales !!!"
      
      if not "reqTrig" in self.store.keys():
        self.store["reqTrig"] = self.required_triggers
      
      # this dictionary stores 
      # the prescales of passed triggers
      if not "passTrig" in self.store.keys():
        self.store["passTrig"] = {}
        for trig,presc in zip(self.chain.passedTriggers,self.chain.triggerPrescales):
          self.store["passTrig"][trig] = presc

      mGeV = GeV * 1.03

      #Adding to the store the electron trigger
      
      """
      The following lines build a trigger dictionary
      necessary for trigger matching. 

      """
      # -----
      #mixed flavour triggers for e/mu selection
      # -----
      if self.key == "leptons_dilepton": return True

      # -----
      # muons
      # -----
      if self.key == "muons" or self.key == "leptons":
        self.store["SingleMuTrigIndex"] = {}  # for trigger matching
        self.store["SingleMuTrigSlice"] = {}  # for prescale slicing

        # the mu_listTrigChains is filled in the ntuple with 
        # single-muon triggers if # muons>0. If more 
        # than one muon exists skip repetitions
        for i,trig in enumerate(self.chain.muon_listTrigChains):
          if trig in self.store["SingleMuTrigIndex"].keys(): continue
          self.store["SingleMuTrigIndex"][trig] = i

        # the slice has to be built using the required triggers ...
        """
        muons_thr = [1000 * GeV]
        for trig in self.store["reqTrig"]:
          for thr in trig.split("_"):
            if thr.startswith("mu"): 
              muons_thr.append( float( thr.replace("mu","") ) * mGeV )  
        muons_thr.sort() 
        
        for ithr in xrange(len(muons_thr) - 1):
          for trig in self.store["SingleMuTrigIndex"].keys():
            for thr in trig.split("_"):
              if thr.startswith("mu"):
                trig_thr = float( thr.replace("mu","") ) * mGeV
                if trig_thr>= muons_thr[ithr] and trig_thr < muons_thr[ithr+1]:
                  self.store["SingleMuTrigSlice"][trig] = (muons_thr[ithr],muons_thr[ithr+1])
        """
      
      # ... by hand for now 
      self.store["SingleMuTrigSlice"]["HLT_mu26_ivarmedium"] = (28*GeV,51*GeV)
      self.store["SingleMuTrigSlice"]["HLT_mu50"] = (51*GeV,10000*GeV)
      
      
      # ---------
      # electrons
      # ---------
      if self.key == "electrons" or self.key == "leptons":
        self.store["SingleEleTrigIndex"] = {}  # for trigger matching
        self.store["SingleEleTrigSlice"] = {}  # for prescale slicing

        # the el_listTrigChains is filled in the ntuple with 
        # single-electron triggers if # electrons>0. If more 
        # than one electrons exists skip repetitions
        for i,trig in enumerate(self.chain.el_listTrigChains):
          if trig in self.store["SingleEleTrigIndex"].keys(): continue
          self.store["SingleEleTrigIndex"][trig] = i

        # the slice has to be built using the required triggers!
        electrons_thr = [1000 * GeV]
        for trig in self.store["reqTrig"]:
          for thr in trig.split("_"):
            if thr.startswith("e"): 
              electrons_thr.append( float( thr.replace("e","") ) * dGeV )  
        electrons_thr.sort() 
        
        for ithr in xrange(len(electrons_thr) - 1):
          for trig in self.store["SingleEleTrigIndex"].keys():
            for thr in trig.split("_"):
              if thr.startswith("e"):
                trig_thr = float( thr.replace("e","") ) * GeV
                if trig_thr>= electrons_thr[ithr] and trig_thr < electrons_thr[ithr+1]:
                  self.store["SingleEleTrigSlice"][trig] = (electrons_thr[ithr],electrons_thr[ithr+1])
      
      return True

#-------------------------------------------------------------------------------
class Particle(pyframe.core.ParticleProxy):
    """
    Variables added to the particle
    """
    #__________________________________________________________________________
    def __init__(self, particle, **kwargs):
        pyframe.core.ParticleProxy.__init__(self, 
             tree_proxy = particle.tree_proxy,
             index      = particle.index,
             prefix     = particle.prefix)   
        self.particle = particle
        self.__dict__ = particle.__dict__.copy() 
    #__________________________________________________________________________
    def isMatchedToTrigChain(self):
      return self.isTrigMatched

    # https://svnweb.cern.ch/trac/atlasoff/browser/PhysicsAnalysis/MCTruthClassifier/tags/MCTruthClassifier-00-00-26/MCTruthClassifier/MCTruthClassifierDefs.h
    # https://twiki.cern.ch/twiki/bin/view/AtlasProtected/MCTruthClassifier 
    #__________________________________________________________________________
    def isTrueNonIsoMuon(self):
        matchtype = self.truthType in [5,7,8]
        return self.isTruthMatchedToMuon and matchtype
    #__________________________________________________________________________
    def isTrueIsoMuon(self):   
        matchtype = self.truthType in [6]
        return self.isTruthMatchedToMuon and matchtype

    #__________________________________________________________________________
    def electronType(self):
      trueCharge = -self.firstEgMotherPdgId/11.
      chargeEval = abs(self.trkcharge - trueCharge)
      if   self.truthType==2 and self.truthOrigin in [10,12,13,14,43] and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==0 :
        return 1
      elif self.truthType==2 and self.truthOrigin in [10,12,13,14,43] and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==2 :
        return 2
      elif self.truthType==4 and self.truthOrigin== 5 and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==2 :
        return 3
      elif self.truthType==4 and self.truthOrigin== 5 and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==0 :
        return 4
      elif self.truthType==4 and self.truthOrigin== 5 and self.firstEgMotherTruthType==15 and self.firstEgMotherTruthOrigin==40 :
        return 5
      else :
        return 6

    #__________________________________________________________________________
    def isTrueIsoElectron(self):
      trueCharge = -self.firstEgMotherPdgId/11.
      chargeEval = abs(self.trkcharge - trueCharge)
      
      if   self.truthType==2 and self.truthOrigin in [10,12,13,14,43] and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==0 :
        return True
      elif self.truthType==2 and self.truthOrigin in [10,12,13,14,43] and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==2 :
        return True
      elif self.truthType==4 and self.truthOrigin== 5 and self.firstEgMotherTruthType== 2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] and chargeEval==2 :
        return True

      return False

    #__________________________________________________________________________
    def isTrueNonIsoElectron(self):
        matchtype = self.truthType in [1,3,4]
        return matchtype
    
    #__________________________________________________________________________
    def electronTypeSimple(self):
      if   self.truthType==2 and self.truthOrigin in [10,12,13,14,43] :
        return 1
      else :
        return 2

    #__________________________________________________________________________
    def electronTypeNew(self):
      if   self.firstEgMotherTruthType==2 and self.firstEgMotherTruthOrigin in [10,12,13,14,43] :
        return 1
      elif self.firstEgMotherTruthOrigin in [25,26] :
        return 2
      else :
        return 0
        
        
    def tauTrueCharge(self):
      trueCharge = -self.truthPdgId/15.
      return trueCharge
      
    def isTrueOneProngedTauFromZ(self):
      if self.isTruthMatchedToTau and self.truthOrigin == 13 and self.truthStatus == 9 : return True
      else: return False 
      
    def isTrueThreeProngedTauFromZ(self):
      if self.isTruthMatchedToTau and self.truthOrigin == 13 and self.truthStatus == 10 : return True                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      else: return False          

#------------------------------------------------------------------------------
class ParticlesBuilder(pyframe.core.Algorithm):
    #__________________________________________________________________________
    def __init__(self, name="ParticlesBuilder", key=""):
        pyframe.core.Algorithm.__init__(self, name=name)
        self.key  = key
    #__________________________________________________________________________
    def initialize(self):
        log.info('initialize single particles for %s ...' % self.key)
    #__________________________________________________________________________
    def execute(self,weight):
        self.store[self.key] = [Particle(copy(l)) for l in self.store[self.key]]

#------------------------------------------------------------------------------
class SR2ChannelFlavour(pyframe.core.Algorithm):# Class for channel categorization in SR2
    #__________________________________________________________________________
    def __init__(self,name="FlavourTagging" ):
        pyframe.core.Algorithm.__init__(self, name = name)
    #__________________________________________________________________________
    def initialize(self):
        log.info('Trying to identify SR2 flavour channel')
    #__________________________________________________________________________
    def execute(self,weight):
        pyframe.core.Algorithm.execute(self, weight)
        #Legend: 1 eeee, 2 mmmm, 3 emem, 4 eemm, 5 eeem, 6 mmem
        electrons = self.store['electrons']
        muons     = self.store['muons']
        elecoupleSS = False
        mucoupleSS  = False
        leptons = electrons + muons
        totalCharge=0

        CF=-1
        self.store["ChannelFlavour"]={}

        if(len(leptons)==4):
            for i in leptons:
                totalCharge = totalCharge + i.trkcharge

        if(len(electrons)==2):
            if((electrons[0].trkcharge * electrons[1].trkcharge)>0):
                elecoupleSS
        if(len(muons)==2):
            if((muons[0].trkcharge * muons[1].trkcharge)>0):
                mucoupleSS 

        if   (len(electrons)==4 and len(muons)==0 and totalCharge==0): CF = 0
        elif (len(electrons)==0 and len(muons)==4 and totalCharge==0): CF = 1
        elif (len(electrons)==2 and len(muons)==2 and elecoupleSS==False and mucoupleSS==False and totalCharge==0): CF = 2
        elif (len(electrons)==2 and len(muons)==2 and elecoupleSS and mucoupleSS and totalCharge==0): CF = 3
        elif (len(electrons)==3 and len(muons)==1 and totalCharge==0): CF = 4
        elif (len(electrons)==1 and len(muons)==3 and totalCharge==0): CF = 5
        elif (len(electrons)==2 and len(muons)==0) : CF = 6
        
        
        self.store["ChannelFlavour"]=CF
        
        return True

#------------------------------------------------------------------------------
class BuildLooseTightElectronsMuons(pyframe.core.Algorithm):# Building a loose container for electrons (cutting away not loose electrons from ntuples)
    #__________________________________________________________________________
    def __init__(self, 
                 name="BuildLooseTightElectronsMuons", 
                 key_electrons="electrons",
                 key_muons="muons",
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons  = key_electrons
        self.key_muons  = key_muons
    #__________________________________________________________________________
    def initialize(self):
        log.info('Building loose electron container for %s ...' % self.key_electrons)
    #__________________________________________________________________________
    def execute(self,weight):
        pyframe.core.Algorithm.execute(self, weight)
        #remove muons 
        """
        for muon in self.store[self.key_muons][:]:
            if muon.tlv.Pt() < 30*GeV or muon.trkd0sig > 10.0 or (muon.trkd0sig > 3.0 and muon.isIsolated_FixedCutTightTrackOnly):
                self.store[self.key_muons].remove(muon)
        """
        for muon in self.store[self.key_muons][:]:
            if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560): pass
            elif ("mc" in self.sampletype) and not muon.isTrueIsoMuon(): continue
            muon_is_tight = bool(muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig<3.and muon.pt>30*GeV)            
            muon_is_loose   = bool(not muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig<10. and muon.pt>30*GeV)
            if(not(muon_is_tight or muon_is_loose)): self.store[self.key_muons].remove(muon)


        # tight muons
        muons_tight = []
        for mu in self.store[self.key_muons][:]:
          if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560): pass
          elif ("mc" in self.sampletype) and not mu.isTrueIsoMuon(): continue  
          if mu.isIsolated_FixedCutTightTrackOnly and mu.trkd0sig<=3.:
            muons_tight += [mu]
        self.store['muons_tight'] = muons_tight


        # loose electrons (no iso // LooseLLH)
        electrons_loose = []
        for ele in self.store[self.key_electrons][:]:
          if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560): pass
          elif ("mc" in self.sampletype) and not ele.isTrueIsoElectron(): continue
          if ( ele.pt>30*GeV and ele.LHLoose and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5 ) :
            electrons_loose += [ele]
        self.store['electrons_loose'] = electrons_loose

        # tight electrons (isoLoose // MediumLLH)
        electrons_tight = []
        for ele in self.store[self.key_electrons][:]:
          if ("mc" in self.sampletype) and self.chain.mcChannelNumber in range(306538,306560): pass
          elif ("mc" in self.sampletype) and not ele.isTrueIsoElectron(): continue
          if ( ele.pt>30*GeV and ele.isIsolated_Loose and ele.LHMedium and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5 ) :
            electrons_tight += [ele]
        self.store['electrons_tight'] = electrons_tight


        return True       
#------------------------------------------------------------------------------
class BuildLooseElectrons(pyframe.core.Algorithm):# Building a loose container for electrons (cutting away not loose electrons from ntuples)
    #__________________________________________________________________________
    def __init__(self, 
                 name="BuildLooseElectrons", 
                 key_electrons="electrons",
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons  = key_electrons
    #__________________________________________________________________________
    def initialize(self):
        log.info('Building loose electron container for %s ...' % self.key_electrons)
    #__________________________________________________________________________
    def execute(self,weight):
        pyframe.core.Algorithm.execute(self, weight)
        electrons_loose = []
        very_loose_ele = self.store[self.key_electrons]
        
        for ele in very_loose_ele:
            if(ele.pt>30*GeV and ele.LHLoose and ele.trkd0sig<5.0 and abs(ele.trkz0sintheta)<0.5):
               electrons_loose += [ele]
        self.store['electrons_loose'] = electrons_loose
        return True     

#------------------------------------------------------------------------------
class BuildLooseAndTightMuons(pyframe.core.Algorithm):# removing from muon container those not T not L muons
    #__________________________________________________________________________
    def __init__(self, 
                 name="BuildLooseAndTightMuons", 
                 key_muons="muons",
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons  = key_muons
    #__________________________________________________________________________
    def initialize(self):
        log.info('Removing from muon store not T or L muons  %s ...' % self.key_muons)
    #__________________________________________________________________________
    def execute(self,weight):
        pyframe.core.Algorithm.execute(self, weight)
        muons = self.store[self.key_muons]
        
        for muon in muons:
            muon_is_tight = bool(muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig<3.and muon.pt>30*GeV)            
            muon_is_loose   = bool(not muon.isIsolated_FixedCutTightTrackOnly and muon.trkd0sig<10. and muon.pt>30*GeV)
            if(not(muon_is_tight or muon_is_loose)): self.store[self.key_muons].remove(muon)

        return True       

#------------------------------------------------------------------------------
class TagAndProbeVars(pyframe.core.Algorithm):
    """
    computes variables for the tag-and-probe selection
    in the di-muon channel
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'TagAndProbeVars',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        
        if len(muons)<2: 
          return True
        
        met = self.store[self.key_met]
        muon1 = muons[0] 
        muon2 = muons[1] 

        # ------------------
        # at least two muons
        # ------------------
          
        # definition of tag and probe 
        lead_mu_is_tight = bool(muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<3.)
        lead_mu_is_loose = bool(not muon1.isIsolated_FixedCutTightTrackOnly and muon1.trkd0sig<10.)

        sublead_mu_is_tight = bool(muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<3.)
        sublead_mu_is_loose = bool(not muon2.isIsolated_FixedCutTightTrackOnly and muon2.trkd0sig<10.)
       
        if lead_mu_is_tight and sublead_mu_is_tight:
          if random.randint(0,9) > 4:
            self.store['tag'] = muon1
            self.store['probe'] = muon2 
          else:
            self.store['tag'] = muon2
            self.store['probe'] = muon1 
        elif lead_mu_is_loose or sublead_mu_is_tight:
          self.store['tag'] = muon2
          self.store['probe'] = muon1
        elif sublead_mu_is_loose or lead_mu_is_tight:
          self.store['tag'] = muon1
          self.store['probe'] = muon2


        return True


#------------------------------------------------------------------------------
class ProbeVars(pyframe.core.Algorithm):
    """
    computes variables for the tag-and-probe selection
    in the di-muon channel
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'ProbeVars',
                 key_tag   = 'tag',
                 key_probe = 'probe',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        
        self.key_tag   = key_tag
        self.key_probe = key_probe
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_tag), "tag key: %s not found in store!" % (self.key_tag)
        assert self.store.has_key(self.key_probe), "probe key: %s not found in store!" % (self.key_probe)
        tag   = self.store[self.key_tag]
        probe = self.store[self.key_probe]
       
        """
        iso/pt<0.8
        ----------
        p0  = 5.66581   +/-   6.81268
        p1  = 1.25722   +/-   0.0603463 
        """
        
        p0  = 5.66581
        p1  = 1.25722

        # RMS is in GeV
        RMS = {}

        RMS["ptiso_20_25"]   = 0.0
        RMS["ptiso_25_30"]   = 12.4064460713
        RMS["ptiso_30_35"]   = 13.2433526355
        RMS["ptiso_35_40"]   = 14.4159208352
        RMS["ptiso_40_45"]   = 16.2752782594
        RMS["ptiso_45_50"]   = 18.2407633765
        RMS["ptiso_50_55"]   = 19.5622710782
        RMS["ptiso_55_60"]   = 20.7644848946
        RMS["ptiso_60_65"]   = 22.4369845476
        RMS["ptiso_65_70"]   = 24.2929719957
        RMS["ptiso_70_75"]   = 26.7638147383
        RMS["ptiso_75_80"]   = 27.4958307282
        RMS["ptiso_80_85"]   = 28.6467918032
        RMS["ptiso_85_90"]   = 30.3006145851
        RMS["ptiso_90_95"]   = 31.4212980513
        RMS["ptiso_95_100"]  = 32.3088211841
        RMS["ptiso_100_105"] = 33.1844260853
        RMS["ptiso_105_110"] = 34.7326856135
        RMS["ptiso_110_115"] = 35.2736180541
        RMS["ptiso_115_120"] = 36.4129657978
        RMS["ptiso_120_125"] = 37.4741421704
        RMS["ptiso_125_130"] = 37.7874721485
        RMS["ptiso_130_135"] = 38.557678202
        RMS["ptiso_135_140"] = 40.4975404537
        RMS["ptiso_140_145"] = 40.998314068
        RMS["ptiso_145_150"] = 42.8896945092
        RMS["ptiso_150_155"] = 43.5952011684
        RMS["ptiso_155_160"] = 44.1735072515
        RMS["ptiso_160_165"] = 45.5866562887
        RMS["ptiso_165_170"] = 47.524117093
        RMS["ptiso_170_175"] = 44.5405330826
        RMS["ptiso_175_180"] = 48.3866372102
        RMS["ptiso_180_185"] = 52.0070717859
        RMS["ptiso_185_190"] = 47.744819892
        RMS["ptiso_190_195"] = 50.5839599775
        RMS["ptiso_195_200"] = 54.7332840655
        RMS["ptiso_200_205"] = 53.1491008055
        RMS["ptiso_205_210"] = 52.2524439685
        RMS["ptiso_210_215"] = 54.2499328095
        RMS["ptiso_215_220"] = 55.2824187879
        RMS["ptiso_220_225"] = 57.1261788076
        RMS["ptiso_225_230"] = 53.3562019687
        RMS["ptiso_230_235"] = 63.8959744557
        RMS["ptiso_235_240"] = 58.3227138415
        RMS["ptiso_240_245"] = 62.1696165824
        RMS["ptiso_245_250"] = 60.1443277898
        RMS["ptiso_250_255"] = 43.3303155178
        RMS["ptiso_255_260"] = 49.5807605407
        RMS["ptiso_260_265"] = 63.1491729748
        RMS["ptiso_265_270"] = 66.1689375705
        RMS["ptiso_270_275"] = 81.6534137744
        RMS["ptiso_275_280"] = 83.7920957755
        RMS["ptiso_280_285"] = 45.3639772014
        RMS["ptiso_285_290"] = 74.506656773
        RMS["ptiso_290_295"] = 69.0819259747
        RMS["ptiso_295_300"] = 56.9806508594
        RMS["ptiso_300_305"] = 50.6671197602
        RMS["ptiso_305_310"] = 71.6676212378
        RMS["ptiso_310_315"] = 62.3832400493
        RMS["ptiso_315_320"] = 94.7307677967
        
        probe_ptiso = ( probe.tlv.Pt() + probe.ptvarcone30 ) / GeV

        probe_RMS = 94.7307677967 # last bin!
        
        for k,v in RMS.iteritems():
          if probe_ptiso >= float(k.split("_")[1]) and probe_ptiso < float(k.split("_")[2]):
            probe_RMS = v

        self.store["probe_ujet_pt"] =  p1 * probe_ptiso + p0 + random.gauss(0.,probe_RMS)

        return True



#------------------------------------------------------------------------------
class DiJetVars(pyframe.core.Algorithm):
          
    """
    computes variables for the di-jet selection used for
    muon fake-factor measurement
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'VarsAlg',
                 key_muons = 'muons',
                 key_jets  = 'jets',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_jets = key_jets
        self.key_met = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        met = self.store[self.key_met]
        jets = self.store[self.key_jets]
        
        # -------------------------
        # at least a muon and a jet
        # -------------------------
        
        if bool(len(jets)) and bool(len(muons)):
          self.store['mujet_dphi'] = muons[0].tlv.DeltaPhi(jets[0].tlv)
          scdphi = 0.0
          scdphi += ROOT.TMath.Cos(met.tlv.Phi() - muons[0].tlv.Phi())
          scdphi += ROOT.TMath.Cos(met.tlv.Phi() - jets[0].tlv.Phi())
          self.store['scdphi'] = scdphi
        
        return True



#------------------------------------------------------------------------------
class DiMuVars(pyframe.core.Algorithm):
    """
    computes variables for the di-muon selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiMuVars',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]
        electrons = self.store['electrons']
        met = self.store[self.key_met]
        
        # ------------------
        # at least two muons
        # ------------------
        
        # dict containing pair 
        # and significance
        ss_pairs = {} 
        if len(muons)>=2:
          
          for p in combinations(muons,2):
            if p[0].trkcharge * p[1].trkcharge > 0.:
              ss_pairs[p] = p[0].trkd0sig + p[1].trkd0sig 
          
          max_sig  = 1000.
          for pair,sig in ss_pairs.iteritems():
            if sig < max_sig: 
              if pair[0].tlv.Pt() > pair[1].tlv.Pt():
                self.store['muon1'] = pair[0]
                self.store['muon2'] = pair[1]
              else: 
                self.store['muon1'] = pair[1]
                self.store['muon2'] = pair[0]
              max_sig = sig 
        
        if ss_pairs:
          muon1 = self.store['muon1'] 
          muon2 = self.store['muon2'] 
        
          self.store['charge_product'] = muon2.trkcharge*muon1.trkcharge
          self.store['charge_sum']     = muon1.trkcharge + muon2.trkcharge
          self.store['mVis']           = (muon2.tlv+muon1.tlv).M()
          self.store['muons_dphi']     = muon2.tlv.DeltaPhi(muon1.tlv)
          self.store['muons_deta']     = muon2.tlv.Eta()-muon1.tlv.Eta()
          self.store['muons_dR']       = math.sqrt(self.store['muons_dphi']**2 + self.store['muons_deta']**2)
          self.store['muons_pTH']            = (muon2.tlv+muon1.tlv).Pt()
          
          self.store['nleptons']       = self.chain.nmuon + self.chain.nel
          
          leptons = muons + electrons
          
          if len(leptons) == 2:
            lep1T = ROOT.TLorentzVector()
            lep1T.SetPtEtaPhiM( leptons[0].tlv.Pt(), 0., leptons[0].tlv.Phi(), leptons[0].tlv.M() )
            lep2T = ROOT.TLorentzVector()
            lep2T.SetPtEtaPhiM( leptons[1].tlv.Pt(), 0., leptons[1].tlv.Phi(), leptons[1].tlv.M() )
            
            self.store['mTTot']        = (lep1T + lep2T + met.tlv).M()
            self.store['mVisTot']      = (leptons[0].tlv + leptons[1].tlv).M()
          
          if len(leptons) == 3:
            lep1T = ROOT.TLorentzVector()
            lep1T.SetPtEtaPhiM( leptons[0].tlv.Pt(), 0., leptons[0].tlv.Phi(), leptons[0].tlv.M() )
            lep2T = ROOT.TLorentzVector()
            lep2T.SetPtEtaPhiM( leptons[1].tlv.Pt(), 0., leptons[1].tlv.Phi(), leptons[1].tlv.M() )
            lep3T = ROOT.TLorentzVector()
            lep3T.SetPtEtaPhiM( leptons[2].tlv.Pt(), 0., leptons[2].tlv.Phi(), leptons[2].tlv.M() )
            
            self.store['mTTot']        = (lep1T + lep2T + lep3T + met.tlv).M()
            self.store['mVisTot']      = (leptons[0].tlv + leptons[1].tlv + leptons[2].tlv).M()
          
          if len(leptons) == 4:
            lep1T = ROOT.TLorentzVector()
            lep1T.SetPtEtaPhiM( leptons[0].tlv.Pt(), 0., leptons[0].tlv.Phi(), leptons[0].tlv.M() )
            lep2T = ROOT.TLorentzVector()
            lep2T.SetPtEtaPhiM( leptons[1].tlv.Pt(), 0., leptons[1].tlv.Phi(), leptons[1].tlv.M() )
            lep3T = ROOT.TLorentzVector()
            lep3T.SetPtEtaPhiM( leptons[2].tlv.Pt(), 0., leptons[2].tlv.Phi(), leptons[2].tlv.M() )
            lep4T = ROOT.TLorentzVector()
            lep4T.SetPtEtaPhiM( leptons[3].tlv.Pt(), 0., leptons[3].tlv.Phi(), leptons[3].tlv.M() )
            
            self.store['mTTot']        = (lep1T + lep2T + lep3T + lep4T + met.tlv).M()
            self.store['mVisTot']      = (leptons[0].tlv + leptons[1].tlv + leptons[2].tlv + leptons[3].tlv).M()
        
        # puts additional muons in the store
        if ss_pairs and len(muons)>2:
           i = 2
           for m in muons:
             if m==self.store['muon1'] or m==self.store['muon2']: continue
             i = i + 1
             self.store['muon%d'%i] = m

        return True

#------------------------------------------------------------------------------
class DiEleVars(pyframe.core.Algorithm):
    """
    computes variables for the di-electron selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiEleVars',
                 key_electrons = 'electrons_loose',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        electrons = self.store[self.key_electrons]
        met = self.store[self.key_met]
        
        # -----------------------
        # at least two electrons
        # -----------------------
        
        # dict containing pair 
        # and significance
        ss_pairs = {} 
        if len(electrons)>=2:
          
          for p in combinations(electrons,2):
            if p[0].trkcharge * p[1].trkcharge > 0.:
              ss_pairs[p] = p[0].trkd0sig + p[1].trkd0sig 
          
          max_sig  = 1000.
          for pair,sig in ss_pairs.iteritems():
            if sig < max_sig: 
              if pair[0].tlv.Pt() > pair[1].tlv.Pt():
                self.store['ele1'] = pair[0]
                self.store['ele2'] = pair[1]
              else: 
                self.store['ele1'] = pair[1]
                self.store['ele2'] = pair[0]
              max_sig = sig 
        
        if ss_pairs:
          ele1 = self.store['ele1'] 
          ele2 = self.store['ele2'] 
          ele1T = ROOT.TLorentzVector()
          ele1T.SetPtEtaPhiM( ele1.tlv.Pt(), 0., ele1.tlv.Phi(), ele1.tlv.M() )
          ele2T = ROOT.TLorentzVector()
          ele2T.SetPtEtaPhiM( ele2.tlv.Pt(), 0., ele2.tlv.Phi(), ele2.tlv.M() )
        
          self.store['charge_product'] = ele2.trkcharge*ele1.trkcharge
          self.store['mVis']           = (ele2.tlv+ele1.tlv).M()
          self.store['mTtot']          = (ele1T + ele2T + met.tlv).M()  
          self.store['electrons_dphi']       = ele2.tlv.DeltaPhi(ele1.tlv)
          self.store['electrons_deta']       = ele2.tlv.Eta()-ele1.tlv.Eta()
         
        # puts additional electrons in the store
        if ss_pairs and len(electrons)>2:
           i = 2
           for e in electrons:
             if e==self.store['ele1'] or e==self.store['ele2']: continue
             i = i + 1
             self.store['ele%d'%i] = e

        return True
        
#------------------------------------------------------------------------------
class DiEle_chargeflip_Vars(pyframe.core.Algorithm):
    """
    computes variables for any-sign di-electron selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'ASDiEleVars',
                 key_electrons = 'electrons_loose',
                 key_met   = 'met_trk',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        electrons = self.store[self.key_electrons]
        met = self.store[self.key_met]
        
        
     
        
        # -----------------------
        # Exactly two electrons
        # -----------------------
        
        #Put leading and subleading electron in order
         
        if len(electrons)==2:
          
          if electrons[0].tlv.Pt() > electrons[0].tlv.Pt():
                self.store['ele1'] = electrons[0]
                self.store['ele2'] = electrons[1]
          else: 
                self.store['ele1'] = electrons[1]
                self.store['ele2'] = electrons[0]
               
        
        
          ele1 = self.store['ele1'] 
          ele2 = self.store['ele2'] 
          ele1T = ROOT.TLorentzVector()
          ele1T.SetPtEtaPhiM( ele1.tlv.Pt(), ele1.tlv.Eta(), ele1.tlv.Phi(), ele1.tlv.M() )
          ele2T = ROOT.TLorentzVector()
          ele2T.SetPtEtaPhiM( ele2.tlv.Pt(), ele2.tlv.Eta(), ele2.tlv.Phi(), ele2.tlv.M() )
          
          #********   Create charge flip variables    ************
          
          pt_bins  = [30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200., 400.] 
          eta_bins = [0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
          tot_bins = len(pt_bins)*len(pt_bins)*(len(eta_bins)-1)*(len(eta_bins)-1)
          
          self.store['pt_bins']= pt_bins
          self.store['eta_bins']= eta_bins
          self.store['tot_bins']= tot_bins
          
          ptbin1 = digitize( ele1.tlv.Pt()/GeV, pt_bins )
          ptbin2 = digitize( ele2.tlv.Pt()/GeV, pt_bins )
          
          etabin1 = digitize( abs(ele1.caloCluster_eta), eta_bins )
          etabin2 = digitize( abs(ele2.caloCluster_eta), eta_bins )
          
          assert ptbin1!=0 and ptbin2!=0 and etabin1!=0 and etabin2!=0 #"bins shouldn't be 0"
          
          # encode pt1, pt2, eta1, eta2 into 1D bins given pt_bins and eta_bins
          CFtotBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          
          #self.h_chargeFlipHist = self.hist('h_chargeFlipHist', "ROOT.TH1F('$', ';pt: "+str(len(pt_bins))+" eta: "+str(len(eta_bins)-1)+";Events',"+str(tot_bins)+",0,"+str(tot_bins)+")", dir=EVT)
          
          #********    Store all variables    ****************
        
          self.store['charge_product'] = ele2.trkcharge*ele1.trkcharge
          self.store['mVis']           = (ele2.tlv+ele1.tlv).M()
          self.store['mTtot']          = (ele1T + ele2T + met.tlv).M()  
          self.store['electrons_dphi'] = ele2.tlv.DeltaPhi(ele1.tlv)
          self.store['electrons_deta'] = ele2.tlv.Eta()-ele1.tlv.Eta()
          
          self.store['CFtotBin']			 = CFtotBin
         
        return True
        
class DiTau_chargeflip_Vars(pyframe.core.Algorithm):
    """
    computes variables for di-tau CF selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'ASDiTauVars',
                 key_electrons = 'electrons',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 key_taus = 'taus'
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_muons = key_muons
        self.key_met   = key_met
        self.key_taus = key_taus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_taus), "Taus key: %s not found in store!" % (self.key_electrons)
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        
        
     
        
        # -----------------------
        # Exactly two tau
        # -----------------------
        
        #Put leading and subleading electron in order
         
        if len(taus)==2:
          
          if taus[0].tlv.Pt() > taus[0].tlv.Pt():                                                       # Order the leading and subleading
                self.store['tau1'] = taus[0]
                self.store['tau2'] = taus[1]
          else: 
                self.store['tau1'] = taus[1]
                self.store['tau2'] = taus[0]
               
        
        
          tau1 = self.store['tau1'] 
          tau2 = self.store['tau2'] 
          tau1T = ROOT.TLorentzVector()
          tau1T.SetPtEtaPhiM( tau1.tlv.Pt(), tau1.tlv.Eta(), tau1.tlv.Phi(), tau1.tlv.M() )
          tau2T = ROOT.TLorentzVector()
          tau2T.SetPtEtaPhiM( tau2.tlv.Pt(), tau2.tlv.Eta(), tau2.tlv.Phi(), tau2.tlv.M() )
          
          #********   Create charge flip variables    ************
          
          #pt_bins  = [20., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200.] 
          #eta_bins = [0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
          #pt_bins  = [20., 25., 35, 80.] 
          #eta_bins = [0.0, 0.4, 0.8, 1.37, 1.52, 2.5]
          pt_bins  = [20., 25., 30., 40., 50.]                                                          # Simon's binning
          eta_bins = [0.0, 0.3, 0.6, 1.0, 1.37, 1.52, 2.0, 2.5]
          tot_bins = len(pt_bins)*len(pt_bins)*(len(eta_bins)-1)*(len(eta_bins)-1)
          
          self.store['pt_bins']= pt_bins
          self.store['eta_bins']= eta_bins
          self.store['tot_bins']= tot_bins
                   
          ptbin1 = digitize( tau1.tlv.Pt()/GeV, pt_bins )
          ptbin2 = digitize( tau2.tlv.Pt()/GeV, pt_bins )
          
          etabin1 = digitize( abs(tau1.tlv.Eta()), eta_bins )
          etabin2 = digitize( abs(tau2.tlv.Eta()), eta_bins )
          
          #"bins shouldn't be 0"
          assert ptbin1!=0 
          assert ptbin2!=0 
          assert etabin1!=0 
          assert etabin2!=0 
          
          # encode pt1, pt2, eta1, eta2 into 1D bins given pt_bins and eta_bins
          CFtotBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          
          
          
         
            
          
                  
          #********    Store all variables    ****************
         
          self.store['taus_CFtotBin']			 = CFtotBin
         
        return True 
          
                        
class TauTruthCFVars(pyframe.core.Algorithm):
    """
    computes variables for Tau Truth CF
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'TauTruthCFVars',
                 key_electrons = 'electrons',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 key_taus = 'taus'
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_muons = key_muons
        self.key_met   = key_met
        self.key_taus = key_taus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_taus), "Taus key: %s not found in store!" % (self.key_electrons)
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        
        
     
        
        # -----------------------
        # at least one tau
        # -----------------------
        
        #Put leading and subleading electron in order
         
        if len(taus)>=1:
          
   
          for t in taus:
            
            if t.isTrueOneProngedTauFromZ():
              if t.tauTrueCharge() != t.charge:
              
                 self.store['OneProngedTauCF_pT']	 = t.tlv.Pt()
                 self.store['OneProngedTauCF_eta'] = abs(t.tlv.Eta())

            elif t.isTrueThreeProngedTauFromZ():
              if t.tauTrueCharge() != t.charge:
              
                 self.store['ThreeProngedTauCF_pT']	 = t.tlv.Pt()
                 self.store['ThreeProngedTauCF_eta'] = abs(t.tlv.Eta())          
                      
         
         
        return True 

class DiTauHadVars(pyframe.core.Algorithm):
    """
    Computes variables for the diTau_had selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiTauHadVars',
                 key_taus   = 'taus',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_taus = key_taus
        self.key_met   = key_met
        

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_taus), "tau key: %s not found in store!" % (self.key_taus)
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        
                
        # ------------------
        # exactly two tau_had
        # ------------------
        
        # dict containing pair 
        # and significance
         
        if len(taus) == 2:
        
          if taus[0].tlv.Pt() > taus[0].tlv.Pt():
                self.store['tau1'] = taus[0]
                self.store['tau2'] = taus[1]
          else: 
                self.store['tau1'] = taus[1]
                self.store['tau2'] = taus[0]
                
          tau1 = self.store['tau1'] 
          tau2 = self.store['tau2'] 
          
          
          tau1T = ROOT.TLorentzVector()
          tau1T.SetPtEtaPhiM( tau1.tlv.Pt(), tau1.tlv.Eta(), tau1.tlv.Phi(), tau1.tlv.M() )
          
          
          tau2T = ROOT.TLorentzVector()
          tau2T.SetPtEtaPhiM( tau2.tlv.Pt(), tau2.tlv.Eta(), tau2.tlv.Phi(), tau2.tlv.M() )
          
          self.store['taus_charge_product'] = tau2.charge*tau1.charge
          self.store['taus_mTVis']          = (tau2.tlv+tau1.tlv).M()
          self.store['taus_mTtot']          = (tau1T + tau2T + met.tlv).M()  
          self.store['taus_dphi']           = tau2.tlv.DeltaPhi(tau1.tlv)
          self.store['taus_deta']           = tau2.tlv.Eta()-tau1.tlv.Eta()
          
          self.store['taus_mCol']           = self.store['taus_mTVis'] / self.collinnear_approx_factor(met.tlv.Pt(), met.tlv.Phi(), tau1T.Pt(), tau1T.Phi(), tau2T.Pt(), tau2T.Phi())  
          
        return True
    #__________________________________________________________________________
    def collinnear_approx_factor(self, Pt_miss, Phi_miss, Pt_1, Phi_1, Pt_2, Phi_2): 
        
        #Return the factor of which a diTau event visible invariant mass should be divided by to give
        # the mass as given by the collinear approximation. I.e  M_collinear)=M_Vis / collinear_approx_factor    
        # Takes energy and angle of the missing energy and two particles.
        
        Pt_missy = Pt_miss * math.sin(Phi_miss)
        Pt_missx = Pt_miss * math.cos(Phi_miss)
        Pt_1y = Pt_1 * math.sin(Phi_1)
        Pt_1x = Pt_1 * math.cos(Phi_1)
        Pt_2y = Pt_2 * math.sin(Phi_2)
        Pt_2x = Pt_2 * math.cos(Phi_2)
         
        r_1 = abs ( (Pt_missy * Pt_1x - Pt_missx * Pt_1y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
        r_2 = abs ( (Pt_missy * Pt_2x - Pt_missx * Pt_2y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
           
        x_1 = 1.0 / (r_2 +1.0)
        x_2 = 1.0 / (r_1 +1.0)
        
        factor = math.sqrt(x_1 * x_2)
        
        return factor
        
class TauMuVars(pyframe.core.Algorithm):
    """
    Computes variables for the diTau_had selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'TauMuVars',
                 key_taus  = 'taus',
                 key_muons = 'muons',
                 key_met   = 'met_trk',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_taus = key_taus
        self.key_met   = key_met
        self.key_muons = key_muons
        

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_taus), "tau key: %s not found in store!" % (self.key_taus)
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        muons = self.store[self.key_muons]
        
        
                
        # ------------------
        # exactly one tau_had and one muon
        # ------------------
        
        # dict containing pair 
        # and significance
         
        if len(taus) == 1 and len(muons) == 1:
        
          tau = taus[0] 
          muon = muons[0]
          
          
          tauT = ROOT.TLorentzVector()
          tauT.SetPtEtaPhiM( tau.tlv.Pt(), tau.tlv.Eta(), tau.tlv.Phi(), tau.tlv.M() )
          
          
          muonT = ROOT.TLorentzVector()
          muonT.SetPtEtaPhiM( muon.tlv.Pt(), muon.tlv.Eta(), muon.tlv.Phi(), muon.tlv.M() )
          
          self.store['tauMu_charge_product'] = tau.charge*muon.trkcharge
          self.store['tauMu_mTVis']          = (tauT+muonT).M()
          self.store['tauMu_mTtot']          = (tauT + muonT + met.tlv).M()  
          self.store['tauMu_dphi']           = tauT.DeltaPhi(muonT)
          self.store['charge_deta']           = tauT.Eta()-muonT.Eta()
          
          self.store['tauMu_mCol']           = self.store['tauMu_mTVis'] / self.collinnear_approx_factor(met.tlv.Pt(), met.tlv.Phi(), tauT.Pt(), tauT.Phi(), muonT.Pt(), muonT.Phi())  
          
        return True
    #__________________________________________________________________________
    def collinnear_approx_factor(self, Pt_miss, Phi_miss, Pt_1, Phi_1, Pt_2, Phi_2): 
        
        #Return the factor of which a diTau event visible invariant mass should be divided by to give
        # the mass as given by the collinear approximation. I.e  M_collinear)=M_Vis / collinear_approx_factor    
        # Takes energy and angle of the missing energy and two particles.
        
        Pt_missy = Pt_miss * math.sin(Phi_miss)
        Pt_missx = Pt_miss * math.cos(Phi_miss)
        Pt_1y = Pt_1 * math.sin(Phi_1)
        Pt_1x = Pt_1 * math.cos(Phi_1)
        Pt_2y = Pt_2 * math.sin(Phi_2)
        Pt_2x = Pt_2 * math.cos(Phi_2)
         
        r_1 = abs ( (Pt_missy * Pt_1x - Pt_missx * Pt_1y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
        r_2 = abs ( (Pt_missy * Pt_2x - Pt_missx * Pt_2y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
           
        x_1 = 1.0 / (r_2 +1.0)
        x_2 = 1.0 / (r_1 +1.0)
        
        factor = math.sqrt(x_1 * x_2)
        
        return factor              

#------------------------------------------------------------------------------
class TauMultiLeptonVars(pyframe.core.Algorithm):
    """
    computes variables for the 4lep selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name          = 'TauMultiLeptonVars',
                 key_muons     = 'muons',
                 key_electrons = 'electrons',
                 key_met       = 'met_trk',
                 key_taus       = 'taus'
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons     = key_muons
        self.key_electrons = key_electrons
        self.key_met       = key_met
        self.key_taus       = key_taus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        assert self.store.has_key(self.key_taus), "electrons key: %s not found in store!" % (self.key_taus)
        muons     = self.store[self.key_muons]
        electrons = self.store[self.key_electrons]
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        leptons = electrons + muons + taus                       
        #--------------------
        # two same-sign pairs
       
        two_lep_pairs = {}
        leptonCharge = {}
        pT_tot = 0.
        if len(leptons)>=4:
                         
          for l in leptons:
            if l in taus:
              leptonCharge[l] = l.charge
            else:
              leptonCharge[l] = l.trkcharge 
          
          
          for q in combinations(leptons,4):
            if leptonCharge[q[0]] * leptonCharge[q[1]] * leptonCharge[q[2]] * leptonCharge[q[3]] > 0.0:
              two_lep_pairs[q] =  q[0].tlv.Pt() + q[1].tlv.Pt() + q[2].tlv.Pt() + q[3].tlv.Pt()


          min_pT  = 0.
          for quad,tot_pT in two_lep_pairs.iteritems():
            

            if tot_pT > min_pT:
              min_pT = tot_pT
              
              

              #Case 1: total charge 0
              if leptonCharge[quad[0]] + leptonCharge[quad[1]] + leptonCharge[quad[2]] + leptonCharge[quad[3]] == 0:
              
                for p in combinations(quad,2):
                
                  if (leptonCharge[p[0]] + leptonCharge[p[1]]) == 2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['lep1'] = p[0]
                      self.store['lep2'] = p[1]
                    else:
                      self.store['lep1'] = p[1]
                      self.store['lep2'] = p[0]
                  elif (leptonCharge[p[0]] + leptonCharge[p[1]]) == -2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['lep3'] = p[0]
                      self.store['lep4'] = p[1]
                    else:
                      self.store['lep3'] = p[1]
                      self.store['lep4'] = p[0]

              #Case 2: Total Charge = +/- 4
              elif abs(leptonCharge[quad[0]] + leptonCharge[quad[1]] + leptonCharge[quad[2]] + leptonCharge[quad[3]]) == 4:
                print("This event has charge 4!\n") #print for debugging purposes 
                self.store['lep1'] = quad[0]
                self.store['lep2'] = quad[1]
                self.store['lep3'] = quad[2]
                self.store['lep4'] = quad[3]

              #Failsafe
              else:
                print("Error: Something has gone horribly wrong with this event!\n")
                self.store['lep1'] = quad[0]
                self.store['lep2'] = quad[1]
                self.store['lep3'] = quad[2]
                self.store['lep4'] = quad[3]

        if two_lep_pairs:
          lep1 = self.store['lep1']
          lep2 = self.store['lep2']

          self.store['charge_product1'] = leptonCharge[lep2]*leptonCharge[lep1]
          self.store['charge_sum1']     = leptonCharge[lep2]+leptonCharge[lep1]
          self.store['mVis1']           = (lep2.tlv+lep1.tlv).M()
          self.store['leps_dphi1']     = lep2.tlv.DeltaPhi(lep1.tlv)
          self.store['leps_deta1']     = lep2.tlv.Eta()-lep1.tlv.Eta()
          self.store['pTH1']            = (lep2.tlv+lep1.tlv).Pt()
          self.store['leps_dR1']       = lep2.tlv.DeltaR(lep1.tlv)
          
          #print(self.store['mVis1'])

          lep3 = self.store['lep3']
          lep4 = self.store['lep4']

          #Define here the OS masses stores
          self.store['mOS1'] = (lep1.tlv + lep3.tlv).M()
          self.store['mOS2'] = (lep1.tlv + lep4.tlv).M()
          self.store['mOS3'] = (lep2.tlv + lep3.tlv).M()
          self.store['mOS4'] = (lep2.tlv + lep4.tlv).M()

          self.store['charge_product2'] = leptonCharge[lep4]*leptonCharge[lep3]
          self.store['charge_sum2']     = leptonCharge[lep4]+leptonCharge[lep3]
          self.store['mVis2']           = (lep4.tlv+lep3.tlv).M()
          self.store['leps_dphi2']     = lep4.tlv.DeltaPhi(lep3.tlv)
          self.store['leps_deta2']     = lep4.tlv.Eta()-lep3.tlv.Eta()
          self.store['pTH2']            = (lep4.tlv+lep3.tlv).Pt()
          self.store['leps_dR2']       = lep4.tlv.DeltaR(lep3.tlv)

          self.store['charge_product'] = leptonCharge[quad[0]] * leptonCharge[quad[1]] * leptonCharge[quad[2]] * leptonCharge[quad[3]]
          self.store['charge_sum']     = leptonCharge[quad[0]] + leptonCharge[quad[1]] + leptonCharge[quad[2]] + leptonCharge[quad[3]]
          self.store['mTtot']          = (lep1.tlv + lep2.tlv + lep3.tlv + lep4.tlv + met.tlv).M()
          self.store['mVis']           = (self.store['mVis1']+self.store['mVis2'])/2
          self.store['FullMass']       = (self.store['mVis1']+self.store['mVis2'])
          self.store['dmOverM']        = ((self.store['mVis1'] - self.store['mVis2'])/((self.store['mVis1']+self.store['mVis2'])/2))
          self.store['dmVis']          = self.store['mVis1'] - self.store['mVis2']
          self.store['pairs_dphi']     = (lep3.tlv+lep4.tlv).DeltaPhi(lep1.tlv+lep2.tlv)
          self.store['pairs_deta']     = (lep3.tlv+lep4.tlv).Eta()-(lep1.tlv+lep2.tlv).Eta()
          self.store['pairs_dR']       = (lep3.tlv+lep4.tlv).DeltaR(lep1.tlv+lep2.tlv)
        return True       
#------------------------------------------------------------------------------
class SignalComparisonVars(pyframe.core.Algorithm):
    """
    computes variables for the mixed (electron-muon) selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiLeptonVars',
                 key_electrons = 'electrons',
                 key_muons = 'muons',
                 key_taus = 'taus',
                 key_met   = 'met_trk',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_muons = key_muons
        self.key_met   = key_met
        self.key_taus  = key_taus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        assert self.store.has_key(self.key_taus), "electrons key: %s not found in store!" % (self.key_taus)
        muons     = self.store[self.key_muons]
        electrons = self.store[self.key_electrons]
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        leptons = electrons + muons + taus  
        
        if len(taus) >= 4: print('At least for taus \n')
        self.store['ntau'] = len(taus)
        self.store['met'] = met.tlv.Pt()
            
                 
         
        
          
          
        return True
#------------------------------------------------------------------------------
class DiLeptonVars(pyframe.core.Algorithm):
    """
    computes variables for the mixed (electron-muon) selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'DiLeptonVars',
                 key_electrons = 'electrons',
                 key_muons = 'muons',
                 key_taus = 'taus',
                 key_met   = 'met_trk',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_muons = key_muons
        self.key_met   = key_met
        self.key_taus  = key_taus

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        assert self.store.has_key(self.key_taus), "electrons key: %s not found in store!" % (self.key_taus)
        muons     = self.store[self.key_muons]
        electrons = self.store[self.key_electrons]
        taus = self.store[self.key_taus]
        met = self.store[self.key_met]
        leptons = electrons + muons + taus  
        
        # -------------------------------
        # at least 2 leptons
        # -------------------------------
        
        # dict containing pair 
        # and significance
        ss_pairs = {}
        leptonCharge = {} 
        if len(leptons) >= 2:
        
          for l in leptons:
            if l in taus:
              leptonCharge[l] = l.charge
            else:
              leptonCharge[l] = l.trkcharge 
          #and (q[0] in taus or q[1] in taus)
          for q in combinations(leptons,2):
            if (leptonCharge[q[0]] * leptonCharge[q[1]] > 0) :
              ss_pairs[q] =  q[0].tlv.Pt() + q[1].tlv.Pt() 

          min_pT  = 0.       
          
          for pair,tot_pT in ss_pairs.iteritems():
            if tot_pT > min_pT:
              min_pT = tot_pT 
              if pair[0].tlv.Pt() > pair[1].tlv.Pt():
                self.store['lep1'] = pair[0] # leading
                self.store['lep2'] = pair[1] # subleading
              else: 
                self.store['lep1'] = pair[1] # subleading
                self.store['lep2'] = pair[0] # leading
               
        
        if ss_pairs :
          lep1 = self.store['lep1'] # leading
          lep2 = self.store['lep2'] # subleading
          lep1T = ROOT.TLorentzVector()
          lep1T.SetPtEtaPhiM( lep1.tlv.Pt(), 0., lep1.tlv.Phi(), lep1.tlv.M() )
          lep2T = ROOT.TLorentzVector()
          lep2T.SetPtEtaPhiM( lep2.tlv.Pt(), 0., lep2.tlv.Phi(), lep2.tlv.M() )
          
                 
          self.store['charge_product'] = leptonCharge[lep2] * leptonCharge[lep1]
          self.store['mTVis']           = (lep2.tlv+lep1.tlv).M()
          #print(self.store['mTVis']) 
          self.store['mTtot']          = (lep1T + lep2T + met.tlv).M()  
          self.store['dilepton_dphi']       = lep2.tlv.DeltaPhi(lep1.tlv)
          self.store['dilepton_deta']       = lep2.tlv.Eta()-lep1.tlv.Eta()
          self.store['pTH']            = (lep1.tlv+lep2.tlv).Pt()
          self.store['sumpT']            = (lep1.tlv.Pt()+lep2.tlv.Pt())
          self.store['dilepton_dR']       = lep1.tlv.DeltaR(lep2.tlv)
          
          
          if (lep1 in electrons and lep2 in electrons):
          	self.store['decayType'] = 0
          elif (lep1 in muons and lep2 in muons):
          	self.store['decayType'] = 1
          elif (lep1 in taus and lep2 in taus):
          	self.store['decayType'] = 2	
          elif ((lep1 in electrons and lep2 in muons) or (lep2 in electrons and lep1 in muons)):
          	self.store['decayType'] = 3	
          elif ((lep1 in taus and lep2 in muons) or (lep2 in taus and lep1 in muons)):
          	self.store['decayType'] = 4
          elif ((lep1 in taus and lep2 in electrons) or (lep2 in taus and lep1 in electrons)):
          	self.store['decayType'] = 5
          	
          
          col_factor = self.collinnear_approx_factor(met.tlv.Pt(), met.tlv.Phi(), lep1T.Pt(), lep1T.Phi(), lep2T.Pt(), lep2T.Phi())
                
          self.store['dilep_mCol']           = self.store['mTVis'] / col_factor
          self.store['dilep_mCol_80'] = -1
          self.store['dilep_mCol_60'] = -1
          
          
        
          if abs(lep2.tlv.DeltaPhi(lep1.tlv)) < 0.8*math.pi:
           self.store['dilep_mCol_80'] = self.store['mTVis'] / col_factor
          if abs(lep2.tlv.DeltaPhi(lep1.tlv)) < 0.6*math.pi:
           
           self.store['dilep_mCol_60'] = self.store['mTVis'] / col_factor
          
          
          
        return True
    #__________________________________________________________________________
    def collinnear_approx_factor(self, Pt_miss, Phi_miss, Pt_1, Phi_1, Pt_2, Phi_2): 
        
        #Return the factor of which a diTau event visible invariant mass should be divided by to give
        # the mass as given by the collinear approximation. I.e  M_collinear)=M_Vis / collinear_approx_factor    
        # Takes energy and angle of the missing energy and two particles.
        
        Pt_missy = Pt_miss * math.sin(Phi_miss)
        Pt_missx = Pt_miss * math.cos(Phi_miss)
        Pt_1y = Pt_1 * math.sin(Phi_1)
        Pt_1x = Pt_1 * math.cos(Phi_1)
        Pt_2y = Pt_2 * math.sin(Phi_2)
        Pt_2x = Pt_2 * math.cos(Phi_2)
         
        r_1 = abs ( (Pt_missy * Pt_1x - Pt_missx * Pt_1y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
        r_2 = abs ( (Pt_missy * Pt_2x - Pt_missx * Pt_2y)  /  (Pt_1y * Pt_2x - Pt_1x * Pt_2y) )
           
        x_1 = 1.0 / (r_2 +1.0)
        x_2 = 1.0 / (r_1 +1.0)
        
        factor = math.sqrt(x_1 * x_2)
        
        return factor

#------------------------------------------------------------------------------
class ThreeLepVars(pyframe.core.Algorithm):
    """
    computes variables for the mixed (electron-muon) selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'ThreeLepVars',
                 key_electrons = 'electrons_loose',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_electrons = key_electrons
        self.key_muons = key_muons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        electrons = self.store[self.key_electrons]
        muons = self.store[self.key_muons]
        met = self.store[self.key_met]
        
        # -------------------------------
        # at least 1 electron and 1 muon
        # -------------------------------
        
        # dict containing pair 
        # and significance
        leptons = electrons + muons
        if len(leptons)==3:
          
          for lep in combinations(leptons,3):
              if (lep[0].trkcharge*lep[1].trkcharge > 0.0):   
                   if lep[0].tlv.Pt() > lep[1].tlv.Pt():              
                       self.store['lep1'] = lep[0] # leading
                       self.store['lep2'] = lep[1] # subleading
                       self.store['lep3'] = lep[2] # OS one
                   else: 
                       self.store['lep2'] = lep[0] # leading
                       self.store['lep1'] = lep[1] # subleading
                       self.store['lep3'] = lep[2] # OS one
              elif(lep[1].trkcharge*lep[2].trkcharge > 0.0):         
                   if lep[1].tlv.Pt() > lep[2].tlv.Pt():              
                       self.store['lep1'] = lep[1] # leading
                       self.store['lep2'] = lep[2] # subleading
                       self.store['lep3'] = lep[0] # OS one
                   else: 
                       self.store['lep2'] = lep[1] # leading
                       self.store['lep1'] = lep[2] # subleading
                       self.store['lep3'] = lep[0] # OS one
              elif(lep[0].trkcharge*lep[2].trkcharge > 0.0):         
                   if lep[0].tlv.Pt() > lep[2].tlv.Pt():              
                       self.store['lep1'] = lep[0] # leading
                       self.store['lep2'] = lep[2] # subleading
                       self.store['lep3'] = lep[1] # OS one
                   else: 
                       self.store['lep2'] = lep[2] # leading
                       self.store['lep1'] = lep[0] # subleading
                       self.store['lep3'] = lep[1] # OS one
                
          lep1 = self.store['lep1'] # leading
          lep2 = self.store['lep2'] # subleading
          lep3 = self.store['lep3'] # OS lep
          
          lep1T = ROOT.TLorentzVector()
          lep1T.SetPtEtaPhiM( lep1.tlv.Pt(), 0., lep1.tlv.Phi(), lep1.tlv.M() )
          lep2T = ROOT.TLorentzVector()
          lep2T.SetPtEtaPhiM( lep2.tlv.Pt(), 0., lep2.tlv.Phi(), lep2.tlv.M() )
          lep3T = ROOT.TLorentzVector()
          lep3T.SetPtEtaPhiM( lep3.tlv.Pt(), 0., lep3.tlv.Phi(), lep3.tlv.M() )
          
          self.store['charge_product'] = lep2.trkcharge*lep1.trkcharge
          self.store['mVis']           = (lep2.tlv+lep1.tlv).M()
          self.store['mTtot']          = (lep1T + lep2T + met.tlv).M()  
          self.store['elemu_dphi']       = lep2.tlv.DeltaPhi(lep1.tlv)
          self.store['elemu_deta']       = lep2.tlv.Eta()-lep1.tlv.Eta()
          self.store['elemu_dR']         = lep2.tlv.DeltaR(lep1.tlv)
          self.store['pTH']         = (lep1.tlv+ lep2.tlv).Pt()
          self.store['sumpT']         = (lep1.tlv.Pt()+ lep2.tlv.Pt() + lep3.tlv.Pt())
          
          #Variables for the two OS couples:
          self.store['OSmVis1']           = (lep1.tlv+lep3.tlv).M()
          self.store['OSmTtot1']          = (lep1T + lep3T + met.tlv).M()  
          self.store['OSelemu_dphi1']       = lep1.tlv.DeltaPhi(lep3.tlv)
          self.store['OSelemu_deta1']       = lep1.tlv.Eta()-lep3.tlv.Eta()

          self.store['OSmVis2']           = (lep2.tlv+lep3.tlv).M()
          self.store['OSmTtot2']          = (lep2T + lep3T + met.tlv).M()  
          self.store['OSelemu_dphi2']       = lep2.tlv.DeltaPhi(lep3.tlv)
          self.store['OSelemu_deta2']       = lep2.tlv.Eta()-lep3.tlv.Eta()

        return True

#------------------------------------------------------------------------------
class MultiMuVars(pyframe.core.Algorithm):
    """
    computes variables for the di-muon selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name      = 'MultiMuVars',
                 key_muons = 'muons',
                 key_met   = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons = key_muons
        self.key_met   = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        muons = self.store[self.key_muons]

        #--------------------
        # two same-sign pairs
        #--------------------
        two_pairs = {}
        if len(muons)>=4:
          for q in combinations(muons,4):
            if q[0].trkcharge * q[1].trkcharge * q[2].trkcharge * q[3].trkcharge > 0.0:
              two_pairs[q] = q[0].trkd0sig + q[1].trkd0sig + q[2].trkd0sig + q[3].trkd0sig

          max_sig  = 1000.
          for quad,sig in two_pairs.iteritems():

            if sig < max_sig:
              max_sig = sig 

              #Case 1: total charge 0
              if quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge == 0:
                for p in combinations(quad,2):
                  if (p[0].trkcharge + p[1].trkcharge) == 2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['muon1'] = p[0]
                      self.store['muon2'] = p[1]
                    else:
                      self.store['muon1'] = p[1]
                      self.store['muon2'] = p[0]
                  elif (p[0].trkcharge + p[1].trkcharge) == -2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['muon3'] = p[0]
                      self.store['muon4'] = p[1]
                    else:
                      self.store['muon3'] = p[1]
                      self.store['muon4'] = p[0]

              #Case 2: Total Charge = +/- 4
              elif abs(quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge) == 4:
                print("This event has charge 4!\n") #print for debugging purposes 
                self.store['muon1'] = quad[0]
                self.store['muon2'] = quad[1]
                self.store['muon3'] = quad[2]
                self.store['muon4'] = quad[3]

              #Failsafe
              else:
                print("Error: Something has gone horribly wrong with this event!\n")
                self.store['muon1'] = quad[0]
                self.store['muon2'] = quad[1]
                self.store['muon3'] = quad[2]
                self.store['muon4'] = quad[3]

        if two_pairs:
          muon1 = self.store['muon1']
          muon2 = self.store['muon2']
          muon1T = ROOT.TLorentzVector()
          muon1T.SetPtEtaPhiM( muon1.tlv.Pt(), 0., muon1.tlv.Phi(), muon1.tlv.M() )
          muon2T = ROOT.TLorentzVector()
          muon2T.SetPtEtaPhiM( muon2.tlv.Pt(), 0., muon2.tlv.Phi(), muon2.tlv.M() )

          self.store['charge_product1'] = muon2.trkcharge*muon1.trkcharge
          self.store['charge_sum1']     = muon1.trkcharge + muon2.trkcharge
          self.store['mVis1']           = (muon2.tlv+muon1.tlv).M()
          self.store['muons_dphi1']     = muon2.tlv.DeltaPhi(muon1.tlv)
          self.store['muons_deta1']     = muon2.tlv.Eta()-muon1.tlv.Eta()
          self.store['pTH1']            = (muon2.tlv+muon1.tlv).Pt()
          self.store['muons_dR1']       = math.sqrt(self.store['muons_dphi1']**2 + self.store['muons_deta1']**2)

          muon3 = self.store['muon3']
          muon4 = self.store['muon4']
          muon3T = ROOT.TLorentzVector()
          muon3T.SetPtEtaPhiM( muon3.tlv.Pt(), 0., muon3.tlv.Phi(), muon3.tlv.M() )
          muon4T = ROOT.TLorentzVector()
          muon4T.SetPtEtaPhiM( muon4.tlv.Pt(), 0., muon4.tlv.Phi(), muon4.tlv.M() )

          self.store['charge_product2'] = muon4.trkcharge*muon3.trkcharge
          self.store['charge_sum2']     = muon3.trkcharge + muon4.trkcharge
          self.store['mVis2']           = (muon4.tlv+muon3.tlv).M()
          self.store['muons_dphi2']     = muon4.tlv.DeltaPhi(muon3.tlv)
          self.store['muons_deta2']     = muon4.tlv.Eta()-muon3.tlv.Eta()
          self.store['pTH2']            = (muon4.tlv+muon3.tlv).Pt()
          self.store['muons_dR2']       = math.sqrt(self.store['muons_dphi2']**2 + self.store['muons_deta2']**2)

          self.store['charge_product'] = muon4.trkcharge * muon3.trkcharge * muon2.trkcharge * muon1.trkcharge
          self.store['charge_sum']     = muon1.trkcharge + muon2.trkcharge + muon3.trkcharge + muon4.trkcharge
          self.store['mTtot']          = (muon1T + muon2T + muon3T + muon4T + met.tlv).M()
          self.store['mVis']           = (self.store['mVis1']+self.store['mVis2'])/2
          self.store['dmVis']          = self.store['mVis1'] - self.store['mVis2']
          self.store['pairs_dphi']     = (muon3.tlv+muon4.tlv).DeltaPhi(muon1.tlv+muon2.tlv)
          self.store['pairs_deta']     = (muon3.tlv+muon4.tlv).Eta()-(muon1.tlv+muon2.tlv).Eta()
          self.store['pairs_dR']       = math.sqrt(self.store['pairs_dphi']**2 + self.store['pairs_deta']**2)

        return True
#------------------------------------------------------------------------------
class MultiLeptonVars(pyframe.core.Algorithm):
    """
    computes variables for the 4lep selection
    """
    #__________________________________________________________________________
    def __init__(self, 
                 name          = 'MultiLeptonVars',
                 key_muons     = 'muons',
                 key_electrons = 'electrons_loose',
                 key_met       = 'met_clus',
                 ):
        pyframe.core.Algorithm.__init__(self, name)
        self.key_muons     = key_muons
        self.key_electrons = key_electrons
        self.key_met       = key_met

    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)
        """
        computes variables and puts them in the store
        """

        ## get objects from event candidate
        ## --------------------------------------------------
        assert self.store.has_key(self.key_muons), "muons key: %s not found in store!" % (self.key_muons)
        assert self.store.has_key(self.key_electrons), "electrons key: %s not found in store!" % (self.key_electrons)
        muons     = self.store[self.key_muons]
        electrons = self.store[self.key_electrons]
        met = self.store[self.key_met]
        leptons = electrons + muons                       
        #--------------------
        # two same-sign pairs
        alpha = array('d',[0.08, 0.004, 0.005, 0.004, 0.003, 0.004])
        beta  = array('d',[0.78, 1.50,  1.41,  1.45,  1.41,  1.46 ])
        flavour =self.store['ChannelFlavour']

        two_lep_pairs = {}
        if len(leptons)>=4:
          for q in combinations(leptons,4):
            if q[0].trkcharge * q[1].trkcharge * q[2].trkcharge * q[3].trkcharge > 0.0:
              two_lep_pairs[q] = q[0].trkd0sig + q[1].trkd0sig + q[2].trkd0sig + q[3].trkd0sig


          max_sig  = 1000.
          for quad,sig in two_lep_pairs.iteritems():

            if sig < max_sig:
              max_sig = sig 

              #Case 1: total charge 0
              if quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge == 0:
                for p in combinations(quad,2):
                  if (p[0].trkcharge + p[1].trkcharge) == 2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['lep1'] = p[0]
                      self.store['lep2'] = p[1]
                    else:
                      self.store['lep1'] = p[1]
                      self.store['lep2'] = p[0]
                  elif (p[0].trkcharge + p[1].trkcharge) == -2:
                    if p[0].tlv.Pt() > p[1].tlv.Pt():
                      self.store['lep3'] = p[0]
                      self.store['lep4'] = p[1]
                    else:
                      self.store['lep3'] = p[1]
                      self.store['lep4'] = p[0]

              #Case 2: Total Charge = +/- 4
              elif abs(quad[0].trkcharge + quad[1].trkcharge + quad[2].trkcharge + quad[3].trkcharge) == 4:
                print("This event has charge 4!\n") #print for debugging purposes 
                self.store['lep1'] = quad[0]
                self.store['lep2'] = quad[1]
                self.store['lep3'] = quad[2]
                self.store['lep4'] = quad[3]

              #Failsafe
              else:
                print("Error: Something has gone horribly wrong with this event!\n")
                self.store['lep1'] = quad[0]
                self.store['lep2'] = quad[1]
                self.store['lep3'] = quad[2]
                self.store['lep4'] = quad[3]

        if two_lep_pairs:
          lep1 = self.store['lep1']
          lep2 = self.store['lep2']

          self.store['charge_product1'] = lep2.trkcharge*lep1.trkcharge
          self.store['charge_sum1']     = lep1.trkcharge + lep2.trkcharge
          self.store['mVis1']           = (lep2.tlv+lep1.tlv).M()
          self.store['leps_dphi1']     = lep2.tlv.DeltaPhi(lep1.tlv)
          self.store['leps_deta1']     = lep2.tlv.Eta()-lep1.tlv.Eta()
          self.store['pTH1']            = (lep2.tlv+lep1.tlv).Pt()
          self.store['leps_dR1']       = lep2.tlv.DeltaR(lep1.tlv)

          lep3 = self.store['lep3']
          lep4 = self.store['lep4']

          #Define here the OS masses stores
          self.store['mOS1'] = (lep1.tlv + lep3.tlv).M()
          self.store['mOS2'] = (lep1.tlv + lep4.tlv).M()
          self.store['mOS3'] = (lep2.tlv + lep3.tlv).M()
          self.store['mOS4'] = (lep2.tlv + lep4.tlv).M()

          self.store['charge_product2'] = lep4.trkcharge*lep3.trkcharge
          self.store['charge_sum2']     = lep3.trkcharge + lep4.trkcharge
          self.store['mVis2']           = (lep4.tlv+lep3.tlv).M()
          self.store['leps_dphi2']     = lep4.tlv.DeltaPhi(lep3.tlv)
          self.store['leps_deta2']     = lep4.tlv.Eta()-lep3.tlv.Eta()
          self.store['pTH2']            = (lep4.tlv+lep3.tlv).Pt()
          self.store['leps_dR2']       = lep4.tlv.DeltaR(lep3.tlv)

          self.store['charge_product'] = lep4.trkcharge * lep3.trkcharge * lep2.trkcharge * lep1.trkcharge
          self.store['charge_sum']     = lep1.trkcharge + lep2.trkcharge + lep3.trkcharge + lep4.trkcharge
          self.store['mTtot']          = (lep1.tlv + lep2.tlv + lep3.tlv + lep4.tlv + met.tlv).M()
          self.store['mVis']           = (self.store['mVis1']+self.store['mVis2'])/2
          self.store['FullMass']       = (self.store['mVis1']+self.store['mVis2'])
          self.store['dmOverM']        = ((self.store['mVis1'] - self.store['mVis2'])/((self.store['mVis1']+self.store['mVis2'])/2))
          self.store['dmOverAlphaMBeta']= ((self.store['mVis1']/GeV - self.store['mVis2']/GeV)/(alpha[flavour]*pow(self.store['mVis']/GeV,beta[flavour])))
          self.store['dmVis']          = self.store['mVis1'] - self.store['mVis2']
          self.store['pairs_dphi']     = (lep3.tlv+lep4.tlv).DeltaPhi(lep1.tlv+lep2.tlv)
          self.store['pairs_deta']     = (lep3.tlv+lep4.tlv).Eta()-(lep1.tlv+lep2.tlv).Eta()
          self.store['pairs_dR']       = (lep3.tlv+lep4.tlv).DeltaR(lep1.tlv+lep2.tlv)
        return True
        
 

#__________________________________________________________________________
#Used for the charge flip code to get the bins correct
def digitize(value, binEdges):
  assert isinstance(binEdges,list), "binEdges must be an array of bin edges"
  if value < binEdges[0]: return 0
  elif value >= binEdges[-1]: return len(binEdges)
  for i in range(len(binEdges)):
    edlow = binEdges[i]
    edhigh = binEdges[i+1]
    if value >= edlow and value < edhigh:
      return i+1
# EOF 


