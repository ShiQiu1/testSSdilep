#include <map>
#include <utility>
#include <string>       // std::string
#include <iostream>     // std::cout
#include <sstream>      // std::ostringstream
#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TLatex.h"
#include "TLine.h"
#include "TLegend.h"
#include "TROOT.h"

void DCHSignalCombinedPlots(bool tauFlag) {
  gROOT->SetBatch(kTRUE);
  gStyle->SetOptStat(0);
 
  double m_dch[] = {300,400,500,600,700,800,900,1000,1100,1200,1300};
  
  //Integer to color the histogram lines
  int color = 1;
  
  //Validation Files
  std::map <std::string, TFile*> validationFiles;
  //Histograms
  std::map <std::string, TH1D*> h1;
  //std::map <std::string, TH1D*> h2;
  //std::map <std::string, TH1D*> h3;
  std::map <std::string, TH1D*> h4;
  std::map <std::string, TH1D*> h5;
  std::map <std::string, TH1D*> h6;
  std::map <std::string, TH1D*> h7;
  std::map <std::string, TH1D*> h8;
  std::map <std::string, TH1D*> h9;
  std::map <std::string, TH1D*> h10;
  std::map <std::string, TH1D*> h11;
  std::map <std::string, TH1D*> h12;
  std::map <std::string, TH1D*> h13;
  std::map <std::string, TH1D*> h14;

  TCanvas* c1 = new TCanvas("decayTypeC", "decayTypeC", 600, 400);
  //TCanvas* c2 = new TCanvas("leptonPairTypePC", "leptonPairTypePC", 600, 400);
  //TCanvas* c3 = new TCanvas("leptonPairTypeNC", "leptonPairTypeNC", 600, 400);
  TCanvas* c4 = new TCanvas("invariantMassPC", "invariantMassPC", 600, 400);
  TCanvas* c5 = new TCanvas("invariantMassNC", "invariantMassNC", 600, 400);
  TCanvas* c6 = new TCanvas("leadingPtPC", "leadingPtPC", 600, 400);
  TCanvas* c7 = new TCanvas("leadingPtNC", "leadingPtNC", 600, 400);
  TCanvas* c8 = new TCanvas("subLeadingPtPC", "subLeadingPtPC", 600, 400);
  TCanvas* c9 = new TCanvas("subLeadingPtNC", "subLeadingPtNC", 600, 400);
  TCanvas* c10 = new TCanvas("leadingEtaPC", "leadingEtaPC", 600, 400);
  TCanvas* c11 = new TCanvas("leadingEtaNC", "leadingEtaNC", 600, 400);
  TCanvas* c12 = new TCanvas("subLeadingEtaPC", "subLeadingEtaPC", 600, 400);
  TCanvas* c13 = new TCanvas("subLeadingEtaNC", "subLeadingEtaNC", 600, 400);
  TCanvas* c14 = new TCanvas("FinalStateLeptons", "Final State Leptons", 600, 400);

  TLegend* leg = new TLegend(0.15,0.57,0.48,0.88);
  leg->SetHeader("m(H^{++}) = 600 GeV");
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  TLegend* leg2 = new TLegend(0.62,0.57,0.94,0.88);
  leg2->SetHeader("m(H^{++}) = 600 GeV");
  leg2->SetFillStyle(0);
  leg2->SetBorderSize(0);
  TLegend* leg3 = new TLegend(0.38,0.58,0.68,0.93);
  leg3->SetHeader("m(H^{++}) = 600 GeV");
  leg3->SetFillStyle(0);
  leg3->SetBorderSize(0);
  std::cout << "hej" << std::endl; 
  TObject* nullPtr = NULL;  
  TLegend* legend = new TLegend(0.82,0.64,0.98,0.78);
  legend->AddEntry(nullPtr,"e  =  e/#tau_{e}    ","");
  legend->AddEntry(nullPtr,"m  =  #mu/#tau_{#mu}     ","");
  legend->AddEntry(nullPtr,"t  =  #tau_{had}    ","");
  
  for(int i = 0; i<=1; i++){
   
    // Open file
    ostringstream fileName;
    cout << tauFlag << endl;
    if (tauFlag == 1){
    cout << "hej" << endl;
		  if (i == 0) {
		  fileName << "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_signal_tau_fast_tau.root";
		  }
		  else{
		  
		  fileName << "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_signal_tau_full_tau.root";
		  } 
    }
    
    else {
    cout << "hejeeeee" << endl;
		  if (i == 0) {
		  fileName << "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_signal_tau_fast.root";
		  }
		  else{
		  
		  fileName << "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_signal_tau_full.root";
		  } 
    }
    
    
    
    validationFiles.insert( std::pair<std::string,TFile*>( fileName.str(), TFile::Open( fileName.str().c_str() ) ) );
    // Get Histogram Pointers
    h1.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get("regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/decayType/h_decayType" ) ) );
    
    h4.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/event/h_dilepton_mVis" ) ) );
    
    h5.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/collinear/h_dilep_mCol" ) ) );
    h6.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/event/h_dilepton_mTtot" ) ) );
    h7.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/event/h_dilepton_dphi" ) ) );
    h8.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/TwoLeptons/noCut_diLeptondPhiMoreThan005Pi/event/h_dilepton_deta" ) ) );
    h9.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/SignalComparison/noCut/signalComparison/h_nTau" ) ) );
   
    h10.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "regions/SignalComparison/noCut/met/h_met_trk_et" ) ) );
    /*
    h11.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "DCHValidationHistograms/LeadingEtaN" ) ) );
    h12.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "DCHValidationHistograms/SubLeadingEtaP" ) ) );
    h13.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "DCHValidationHistograms/SubLeadingEtaN" ) ) );
    h14.insert( std::pair<std::string,TH1D*>( fileName.str(), (TH1D*) validationFiles[ fileName.str().c_str() ]->Get( "DCHValidationHistograms/FinalStateLeptons" ) ) );
    */
     
    if(i==0) color = 1;
    else if(i==1) color = 2;
    else if(i==2) color = 3;
    else if(i==3) color = 4;
    else if(i==4) color = 5;
    else if(i==5) color = 6;
    else if(i==6) color = 7;
    else if(i==7) color = 8;
    else if(i==8) color = 9;
    else if(i==9) color = 28;
    else if(i==10) color = 46;
    
    
    
    if(i==0){
    //Decay  Type
      c1->cd();
      std::cout << fileName.str() << std::endl;
      h1[ fileName.str() ]->Draw();
      h1[ fileName.str() ]->SetLineColor(color);
      
      std::ostringstream test; test << "Fast sim, n = " << h1[ fileName.str() ]->GetEntries();
           
      leg->AddEntry( h1[ fileName.str() ], test.str().c_str(), "l");
      leg2->AddEntry( h1[ fileName.str() ], "Fast sim", "l");
   
  
			h1[ fileName.str() ]->SetNameTitle("DecayType","Leading Same-sign dilepton type");
			h1[ fileName.str() ]->GetYaxis()->SetTitle("Events");
			h1[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
		
			h1[ fileName.str() ]->GetXaxis()->SetLabelSize(0.06);
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(1,"2e");
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(2,"2m");
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(3,"2t");
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(4,"em");
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(5,"tm");
			h1[ fileName.str() ]->GetXaxis()->SetBinLabel(6,"te"); 
      
    
      
      
      //c2->cd();
      //h2[ fileName.str() ]->Draw();

      //c3->cd();
      //h3[ fileName.str() ]->Draw();

			//Invariant visible mass
      c4->cd();
      h4[ fileName.str() ]->Draw();
      h4[ fileName.str() ]->SetLineColor(color);
      h4[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h4[ fileName.str() ]->GetXaxis()->SetTitle("m((l/#tau_{had})#tau_{had}) [GeV]");
      std::ostringstream ppm; ppm << "Events/(" << h4[ fileName.str() ]->GetBinWidth(0) << " GeV)";
      h4[ fileName.str() ]->GetYaxis()->SetTitle(ppm.str().c_str());
      h4[ fileName.str() ]->SetTitle("Same-sign dilepton visible invariant mass");

      c5->cd();
      h5[ fileName.str() ]->Draw();
      h5[ fileName.str() ]->SetLineColor(color);
      h5[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h5[ fileName.str() ]->GetXaxis()->SetTitle("m_{col}((l/#tau_{had})#tau_{had}) [GeV]");
      std::ostringstream ppn; ppn << "Events/(" << h5[ fileName.str() ]->GetBinWidth(0) << " GeV)";
      h5[ fileName.str() ]->GetYaxis()->SetTitle(ppn.str().c_str());
      h5[ fileName.str() ]->SetTitle("Same-sign dilepton collinear invariant mass");

      c6->cd();
      h6[ fileName.str() ]->Draw();
      h6[ fileName.str() ]->SetLineColor(color);
      h6[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h6[ fileName.str() ]->GetXaxis()->SetTitle("m((l/#tau_{had})#tau_{had}p_{T}^{miss}) [GeV]");
      std::ostringstream pllp; pllp << "Events/(" << h6[ fileName.str() ]->GetBinWidth(0) << " GeV)";
      h6[ fileName.str() ]->GetYaxis()->SetTitle(pllp.str().c_str());
      
      h6[ fileName.str() ]->SetTitle("Same-sign dilepton total invariant mass");

      c7->cd();
      h7[ fileName.str() ]->Draw();
      h7[ fileName.str() ]->SetLineColor(color);
      h7[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h7[ fileName.str() ]->GetXaxis()->SetTitle("#Delta#phi");
      std::ostringstream nllp; nllp << "Events/(" << h7[ fileName.str() ]->GetBinWidth(0) << ")";
      h7[ fileName.str() ]->GetYaxis()->SetTitle(nllp.str().c_str());
      leg3->AddEntry( h7[ fileName.str() ], "Fast sim", "l");

      c8->cd();
      h8[ fileName.str() ]->Draw();
      h8[ fileName.str() ]->SetLineColor(color);      
      h8[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h8[ fileName.str() ]->GetXaxis()->SetTitle("#Delta#eta");
      std::ostringstream psllp; psllp << "events/(" << h8[ fileName.str() ]->GetBinWidth(0) << ")";
      h8[ fileName.str() ]->GetYaxis()->SetTitle(psllp.str().c_str());

      c9->cd();
      //Double_t scaleFast = 1/h9[ fileName.str() ]->Integral();
  		//h9[ fileName.str() ]->Scale(scaleFast);
      h9[ fileName.str() ]->Draw();
      h9[ fileName.str() ]->SetLineColor(color);
      h9[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h9[ fileName.str() ]->GetXaxis()->SetTitle("n_{#tau}");
      std::ostringstream nsllp; nsllp << "Events";
      h9[ fileName.str() ]->GetYaxis()->SetTitle(nsllp.str().c_str());
      
      h9[ fileName.str() ]->GetXaxis()->SetBinLabel(1,"0");
			h9[ fileName.str() ]->GetXaxis()->SetBinLabel(2,"1");
			h9[ fileName.str() ]->GetXaxis()->SetBinLabel(3,"2");
			h9[ fileName.str() ]->GetXaxis()->SetBinLabel(4,"3");
			h9[ fileName.str() ]->GetXaxis()->SetBinLabel(5,"4");
      
      
      h9[ fileName.str() ]->SetTitle("Number of #tau_{had} per event");

      c10->cd();
      h10[ fileName.str() ]->Draw();
      h10[ fileName.str() ]->SetLineColor(color);
      h10[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h10[ fileName.str() ]->GetXaxis()->SetTitle("p^{miss}_{T} [GeV]");
      h10[ fileName.str() ]->GetYaxis()->SetTitle("Events /(20 GeV)");
     
      
      h10[ fileName.str() ]->SetTitle("Missing momentum p^{miss}_T");
 /*     
      h10[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h10[ fileName.str() ]->GetXaxis()->SetTitle("#eta");
      std::ostringstream plle; plle << "Leptons/(" << h10[ fileName.str() ]->GetBinWidth(0) << " )";
      h10[ fileName.str() ]->GetYaxis()->SetTitle(plle.str().c_str());
      h10[ fileName.str() ]->GetYaxis()->SetRangeUser(0,1800);

      c11->cd();
      h11[ fileName.str() ]->Draw();
      h11[ fileName.str() ]->SetLineColor(color);
      h11[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h11[ fileName.str() ]->GetXaxis()->SetTitle("#eta");
      std::ostringstream nlle; nlle << "Leptons/(" << h11[ fileName.str() ]->GetBinWidth(0) << " )";
      h11[ fileName.str() ]->GetYaxis()->SetTitle(nlle.str().c_str());
      h11[ fileName.str() ]->GetYaxis()->SetRangeUser(0,1800);

      c12->cd();
      h12[ fileName.str() ]->Draw();
      h12[ fileName.str() ]->SetLineColor(color);
      h12[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h12[ fileName.str() ]->GetXaxis()->SetTitle("#eta");
      std::ostringstream pslle; pslle << "Leptons/(" << h12[ fileName.str() ]->GetBinWidth(0) << " )";
      h12[ fileName.str() ]->GetYaxis()->SetTitle(pslle.str().c_str());
      h12[ fileName.str() ]->GetYaxis()->SetRangeUser(0,1200);


      c13->cd();
      h13[ fileName.str() ]->Draw();
      h13[ fileName.str() ]->SetLineColor(color);      
      h13[ fileName.str() ]->GetYaxis()->SetTitleOffset(1.4);
      h13[ fileName.str() ]->GetXaxis()->SetTitle("#eta");
      std::ostringstream nslle; nslle << "Leptons/(" << h13[ fileName.str() ]->GetBinWidth(0) << " )";
      h13[ fileName.str() ]->GetYaxis()->SetTitle(nslle.str().c_str());
      h13[ fileName.str() ]->GetYaxis()->SetRangeUser(0,1200);
      */
    }
    else{
    
    	c1->cd();
  	  h1[ fileName.str() ]->Draw("same");
      h1[ fileName.str() ]->SetLineColor(color);
    	    	   		  
      
      
      std::ostringstream legName; legName << "Full sim";
      std::ostringstream test; test << "Full sim, n = " << h1[ fileName.str() ]->GetEntries();
      leg->AddEntry( h1[ fileName.str() ], test.str().c_str(), "l");
      leg2->AddEntry( h1[ fileName.str() ], legName.str().c_str(), "l");
      leg->Draw(); legend->Draw();
      
      c4->cd();
      h4[ fileName.str() ]->Draw("same");
      h4[ fileName.str() ]->SetLineColor(color);
      leg2->Draw();
      
      c5->cd();
      h5[ fileName.str() ]->Draw("same");
      h5[ fileName.str() ]->SetLineColor(color);
       leg2->Draw();
      c6->cd();
      h6[ fileName.str() ]->Draw("same");
      h6[ fileName.str() ]->SetLineColor(color);
      leg2->Draw();
      c7->cd();
      h7[ fileName.str() ]->Draw("same");
      h7[ fileName.str() ]->SetLineColor(color);
      leg3->AddEntry( h7[ fileName.str() ], "Full sim", "l");
      leg3->Draw();
      c8->cd();
      h8[ fileName.str() ]->Draw("same");
      h8[ fileName.str() ]->SetLineColor(color);
       leg2->Draw();
      
      c9->cd();
      //Double_t scaleFull = 1/h9[ fileName.str() ]->Integral();
      //h9[ fileName.str() ]->Scale(scaleFull);
      h9[ fileName.str() ]->Draw("same");
      h9[ fileName.str() ]->SetLineColor(color);
       leg2->Draw();
      
      c10->cd();
      h10[ fileName.str() ]->Draw("same");
      h10[ fileName.str() ]->SetLineColor(color);
      leg2->Draw();
      /*
      c11->cd();
      h11[ fileName.str() ]->Draw("same");
      h11[ fileName.str() ]->SetLineColor(color);
      if(i==10) leg->Draw();
      c12->cd();
      h12[ fileName.str() ]->Draw("same");
      h12[ fileName.str() ]->SetLineColor(color);
      if(i==10) leg->Draw();
      c13->cd();
      h13[ fileName.str() ]->Draw("same");
      h13[ fileName.str() ]->SetLineColor(color);
      if(i==10) leg->Draw();
      
      c14->cd();
      h14[ fileName.str() ]->Draw("same");
      h14[ fileName.str() ]->SetLineColor(color);
      if(i==10) leg->Draw(); legend->Draw();
      */
    }

  }
  std::cout << "hej3" << std::endl;
  c1->Print("DCH_DecayType.pdf");
  //c2->Print();
  //c3->Print();
  
  c4->Print("DCH_VisibleMass.pdf");
  
  c5->Print("DCH_CollinearMass.pdf");
  c6->Print("DCH_TotalMass.pdf");
  c7->Print("DCH_dPhi.pdf");
  c8->Print("DCH_dEta.pdf");
 
  c9->Print("DCH_nTau.pdf");
   
  c10->Print("DCH_met.pdf");
  /*
  c11->Print("ValidationPlots/GeneralPlots/DCH_LeadingEtaN.pdf");
  c12->Print("ValidationPlots/GeneralPlots/DCH_SubLeadingEtaP.pdf");
  c13->Print("ValidationPlots/GeneralPlots/DCH_SubLeadingEtaN.pdf");
  c14->Print("ValidationPlots/GeneralPlots/DCH_FinalStateLeptons.pdf");
*/
}
