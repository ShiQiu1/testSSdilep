## modules
import ROOT

import histmgr
import funcs
import os

#from ssdilep.samples import samples, samples_DCH
from ssdilep.samples import samples
from ssdilep.plots   import vars_mumu
from ssdilep.plots   import vars
from systematics     import *

from optparse import OptionParser

DO_SYS = True
ELE_SYS = False
MU_SYS = False

BRee = 0.
BRem = 0.
BRmm = 0.

#-----------------
# input
#-----------------
parser = OptionParser()
parser.add_option('-v', '--var', dest='vname',
                  help='varable name',metavar='VAR',default=None)
parser.add_option('-r', '--reg', dest='region',
                  help='region name',metavar='REG',default=None)
parser.add_option('-l', '--lab', dest='label',
                  help='region label',metavar='LAB',default=None)
parser.add_option('-c', '--icut', dest='icut',
                  help='number of cuts',metavar='ICUT',default=None)
parser.add_option('-p', '--makeplot', dest='makeplot',
                  help='make plot',metavar='MAKEPLOT',default=None)
parser.add_option('-i', '--input', dest='indir',
                  help='input directory',metavar='INDIR',default=None)
parser.add_option('-o', '--output', dest='outdir',
                  help='output directory',metavar='OUTDIR',default=None)
parser.add_option('-f', '--fakest', dest='fakest',
                  help='choose fake estimate',metavar='FAKEST',default=None)
parser.add_option('-t', '--tag', dest='tag',
                  help='outfile tag',metavar='TAG',default=None)
parser.add_option('-R', '--rebinToEq', dest='rebinToEq',
                  help='rebinToEq',metavar='REBINTOEQ',default=None)
parser.add_option('-S', '--signal', dest='signal',
                  help='signal',metavar='SIGNAL',default=None)
parser.add_option('-V', '--varName', dest='varName',
                  help='varName',metavar='VARNAME',default=None)
parser.add_option('-L', '--logy', dest='logy',
                  help='logy',metavar='LOGY',default=None)
parser.add_option('-y', '--sys', dest='sys',
                  help='sys',metavar='SYS',default=None)
parser.add_option('-E', '--elesys', dest='elesys',
                  help='elesys',metavar='ELESYS',default=None)
parser.add_option('-M', '--musys', dest='musys',
                  help='musys',metavar='MUSYS',default=None)
parser.add_option('', '--BRee', dest='BRee',
                  help='BRee',metavar='BREE',default=None)
parser.add_option('', '--BRem', dest='BRem',
                  help='BRem',metavar='BREM',default=None)
parser.add_option('', '--BRmm', dest='BRmm',
                  help='BRmm',metavar='BRMM',default=None)
parser.add_option('', '--BRMultiplier', dest='BRMultiplier',
                  help='BRMultiplier',metavar='BRMULTIPLIER',default=None)

(options, args) = parser.parse_args()

if options.sys == "False":
  DO_SYS = False

if options.elesys == "True":
  ELE_SYS = True

if options.musys == "True":
  MU_SYS = True


#-----------------
# Configuration
#-----------------
#lumi =  18232.8
lumi =  36074.56
#lumi =  33257.2 + 3212.96
#lumi =  33257.2 #+ 3212.96

# Control regions
plotsfile = []
if options.makeplot == "False":
  plotsfile.append("hists")
plotsfile.append(options.vname)
plotsfile.append(options.region)
plotsfile.append(options.tag)

for s in plotsfile:
  if not s: plotsfile.remove(s)

plotsfile = "_".join(plotsfile)+".root"
plotsfile = os.path.join(options.outdir,plotsfile)

ROOT.gROOT.SetBatch(True)
hm = histmgr.HistMgr(basedir=options.indir,target_lumi=lumi)

#-----------------
# Samples        
#-----------------

# base samples
data    = samples.all_data
mc_bkg  = samples.mc_bkg
'''
mc_bkg = [
  samples.dibosonSherpa221,
  samples.dibosonSysSample,
  samples.ttX,
  ]
  '''
fakes   = samples.fakes
signal  = samples.signal


#signal.append(samples_DCH.DCH500)
print(data)
# recombined samples
recom_data     = data[0].copy()
recom_mc_bkg  = [ b.copy() for b in mc_bkg ]
recom_sig     = [ s.copy() for s in samples.signal]

## signals
signal_samples = []

# xsecL = [82.677, 34.825, 16.704, 8.7528, 4.9001, 2.882, 1.7631, 1.10919, 0.72042, 0.476508, 0.32154, 0.21991, 0.15288, 0.107411, 0.076403, 0.0547825, 0.039656, 0.0288885, 0.021202, 0.0156347, 0.011632, 0.00874109, 0.0065092]
# masses = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250, 1300]
xsecL = [82.677, 34.825, 16.704, 8.7528, 4.9001, 2.882, 1.7631, 1.10919, 0.72042, 0.476508, 0.32154, 0.21991, 0.15288, 0.107411, 0.076403, 0.0547825, 0.039656, 0.0288885, 0.021202, 0.0156347, 0.011632, 0.00874109]
masses = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200, 1250]


