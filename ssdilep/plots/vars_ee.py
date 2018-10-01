# encoding: utf-8
'''
vars_ee.py
description:
variables for the ee channel
'''

## modules
from var import Var
from funcs import generateLogBins

## Cutflows
## ---------------------------------------
"""
cutflow_weighted          = Var(name = 'cutflow_weighted_mumu',log=False)
cutflow                   = Var(name = 'cutflow_mumu',log=False)
cutflow_weighted_mu_pairs = Var(name = 'cutflow_weighted_mumu_mu_pairs',log=False)
cutflow_mu_pairs          = Var(name = 'cutflow_mumu_mu_pairs',log=False)
cutflow_presel            = Var(name = 'cutflow_presel',log=False)
cutflow_weighted_presel   = Var(name = 'cutflow_weighted_presel',log=False)
cutflow_ZCR               = Var(name = 'cutflow_ZCR',log=False)
cutflow_weighted_ZCR      = Var(name = 'cutflow_weighted_ZCR',log=False)
"""

## Non-equidistant bins from the old framework
## ---------------------------------------
"""
bins_pt = generateLogBins(35,30,2000)

bins_mt = generateLogBins(50,50,2000)
bins_invM = generateLogBins(50,130,2000)
bins_invM_2 = generateLogBins(15,130,200)
bins_invM_3 = generateLogBins(8,130,200)
bins_invM_4 = generateLogBins(6,90,200)
bins_Zpeak = [50,70,74,77,80,82,83,84,85,86,87,88,89,90,91,92,93,94,95,97,99,102,105,110,130]
bins_Zpeak2 = [50,80,100,130]
bins_met = generateLogBins(15,1,1000)
bins_met_2 = generateLogBins(50,25,2000)
"""

bins_pt_2 = generateLogBins(20,30,1000)


