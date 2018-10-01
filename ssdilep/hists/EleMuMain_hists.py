from histconfig import *


hist_list = []


# -------
# event
# -------
hist_list.append(h_averageIntPerXing)
hist_list.append(h_actualIntPerXing)
#hist_list.append(h_correct_mu)
hist_list.append(h_NPV)
hist_list.append(h_nmuons)
hist_list.append(h_nelectrons)
hist_list.append(h_njets)
hist_list.append(h_nbjets)
hist_list.append(h_elemu_chargeprod)
hist_list.append(h_elemu_dphi)
hist_list.append(h_elemu_deta)
hist_list.append(h_elemu_dR)
hist_list.append(h_elemu_pTH)
hist_list.append(h_elemu_sumpT)
hist_list.append(h_elemu_mVis)
hist_list.append(h_elemu_mTtot)

# -------
# electrons
# -------

# leading lep
hist_list.append(h_leplead_pt)
hist_list.append(h_leplead_eta)
hist_list.append(h_leplead_phi)
hist_list.append(h_leplead_trkd0)
hist_list.append(h_leplead_trkd0sig)
hist_list.append(h_leplead_trkz0)
hist_list.append(h_leplead_trkz0sintheta)
hist_list.append(h_leplead_ptvarcone30)

# subleading lep
hist_list.append(h_lepsublead_pt)
hist_list.append(h_lepsublead_eta)
hist_list.append(h_lepsublead_phi)
hist_list.append(h_lepsublead_trkd0)
hist_list.append(h_lepsublead_trkd0sig)
hist_list.append(h_lepsublead_trkz0)
hist_list.append(h_lepsublead_trkz0sintheta)
hist_list.append(h_lepsublead_ptvarcone30)

hist_list.append(h_elelead_pt)
hist_list.append(h_elelead_eta)
hist_list.append(h_elelead_phi)
hist_list.append(h_elelead_trkd0)
hist_list.append(h_elelead_trkd0sig)
hist_list.append(h_elelead_trkz0)
hist_list.append(h_elelead_trkz0sintheta)
hist_list.append(h_elelead_ptvarcone30)

hist_list.append(h_mulead_pt)
hist_list.append(h_mulead_eta)
hist_list.append(h_mulead_phi)
hist_list.append(h_mulead_trkd0)
hist_list.append(h_mulead_trkd0sig)
hist_list.append(h_mulead_trkz0)
hist_list.append(h_mulead_trkz0sintheta)
hist_list.append(h_mulead_ptvarcone30)
# -------
# MET
# -------
hist_list.append(h_met_clus_et)
hist_list.append(h_met_clus_phi)
hist_list.append(h_met_trk_et)
hist_list.append(h_met_trk_phi)
hist_list.append(h_met_clus_sumet)
hist_list.append(h_met_trk_sumet)

#hist_list.append(h_elelead_Origin_vs_Type)
#hist_list.append(h_mulead_Origin_vs_Type)
#hist_list.append(h_elejet_deta)
#hist_list.append(h_elejet_dphi)
#hist_list.append(h_elebjet_deta)
#hist_list.append(h_elebjet_dphi)
#hist_list.append(h_mujet_deta)
#hist_list.append(h_mujet_dphi)
#hist_list.append(h_mubjet_deta)
#hist_list.append(h_mubjet_dphi)

# EOF