#--------------
# Estimators
#--------------
'''
signalMassToPlots = [500,600,700]
BRsToPlot = [100]

BRMultiplier = [16,16,8,4,4,4]
#BRMultiplier = [1,1,1,1,1,1]

element = options.BRMultiplier

for s in samples.all_DCH.daughters:
  print BRMultiplier[int(element)]
  s.xsec = ( s.xsec * BRMultiplier[int(element)])
'''
"""
if options.signal == "True":
  print " signal is true"
  if float(BRee) > 0 and float(BRmm)+float(BRem)==0:

    print "ee"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(ee)=%d" % (mass,br)
        globals()[name+"ee"+str(br)+"mm"+str(100-br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(ee)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"ee"+str(br)+"mm"+str(100-br)] ]
        intiger += 1
        print "I should be adding signal"

  elif float(BRem) > 0 and float(BRmm)+float(BRee)==0:

    print "em"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(e#mu)=%d" % (mass,br)
        globals()[name+"em"+str(br)+"mm"+str(100-br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(e#mu)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"em"+str(br)+"mm"+str(100-br)] ]
        intiger += 1

  elif float(BRmm) > 0 and float(BRee)+float(BRem)==0:

    print "mm"

    for br in [10,50,100]:
      signal_samples += [[]]
      intiger = 1
      for mass,xsec in zip(masses,xsecL):
        if options.makeplot == "True":
          if mass not in signalMassToPlots or br not in BRsToPlot: continue
        name = "Pythia8EvtGen_A14NNPDF23LO_DCH%d" % mass
        print "tlatex: ", "DCH%d Br(#mu#mu)=%d" % (mass,br)
        globals()[name+"ee"+str(100-br)+"mm"+str(br)] = sample.Sample(
          name = name,
          tlatex = ("DCH%d Br(#mu#mu)=%d" % (mass,br)),
          line_color = intiger,
          marker_color = intiger,
          fill_color = intiger,
          line_width  = 3,
          line_style = 1,
          fill_style = 3004,
          xsec       = xsec/1000.,
          )
        signal_samples[len(signal_samples)-1] += [ globals()[name+"ee"+str(br)+"mm"+str(100-br)] ]
        intiger += 1

  else:
    print "working point ",BRee," ",BRem," ",BRem," not yet supported!"
"""


#--------------
# Estimators
#--------------
for s in mc_bkg + signal + data: 
    histmgr.load_base_estimator(hm,s)

main_addition_regions    = []
fake_addition_regions    = []
fake_subtraction_regions = []

reg_prefix, reg_suffix = funcs.get_pref_and_suff(options.region)

if reg_suffix == "MAINREG" or "TESTING":
  
  # including all regions for fake-factor method
  # ---------------------------------------------
  if options.fakest == "AllRegions":
    main_addition_regions = ["TT","TTT","TTTT"]
    
    fake_addition_regions = []
    fake_addition_regions += ["TL","LT"]
    fake_addition_regions += ["TTL","TLT","LTT"]
    fake_addition_regions += ["LLL"]
    fake_addition_regions += ["TTTL","TTLT","TLTT","LTTT"]

    fake_subtraction_regions = []
    fake_subtraction_regions += ["LL"]
    fake_subtraction_regions += ["LLT","LTL","TLL"]
  
  # only two lepton regions
  # ---------------------------------------------
  if options.fakest == "TwoLepRegions":
    
    main_addition_regions    = ["TT"]
    fake_addition_regions    = ["TL","LT"]
    fake_subtraction_regions = ["LL"]

  # only three lepton regions
  # ---------------------------------------------
  if options.fakest == "ThreeLepRegions":
    
    main_addition_regions = ["TTT"]
    
    fake_addition_regions = []
    fake_addition_regions += ["TTL","TLT","LTT"]
    fake_addition_regions += ["LLL"]

    fake_subtraction_regions = []
    fake_subtraction_regions += ["LLT","LTL","TLL"]

  if options.fakest== "FourLepRegions":
    main_addition_regions = ["TTTT"]
    
    fake_addition_regions = []
    fake_addition_regions += ["TTTL","TTLT","LTTT","TLTT"]

    fake_subtraction_regions = []
    fake_subtraction_regions += ["LLTT","LTTL","TLLT","TTLL","TLTL","LTLT"]

else:
  
  if options.fakest == "Subtraction":
    main_addition_regions =  fake_addition_regions = ["TTTT"]
    reg_prefix            =  options.region

'''
fakes.estimator = histmgr.AddRegEstimator(
      hm                  = hm, 
      sample              = fakes,
      data_sample         = data,
      mc_samples          = mc_bkg, 
      addition_regions    = ["_".join([reg_prefix]+[suffix]).rstrip("_") for suffix in fake_addition_regions],
      subtraction_regions = ["_".join([reg_prefix]+[suffix]).rstrip("_") for suffix in fake_subtraction_regions]
      )

'''
for s in recom_mc_bkg + recom_sig + [recom_data]:
  s.estimator = histmgr.AddRegEstimator(
      hm               = hm, 
      sample           = s,
      data_sample      = data,
      mc_samples       = mc_bkg + signal, 
      addition_regions = ["_".join([reg_prefix]+[suffix]).rstrip("_") for suffix in main_addition_regions]
      )

