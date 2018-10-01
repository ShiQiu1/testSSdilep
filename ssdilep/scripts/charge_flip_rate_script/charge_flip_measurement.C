#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "Fit/ParameterSettings.h"
#include "TH2.h"
#include "TLegend.h"
#include "TText.h"
#include "../atlasstyle-00-03-05/AtlasStyle.h"
#include "../atlasstyle-00-03-05/AtlasLabels.h"
#include "../atlasstyle-00-03-05/AtlasUtils.h"

#include "./NumericalMinimizer.h"

#include <iostream>


//*****************************  Charge flip measurment macro   *****************************'


void charge_flip_measurement(bool isEle = 0, bool checkProngedness = 0, double constraint = 1e6 ){




double ptBins[14] = {30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200.};
double etaBins[19] = {0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};
int NptBins = 13;
int NetaBins = 18;
/*


double ptBins[3]  = {20., 25., 40.}; 
double etaBins[6] = {0.0, 0.4, 0.8, 1.37, 1.52, 2.5};
int NptBins = 2;
int NetaBins = 5;



double ptBins[3]  = {20., 50}; 
double etaBins[5] = {0.0, 0.5, 1.37, 1.52, 2.5};
int NptBins = 1;
int NetaBins = 4;
*/
/*
double ptBins[6]  = {20., 25., 30., 40., 50.};
double etaBins[8] = {0.0, 0.3, 0.6, 1.0, 1.37, 1.52, 2.0, 2.5};
int NptBins = 4;
int NetaBins = 7;
*/

string file_path_data;
string file_path_mc;

  //****   Defining root file path    *******
  if(isEle) {
  	 file_path_data = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_data_exot12.root";
  	 file_path_mc = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_mc_exot12_full.root";//
  }
  
  else {
  	 file_path_data = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_mc_tau_CF_final.root";
  	 file_path_mc = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_mc_tau_CF_final.root";
  	
  }	

    
  std::string InputFileData = file_path_data;
  
  std::string InputFileMC = file_path_mc;
  
  TFile* OSCenterFile   = new TFile(InputFileData.c_str());
  TFile* OSSidebandFile = new TFile(InputFileData.c_str());
  TFile* SSCenterFile   = new TFile(InputFileData.c_str());
  TFile* SSSidebandFile = new TFile(InputFileData.c_str());
  
  TFile* OSCenterFileMC   = new TFile(InputFileMC.c_str());
  TFile* OSSidebandFileMC = new TFile(InputFileMC.c_str());
  TFile* SSCenterFileMC   = new TFile(InputFileMC.c_str());
  TFile* SSSidebandFileMC = new TFile(InputFileMC.c_str());
  
  
    
  //****   Associating input histograms to macro objects    *******
  
TH1F* hOSCenterData;  
TH1F* hOSCenterMC; 
TH1F* hSSCenterData; 
TH1F* hSSCenterMC;
TH1F* hOSSidebandData;
TH1F* hOSSidebandMC;
TH1F* hSSSidebandData;
TH1F* hSSSidebandMC;
 
 
 
if(isEle){
 hOSCenterData = (TH1F*) OSCenterFile->Get("/regions/ZWindowAS/ZMassWindowAS/event/h_electrons_chargeflip");
 hOSCenterMC   = (TH1F*) OSCenterFileMC->Get("/regions/ZWindowAS/ZMassWindowAS/event/h_electrons_chargeflip");
  
   hSSCenterData = (TH1F*) SSCenterFile->Get("/regions/ZWindowSS/TwoSSElectrons_ZMassWindowSS/event/h_electrons_chargeflip");
   hSSCenterMC   = (TH1F*) SSCenterFileMC->Get("/regions/ZWindowSS/TwoSSElectrons_ZMassWindowSS/event/h_electrons_chargeflip");
  
   hOSSidebandData = (TH1F*) OSSidebandFile->Get("/regions/ZWindowAS-Sideband/ZMassWindowASSideband/event/h_electrons_chargeflip");
   hOSSidebandMC   = (TH1F*) OSSidebandFileMC->Get("/regions/ZWindowAS-Sideband/ZMassWindowASSideband/event/h_electrons_chargeflip");
  
   hSSSidebandData = (TH1F*) SSSidebandFile->Get("/regions/ZWindowSS-Sideband/TwoSSElectrons_ZMassWindowSSSideband/event/h_electrons_chargeflip");
   hSSSidebandMC   = (TH1F*) SSSidebandFileMC->Get("/regions/ZWindowSS-Sideband/TwoSSElectrons_ZMassWindowSSSideband/event/h_electrons_chargeflip");
}

//______________    If tau variables    _________________________
else if (checkProngedness){

	 hOSCenterData = (TH1F*) OSCenterFile->Get("/regions/ZWindowAS-OnePronged/TauZMassWindowAS_OneProngedTaus/event/h_taus_chargeflip");
   hOSCenterMC   = (TH1F*) OSCenterFileMC->Get("/regions/ZWindowAS-ThreePronged/TauZMassWindowAS_ThreeProngedTaus/event/h_taus_chargeflip");
  
   hSSCenterData = (TH1F*) SSCenterFile->Get("/regions/ZWindowSS-Onepronged/TwoSSTaus_TauZMassWindowSS_OneProngedTaus/event/h_taus_chargeflip");
   hSSCenterMC   = (TH1F*) SSCenterFileMC->Get("/regions/ZWindowSS-Threepronged/TwoSSTaus_TauZMassWindowSS_ThreeProngedTaus/event/h_taus_chargeflip");
  
   hOSSidebandData = (TH1F*) OSSidebandFile->Get("/regions/ZWindowAS-Sideband-OnePronged/TauZMassWindowASSideband_OneProngedTaus/event/h_taus_chargeflip");
  hOSSidebandMC   = (TH1F*) OSSidebandFileMC->Get("/regions/ZWindowAS-Sideband-ThreePronged/TauZMassWindowASSideband_ThreeProngedTaus/event/h_taus_chargeflip");
  
   hSSSidebandData = (TH1F*) SSSidebandFile->Get("/regions/ZWindowSS-Sideband-OnePronged/TwoSSTaus_TauZMassWindowSSSideband_OneProngedTaus/event/h_taus_chargeflip");
   hSSSidebandMC   = (TH1F*) SSSidebandFileMC->Get("/regions/ZWindowSS-Sideband-ThreePronged/TwoSSTaus_TauZMassWindowSSSideband_ThreeProngedTaus/event/h_taus_chargeflip");  
  
} 

else {

	 hOSCenterData = (TH1F*) OSCenterFile->Get("/regions/ZWindowAS-OnePronged/TauZMassWindowAS/event/h_taus_chargeflip");
   hOSCenterMC   = (TH1F*) OSCenterFileMC->Get("/regions/ZWindowAS-OnePronged/TauZMassWindowAS/event/h_taus_chargeflip");
  
   hSSCenterData = (TH1F*) SSCenterFile->Get("/regions/ZWindowSS-Onepronged/TwoSSTaus_TauZMassWindowSS/event/h_taus_chargeflip");
   hSSCenterMC   = (TH1F*) SSCenterFileMC->Get("/regions/ZWindowSS-Onepronged/TwoSSTaus_TauZMassWindowSS/event/h_taus_chargeflip");
  
   hOSSidebandData = (TH1F*) OSSidebandFile->Get("/regions/ZWindowAS-Sideband-OnePronged/TauZMassWindowASSideband/event/h_taus_chargeflip");
  hOSSidebandMC   = (TH1F*) OSSidebandFileMC->Get("/regions/ZWindowAS-Sideband-OnePronged/TauZMassWindowASSideband/event/h_taus_chargeflip");
  
   hSSSidebandData = (TH1F*) SSSidebandFile->Get("/regions/ZWindowSS-Sideband-OnePronged/TwoSSTaus_TauZMassWindowSSSideband/event/h_taus_chargeflip");
   hSSSidebandMC   = (TH1F*) SSSidebandFileMC->Get("/regions/ZWindowSS-Sideband-OnePronged/TwoSSTaus_TauZMassWindowSSSideband/event/h_taus_chargeflip");  
  
}   
  
  





//**********   Write out if the chargeflip histograms are found in the histogram files    ******************************

  if(hOSCenterData) std::cout << "h_ZWindowOS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_data not found" <<std::endl;
  if(hOSCenterMC) std::cout << "h_ZWindowOS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_Zee not found" <<std::endl;
  
  if(hSSCenterData) std::cout << "h_ZWindowSS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_data not found" <<std::endl;
  if(hSSCenterMC) std::cout << "h_ZWindowSS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_Zee not found" <<std::endl;
  
  if(hOSSidebandData) std::cout << "h_ZWindowOS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_data not found" <<std::endl;
  if(hOSSidebandMC) std::cout << "h_ZWindowOS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_Zee not found" <<std::endl;
  
  if(hSSSidebandData) std::cout << "h_ZWindowSS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_data not found" <<std::endl;
  if(hSSSidebandMC) std::cout << "h_ZWindowSS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_Zee not found" <<std::endl;



//********    Start the charge flip measurment plot proction    *************************************

  std::cout << " Data charge-flip measurement " << std::endl;
  
  NumericalMinimizer* NM1 = new NumericalMinimizer(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData, constraint, etaBins, ptBins, NetaBins, NptBins); //Here the actual likliehood minimization is done 
  
  std::cout << " MC charge-flip measurement " << std::endl;
  NumericalMinimizer* NM2 = new NumericalMinimizer(hOSCenterMC,hSSCenterMC,hOSSidebandMC,hSSSidebandMC, constraint, etaBins, ptBins, NetaBins, NptBins);  
  
  
  cout << "Integral of Data: Eta histogram: " << NM1->m_flipRateEta->Integral("width") << " Pt histogram: " << NM1->m_flipRatePt->Integral("width") << endl;  
   
  cout << "Integral of MC:   Eta histogram: " << NM2->m_flipRateEta->Integral("width") << "  Pt histogram: " << NM2->m_flipRatePt->Integral("width") << endl;   
  
  
  
//*****    Total charge flip probability    *******

 
  
//Clear the over and Underflow bins, as they should be empty  
  NM1->m_flipRatePt->ClearUnderflowAndOverflow();
  NM2->m_flipRatePt->ClearUnderflowAndOverflow();
  



//******    Plots are done here    ************************

  
  NM2->m_flipRateEta->SetLineColor(kRed);
  NM2->m_flipRateEta->SetMarkerColor(kRed);
  NM2->m_flipRatePt->SetLineColor(kRed);
  NM2->m_flipRatePt->SetMarkerColor(kRed);
  
  
  // Defining the legend of the plots 
  TLegend* leg = new TLegend(0.20,0.600,0.4,0.725);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetTextSize(0.045);
if(!checkProngedness){
  leg->AddEntry(NM1->m_flipRateEta,"#font[42]{Data}","lpe0");
  leg->AddEntry(NM2->m_flipRateEta,"#font[42]{MC Z#rightarrow #tau#tau}","lpe0");
} 
else{
  leg->AddEntry(NM1->m_flipRateEta,"#font[42]{One-pronged}","lpe0");
  leg->AddEntry(NM2->m_flipRateEta,"#font[42]{Three-pronged}","lpe0");
}  



//****    f(eta) plot    ********

  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  
  //Drawing the f(eta) flip rate
  NM1->m_flipRateEta->Draw();
  NM1->m_flipRateEta->GetXaxis()->SetTitle("#eta");
  NM1->m_flipRateEta->GetYaxis()->SetTitle("f(#eta)");
  NM1->m_flipRateEta->GetYaxis()->SetRangeUser(1e-2,2.5);
  
 	NM2->m_flipRateEta->Draw("same");
  NM2->m_flipRateEta->SetLineColor(kRed);
  NM2->m_flipRateEta->SetMarkerColor(kRed);
  

  //Comparison plot code
  //std::vector<TH1D*> c1h1vec;
  //c1h1vec.push_back(NM2.m_flipRateEta);
  //drawComparison2(c1,&c1h1vec,NM1.m_flipRateEta,"f(#eta)","abs(#eta)",1e-2,20,0,2.47);
  

  
  //Drawing everything else
  //ATLASLabel(0.20,0.83,"Quite unofficial",1);
  //myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();

  
//*****   sigma(Pt) plot    **************  
  
  TCanvas* c2 = new TCanvas("c2","c2",600,600);
  c2->cd();
    
  NM1->m_flipRatePt->Draw();
  NM1->m_flipRatePt->GetXaxis()->SetTitle("p_{T} [GeV]");
  NM1->m_flipRatePt->GetYaxis()->SetTitle("#sigma(p_{T})");
  NM1->m_flipRatePt->GetYaxis()->SetRangeUser(1e-2,0.2);  
 

  NM2->m_flipRatePt->Draw("same");
  NM2->m_flipRatePt->SetLineColor(kRed);
  NM2->m_flipRatePt->SetMarkerColor(kRed);
  
  
  //ATLASLabel(0.20,0.83,"Very unofficial",1);
  //myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();



  TH1D* etaRatio = (TH1D*) NM1->m_flipRateEta->Clone();
  TH1D* ptRatio = (TH1D*) NM1->m_flipRatePt->Clone();

  etaRatio->Divide(NM2->m_flipRateEta);
  ptRatio->Divide(NM2->m_flipRatePt);

//*****    Save all produces graphs    *****************

  TFile *outfile = new TFile("chargeFlipRate.root","RECREATE");
  NM1->m_flipRateEta->SetName("dataEtaRate");
  NM1->m_flipRateEta->Write();
  NM1->m_flipRatePt->SetName("dataPtRate");
  NM1->m_flipRatePt->Write();
  
  NM2->m_flipRateEta->SetName("MCEtaRate");
  NM2->m_flipRateEta->Write();
  NM2->m_flipRatePt->SetName("MCPtRate");
  NM2->m_flipRatePt->Write();
  etaRatio->SetName("etaFunc");
  etaRatio->Write();
  ptRatio->SetName("ptFunc");
  ptRatio->Write();
  
  c1->Print("chargeFlipEta.eps");
  c2->Print("chargeFlipPt.eps");

  outfile->Close();

}
