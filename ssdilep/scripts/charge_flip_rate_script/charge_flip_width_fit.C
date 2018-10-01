#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TH1.h"
#include "TH2.h"
#include "TLegend.h"
#include "Fit/ParameterSettings.h"
#include "RooFit.h"
#include <iostream>

void charge_flip_width_fit(bool IsAS = 1){

  using namespace RooFit;

  TFile* Ztautau   = new TFile("/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_mc_tau.root");
  
  TH1D* hZtautau;
  
  if(IsAS == 1) {
  	 hZtautau = (TH1D*) Ztautau->Get("/regions/ZtautauAS/TwoTaus/event/h_taus_mTVis");
  }
  else if(IsAS == 0) {
  	 hZtautau = (TH1D*) Ztautau->Get("/regions/ZtautauSS/TwoSSTaus/event/h_taus_mTVis");
  }
  else {
  	cout << "Error!" << endl;
  	return;
  }
  			 

  double hmin = 40;
  double hmax = 100;



  // Declare observable x
  RooRealVar x("x","x",hmin,hmax) ;
  RooDataHist dh("dh","dh",x,Import(*hZtautau)) ;

  RooPlot* frame = x.frame(Title("Z mass")) ;
  dh.plotOn(frame,MarkerColor(2),MarkerSize(0.9),MarkerStyle(21));  //this will show histogram data points on canvas 
  dh.statOn(frame);  //this will display hist stat on canvas

  RooRealVar mean("mean","mean",95.0, 70.0, 120.0);
  RooRealVar width("width","width",5.0, 0.0, 120.0);
  RooRealVar sigma("sigma","sigma",5.0, 0.0, 120.0);
  RooGaussian gauss("gauss","gauss",x,mean,sigma);
  //RooBreitWigner gauss("gauss","gauss",x,mean,sigma);
  // RooVoigtian gauss("gauss","gauss",x,mean,width,sigma);

  RooFitResult* filters = gauss.fitTo(dh,"qr");
  gauss.plotOn(frame,LineColor(4));//this will show fit overlay on canvas 
  gauss.paramOn(frame); //this will display the fit parameters on canvas
  //filters->Print("v");

  // Draw all frames on a canvas
  TCanvas* c = new TCanvas("ZtautauASmassHisto","ZtautauASmassHisto",800,400) ;
  c->cd() ;
  gPad->SetLeftMargin(0.15);
           
  frame->GetXaxis()->SetTitle("Z mass (in GeV/c^{2})");
  frame->GetXaxis()->SetTitleOffset(1.2);
  //float binsize = Z_mass->GetBinWidth(1);
  char Bsize[50]; 
  //sprintf(Bsize,"Events per %2.2f",binsize);
  // frame->GetYaxis()->SetTitle(Bsize);  
  //frame->GetYaxis()->SetTitleOffset(1.2);
  frame->Draw() ;
  c->Print("myZmaa.eps");
  
  
}
