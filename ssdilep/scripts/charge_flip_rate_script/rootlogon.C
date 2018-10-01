

void rootlogon()
{
  // Load ATLAS style
    
  gROOT->ProcessLine(".L ../atlasstyle-00-03-05/AtlasStyle.C+");  
  gROOT->ProcessLine(".L ../atlasstyle-00-03-05/AtlasLabels.C+");
  gROOT->ProcessLine(".L ../atlasstyle-00-03-05/AtlasUtils.C+");
  gROOT->ProcessLine(".L ./charge_flip_measurement.C+");
  gROOT->ProcessLine(".L ./NumericalMinimizer.cpp+");
  
  gROOT->ProcessLine("SetAtlasStyle()");
}
