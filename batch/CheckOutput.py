import os
from ssdilep.samples import samples

main_path = "/coepp/cephfs/mel/fscutti/ssdilep"

main_out = []
"""
main_out.append("HistAllVR1")
main_out.append("HistAllVR2")
main_out.append("HistAllVR3")
"""
main_out.append("HistNoteVR1")
main_out.append("HistNoteVR2")
main_out.append("HistNoteVR3")
main_out.append("HistNoteVR4")
main_out.append("HistNoteVR5")


main_type = []
main_type.append("nominal")
main_type.append("FF_UP")
main_type.append("FF_DN")

for outdir in main_out:
  msg1 = "Listing missing output for %s" % os.path.join(main_path,outdir)
  print "-" * len(msg1); print msg1; print "-" * len(msg1)

  missing_data = []
  missing_mc = []
  for typedir in main_type:
    msg2 = "appending for job type %s" % typedir
    print; print msg2; print ">" * len(msg2)

    file_list = os.listdir(os.path.join(main_path,outdir,typedir))
    for s in samples.all_data:
      if not s.name+".root" in file_list: 
        print s.name
        if not s.name in missing_data: missing_data.append(s.name)
    for s in samples.all_mc:
      if not s.name+".root" in file_list: 
        print s.name
        if not s.name in missing_mc: missing_mc.append(s.name)
  
  print; print "failed_data = ";print missing_data; print
  print; print "failed_mc = ";print missing_mc; print 








