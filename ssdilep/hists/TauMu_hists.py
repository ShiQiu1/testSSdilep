from histconfig import *


hist_list = []


# -------
# event
# -------
hist_list.append(h_tauMu_chargeprod)
hist_list.append(h_tauMu_dphi)
hist_list.append(h_tauMu_deta)
hist_list.append(h_tauMu_mTVis)
hist_list.append(h_tauMu_mTtot)
hist_list.append(h_tauMu_mCol)


# -------
# Taus
# -------

# taulead
hist_list.append(h_taulead_pt)
hist_list.append(h_taulead_eta)
hist_list.append(h_taulead_phi)
hist_list.append(h_taulead_ntrk)

# -------
# Muons
# -------

hist_list.append(h_mulead_pt)
hist_list.append(h_mulead_eta)
hist_list.append(h_mulead_phi)

