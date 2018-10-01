from histconfig import *


hist_list = []


# -------
# event
# -------
hist_list.append(h_taus_chargeprod)
hist_list.append(h_taus_dphi)
hist_list.append(h_taus_deta)
hist_list.append(h_taus_mTVis)
hist_list.append(h_taus_mTtot)
hist_list.append(h_taus_mCol)


# -------
# taus
# -------

# taulead
hist_list.append(h_taulead_pt)
hist_list.append(h_taulead_eta)
hist_list.append(h_taulead_phi)
hist_list.append(h_taulead_ntrk)


# tausublead
hist_list.append(h_tausublead_pt)
hist_list.append(h_tausublead_eta)
hist_list.append(h_tausublead_phi)
hist_list.append(h_tausublead_ntrk)