## Event variables
## ---------------------------------------
averageIntPerXing = Var(name = 'averageIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

actualIntPerXing = Var(name = 'actualIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

NPV = Var(name = 'NPV',
              path  = 'event',
              xmin  = 0,
              xmax  = 35.,
              log   = False,
              )

nmuons = Var(name = 'nmuons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nelectrons = Var(name = 'nelectrons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

njets = Var(name = 'njets',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nmuonpairs = Var(name = 'nmuonpairs',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

mujet_dphi = Var(name = 'mujet_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = True,
              )

scdphi = Var(name     = 'scdphi',
              path    = 'event',
              xmin    = -2.,
              xmax    = 2.,
              rebin   = 4,
              log     = False,
              )

electrons_mVis = Var(name     = 'electrons_mVis',
              path    = 'event',
              #xmin    = 0.,
              xmin    = 0.,
              xmax    = 2000.,
              #xmax    = 800.,
              #xmax    = 500.,
              rebin   = 4,
              #rebinVar = bins_invM,
              log     = True,
              #logx    = False,
              )

electrons_mTtot = Var(name     = 'electrons_mTtot',
              path    = 'event',
              #xmin    = 0.,
              xmin    = 0.,
              xmax    = 2000.,
              #xmax    = 800.,
              #xmax    = 500.,
              rebin   = 1,
              #rebinVar = bins_invM,
              log     = True,
              #logx    = False,
              )

electrons_dphi = Var(name = 'electrons_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

electrons_deta = Var(name = 'electrons_deta',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )

electrons_chargeprod = Var(name = 'electrons_chargeprod',
              path    = 'event',
              xmin    = -2,
              xmax    = 2,
              #rebin  = 10,
              log     = False,
              )


## Single electron variables
## ---------------------------------------
elelead_pt = Var(name = 'elelead_pt',
              path   = 'electrons',
              xmin   = 0.,
              #xmax   = 400.,
              xmax   = 2000.,
              #xmax   = 120.,
              #rebin  = 20,
              #rebin  = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log    = True,
              #logx   = False,
              )

elesublead_pt = Var(name = 'elesublead_pt',
              path   = 'electrons',
              xmin   = 0.,
              #xmax   = 400.,
              xmax   = 2000.,
              #xmax   = 120.,
              #rebin  = 20,
              #rebin  = 5,
              rebin  = 1,
              #rebinVar = bins_invM,
              log    = True,
              #logx   = False,
              )

elelead_eta = Var(name = 'elelead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log     = False,
              #logx    = False,
              )

elesublead_eta = Var(name = 'elesublead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log     = False,
              #logx    = False,
              )

elelead_phi = Var(name = 'elelead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              logx    = False,
              )

elesublead_phi = Var(name = 'elesublead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              logx    = False,
              )

elelead_trkd0 = Var(name = 'elelead_trkd0',
              path    = 'electrons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin  = 1,
              log     = False,
              )

elesublead_trkd0 = Var(name = 'elesublead_trkd0',
              path    = 'electrons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin   = 1,
              log     = False,
              )

elelead_trkd0sig = Var(name = 'elelead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

elesublead_trkd0sig = Var(name = 'elesublead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

elelead_trkz0 = Var(name = 'elelead_trkz0',
              path    = 'electrons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

elesublead_trkz0 = Var(name = 'elesublead_trkz0',
              path    = 'electrons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

elelead_trkz0sintheta = Var(name = 'elelead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

elesublead_trkz0sintheta = Var(name = 'elesublead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

# isolation
elelead_topoetcone20 = Var(name = 'elelead_topoetcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )

elelead_topoetcone30 = Var(name = 'elelead_topoetcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_topoetcone40 = Var(name = 'elelead_topoetcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptvarcone20 = Var(name = 'elelead_ptvarcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = True,
              )
elelead_ptvarcone30 = Var(name = 'elelead_ptvarcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptvarcone40 = Var(name = 'elelead_ptvarcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone20 = Var(name = 'elelead_ptcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone30 = Var(name = 'elelead_ptcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone40 = Var(name = 'elelead_ptcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )


## tag and probe
## -------------------------------------
tag_pt = Var(name = 'tag_pt',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 10,
              log    = False,
              )
probe_pt = Var(name = 'probe_pt',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 10,
              log    = False,
              )
probe_ptiso = Var(name = 'probe_ptiso',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 10,
              log    = False,
              )
probe_ujet_pt = Var(name = 'probe_ujet_pt',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 10,
              log    = False,
              )

# jets
jetlead_pt = Var(name = 'jetlead_pt',
              path    = 'jets',
              xmin    = 0.,
              xmax    = 300.,
              rebin   = 5,
              log     = True,
              )


## MET variables
## ---------------------------------------
met_clus_et = Var(name = 'met_clus_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 10,
              log     = False,
              )

met_clus_phi = Var(name = 'met_clus_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

met_trk_et = Var(name = 'met_trk_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 20,
              log     = False,
              )

met_trk_phi = Var(name = 'met_trk_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

met_clus_sumet = Var(name = 'met_clus_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )

met_trk_sumet = Var(name = 'met_trk_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )



vars_list = []


# ---------------
# for all studies
# ---------------
#"""
vars_list.append(averageIntPerXing)
vars_list.append(actualIntPerXing)
vars_list.append(NPV)
vars_list.append(nelectrons)
vars_list.append(nelectrons)
vars_list.append(njets)
vars_list.append(nmuonpairs)

vars_list.append(elelead_pt)
vars_list.append(elelead_eta)
vars_list.append(elelead_phi)
vars_list.append(elelead_trkd0)
vars_list.append(elelead_trkd0sig)
vars_list.append(elelead_trkz0)
vars_list.append(elelead_trkz0sintheta)
vars_list.append(elelead_ptvarcone30)

vars_list.append(met_clus_et)
vars_list.append(met_clus_phi)
vars_list.append(met_clus_sumet)
#"""


# -------------
# tag-and-probe
# -------------
#"""
vars_list.append(tag_pt)
vars_list.append(probe_pt)
vars_list.append(probe_ptiso)
vars_list.append(probe_ptiso)
vars_list.append(probe_ujet_pt)
#"""


# ---------------------
# just for fake-factors
# ---------------------
"""
vars_list.append(mujet_dphi)
vars_list.append(scdphi)
vars_list.append(jetlead_pt)
"""

# ---------------------
# for validation
# ---------------------
#"""
vars_list.append(elesublead_pt)
vars_list.append(elesublead_eta)
vars_list.append(elesublead_phi)
vars_list.append(elesublead_trkd0)
vars_list.append(elesublead_trkd0sig)
vars_list.append(elesublead_trkz0)
vars_list.append(elesublead_trkz0sintheta)

vars_list.append(electrons_mTtot)
vars_list.append(electrons_mVis)
vars_list.append(electrons_dphi)
vars_list.append(electrons_deta)
vars_list.append(electrons_chargeprod)
#"""


# ---------------------
# cutflows
# ---------------------
"""
vars_list.append(cutflow_presel)
vars_list.append(cutflow_weighted_presel)
vars_list.append(cutflow_ZCR)
vars_list.append(cutflow_weighted_ZCR)
"""

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__


## EOF