#-----------------
# Systematics       
#-----------------
# just an example ...
"""
mc_sys = [
    SYS1, 
    SYS2,
    ]
"""
## set mc systematics
#for s in mc_bkg + signals:
#    s.estimator.add_systematics(mc_sys)

#fakes.estimator.add_systematics(FF)

"""
if (DO_SYS):
  # fakes_mumu.estimator.add_systematics(FF)                                                                                                                                    
  if options.fakest == "ChargeFlip":
    chargeFlip.estimator.add_systematics(CF)
  if options.samples == "chargeflip":
    samples.Zee221.estimator.add_systematics(CF)
  if options.samples == "ZPeak":
    samples.Zee221.estimator.add_systematics(CF)
    samples.diboson_sherpa221.estimator.add_systematics(CF)
    samples.ttbar_Py8.estimator.add_systematics(CF)
    samples.singletop_inc.estimator.add_systematics(CF)
    samples.ttX.estimator.add_systematics(CF)
    samples.WenuPowheg.estimator.add_systematics(CF)
    samples.WtaunuPowheg.estimator.add_systematics(CF)
"""

mumu_vdict  = vars.vars_dict

#-----------------
# Plotting 
#-----------------
'''
## order backgrounds for plots
plot_ord_bkg = []
plot_ord_bkg.append( fakes )
plot_ord_bkg += recom_mc_bkg
'''
#plot_ord_bkg += recom_sig

#sys_list_ele = [BEAM, CHOICE, PDF, SCALE_Z, EG_RESOLUTION_ALL, EG_SCALE_ALLCORR, EG_SCALE_E4SCINTILLATOR, CF, TRIG, ID, ISO, RECO]
sys_list_ele = [EG_RESOLUTION_ALL, EG_SCALE_ALLCORR, EG_SCALE_E4SCINTILLATOR, CF, TRIG, ID, ISO, RECO]
sys_list_muon = [MUON_ID, MUON_MS, MUON_RESBIAS, MUON_RHO, MUON_SCALE, TRIGSTAT, TRIGSYS, ISOSYS, ISOSTAT, RECOSYS, RECOSTAT, TTVASYS, TTVASTAT]

if (DO_SYS):
  if ELE_SYS:
    fakes.estimator.add_systematics(FF)
  if MU_SYS:
    fakes.estimator.add_systematics(MUFF)
  for sample in mc_bkg:
    if sample in [samples.dibosonSysSample,samples.ttbar_Py8_up,samples.ttbar_Py8_do,samples.ttbar_Herwig,samples.ttbar_Py8_aMcAtNlo,samples.ttbar_Py8_CF]:
      print "skip sys MC samples in other systematics"
      continue
    if ELE_SYS:
      for sys in sys_list_ele:
        sample.estimator.add_systematics(sys)
    if MU_SYS:
      for sys in sys_list_muon:
        sample.estimator.add_systematics(sys)
  for sample in signal:
    if ELE_SYS:
      for sys in sys_list_ele:
        sample.estimator.add_systematics(sys)
    if MU_SYS:
      for sys in sys_list_muon:
        sample.estimator.add_systematics(sys)

if options.makeplot == "True":
 funcs.plot_hist(
    backgrounds   = recom_mc_bkg,
    signal        = recom_sig  if options.signal=="True" else None,   
    data          = recom_data,
    region        = options.region,
    label         = options.label,
    histname      = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
    xmin          = mumu_vdict[options.vname]['xmin'],
    xmax          = mumu_vdict[options.vname]['xmax'],
    rebin         = mumu_vdict[options.vname]['rebin'],
    rebinVar      = mumu_vdict[options.vname]['rebinVar'],
    log           = mumu_vdict[options.vname]['log'],
    icut          = int(options.icut),
    sys_dict      = sys_dict if DO_SYS else None,
    do_ratio_plot = True,
    save_eps      = True,
    plotsfile     = plotsfile,
    )

else:
 funcs.write_hist(
         backgrounds = plot_ord_bkg,
         signal        = recom_sig  if options.signal=="True" else None,
         #data        = recom_data,
         region      = options.region,
         icut        = int(options.icut),
         histname    = os.path.join(mumu_vdict[options.vname]['path'],mumu_vdict[options.vname]['hname']),
         rebin       = mumu_vdict[options.vname]['rebin'],
         rebinVar    = mumu_vdict[options.vname]['rebinVar'],
         sys_dict    = sys_dict if DO_SYS else None,         
         outname     = plotsfile,
         regName     = options.tag,
         rebinToEq   = True if options.rebinToEq=="True" else False,
         varName     = str(options.varName)
         )
 ## EOF



