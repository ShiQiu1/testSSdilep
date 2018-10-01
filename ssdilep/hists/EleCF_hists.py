from histconfig import *


hist_list = []


# -------
# event
# -------

hist_list.append(h_electrons_chargeprod)
hist_list.append(h_electrons_dphi)
hist_list.append(h_electrons_deta)
hist_list.append(h_electrons_mVis)
hist_list.append(h_electrons_mTtot)

hist_list.append(h_electrons_chargeflip)

# -------
# electrons
# -------

# elelead
hist_list.append(h_elelead_pt)
hist_list.append(h_elelead_eta)
hist_list.append(h_elelead_phi)
hist_list.append(h_elelead_trkd0)
hist_list.append(h_elelead_trkd0sig)
hist_list.append(h_elelead_trkz0)
hist_list.append(h_elelead_trkz0sintheta)
#hist_list.append(h_elelead_ptvarcone30)

# elesublead
hist_list.append(h_elesublead_pt)
hist_list.append(h_elesublead_eta)
hist_list.append(h_elesublead_phi)
hist_list.append(h_elesublead_trkd0)
hist_list.append(h_elesublead_trkd0sig)
hist_list.append(h_elesublead_trkz0)
hist_list.append(h_elesublead_trkz0sintheta)
#hist_list.append(h_elesublead_ptvarcone30)


# EOF
