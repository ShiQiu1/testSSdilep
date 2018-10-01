from histconfig import *


hist_list = []


# -------
# event
# -------

hist_list.append(h_oneProngedTauTruthCF_eta_pT)
hist_list.append(h_threeProngedTauTruthCF_eta_pT)

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
