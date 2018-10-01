#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "Fit/ParameterSettings.h"
#include "TH2.h"
#include "TLegend.h"
#include "TText.h"
#include "TRandom1.h"

#include "./NumericalMinimizer.h"

#include <iostream>


NumericalMinimizer::NumericalMinimizer (TH1F* hOSCenter, TH1F* hSSCenter, TH1F* hOSSideband, TH1F* hSSSideband, double aa, double etaBins[], double ptBins[], int NetaBins, int NptBins):
m_hOSCenter(hOSCenter),
m_hSSCenter(hSSCenter),
m_hOSSideband(hOSSideband),
m_hSSSideband(hSSSideband),
m_constraint(aa),
m_etaBins(etaBins),
m_ptBins(ptBins),
m_NetaBins(NetaBins),
m_NptBins(NptBins)
{
  
  m_etaBins = etaBins;
  m_ptBins = ptBins;
  
  std::cout << "NetaBins: " << m_NetaBins << " NptBins: " << m_NptBins << std::endl;
  cout << m_hOSCenter->GetNbinsX() << endl;
  if(m_hOSCenter->GetNbinsX()!=m_NetaBins*m_NetaBins*m_NptBins*m_NptBins){
    std::cout << "error: bins don't match" << std::endl;
  }
  else{
    std::cout << "number of bins seem to match the total number of bins: " << m_hOSCenter->GetNbinsX() << std::endl;
  }

  if(m_hOSSideband) {
    std::cout << "subtracting the OS sideband.." << std::endl;
    m_hOSCenter->Add(m_hOSSideband,-1);
  }
  if(m_hSSSideband) {
    std::cout << "subtracting the SS sideband.." << std::endl;
    m_hSSCenter->Add(m_hSSSideband,-1);
  }

  m_min = NumericalMinimization1D();
  
  ROOT::Fit::ParameterSettings pars;
  m_flipRatePt =  new TH1D( (std::string("flipRatePt")+hOSCenter->GetTitle()).c_str(), (std::string("flipRatePt")+hOSCenter->GetTitle()).c_str(), m_NptBins, &m_ptBins[0] );
  m_flipRateEta = new TH1D( (std::string("flipRateEta")+hOSCenter->GetTitle()).c_str(), (std::string("flipRateEta")+hOSCenter->GetTitle()).c_str(), m_NetaBins, &m_etaBins[0] );
 
  for (int eta = 0; eta < m_NetaBins; eta++){
    m_min->GetVariableSettings( eta, pars );
    if (m_etaBins[eta] >= 1.37 && m_etaBins[eta] < 1.52) {
      m_flipRateEta->SetBinContent(eta+1,0);
      m_flipRateEta->SetBinError(eta+1,0);      
    }
    else{
      m_flipRateEta->SetBinContent(eta+1,pars.Value());
      m_flipRateEta->SetBinError(eta+1,pars.StepSize());
    }
  }
  for (int pt = 0; pt < m_NptBins; pt++) {
    m_min->GetVariableSettings( m_NetaBins+pt, pars );
    m_flipRatePt->SetBinContent(pt+1,pars.Value());
    m_flipRatePt->SetBinError(pt+1,pars.StepSize());
  }
  
  m_flipRatePt->GetXaxis()->SetRangeUser(m_ptBins[0],m_ptBins[m_NptBins+1]);

  m_outFile = new TFile( (std::string("chargeFlipRates_")+hOSCenter->GetTitle()+std::string(".root")).c_str(), "RECREATE" );
  m_flipRatePt->Write();
  m_flipRateEta->Write();
  m_outFile->Close();
    
}

//-------------------------------------------------
// Log Likelihood    1Dx1D   approximation
//-------------------------------------------------
double NumericalMinimizer::LogLikelihood1D(const double *xx )
{
  double value = 0;
  for(int pt1 = 1; pt1 <= m_NptBins; pt1++) {
    for(int eta1 = 1; eta1 <= m_NetaBins; eta1++) {
      for(int pt2 = 1; pt2 <= m_NptBins; pt2++) {
        for(int eta2 = 1; eta2 <= m_NetaBins; eta2++){
          // totBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          int totBin = ( (pt1-1)*m_NetaBins + eta1 - 1 )*m_NptBins*m_NetaBins + ( (pt2-1)*m_NetaBins + eta2 ) + 1;
          value += -m_hSSCenter->GetBinContent(totBin) * log (xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1] ) 
          + m_hOSCenter->GetBinContent(totBin)*( xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1]  );
        }
      }
    }
  }
  double etaNorm = 0;
  for(int eta1 = 0; eta1 < m_NetaBins; eta1++) {
    if (m_etaBins[eta1] >= 1.37 && m_etaBins[eta1] < 1.52) continue;
    etaNorm += (m_etaBins[eta1+1]-m_etaBins[eta1])*xx[eta1];
  }
  return value + m_constraint*pow((etaNorm-1),2);
}

//-------------------------------------------------
// Log Likelihood    1Dx1D   full formula
//-------------------------------------------------
double NumericalMinimizer::LogLikelihood1Dfull(const double *xx )
{
  double value = 0;
  
  for(int pt1 = 1; pt1 <= m_NptBins; pt1++) {
    for(int eta1 = 1; eta1 <= m_NetaBins; eta1++) {
      for(int pt2 = 1; pt2 <= m_NptBins; pt2++) {
        for(int eta2 = 1; eta2 <= m_NetaBins; eta2++){
          // totBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          int totBin = ( (pt1-1)*m_NetaBins + eta1 - 1 )*m_NptBins*m_NetaBins + ( (pt2-1)*m_NetaBins + eta2 ) + 1;
          //if (m_hSSCenter->GetBinContent(totBin) < 0) m_hSSCenter->SetBinContent(totBin, 0);
          //if (m_hOSCenter->GetBinContent(totBin) < 0) m_hOSCenter->SetBinContent(totBin, 0);
          
          value += -m_hSSCenter->GetBinContent(totBin) * log( xx[eta1-1]*xx[m_NetaBins+pt1-1]*(1-xx[eta2-1]*xx[m_NetaBins+pt2-1]) + 
                                                              xx[eta2-1]*xx[m_NetaBins+pt2-1]*(1-xx[eta1-1]*xx[m_NetaBins+pt1-1]) ) 
          + m_hOSCenter->GetBinContent(totBin)*( xx[eta1-1]*xx[m_NetaBins+pt1-1]*(1-xx[eta2-1]*xx[m_NetaBins+pt2-1]) + 
                                                 xx[eta2-1]*xx[m_NetaBins+pt2-1]*(1-xx[eta1-1]*xx[m_NetaBins+pt1-1]) );
        }
      }
    }
  }
  double etaNorm = 0;
  for(int eta1 = 0; eta1 < m_NetaBins; eta1++) {
    if (m_etaBins[eta1] >= 1.37 && m_etaBins[eta1] < 1.52) continue;
    etaNorm += (m_etaBins[eta1+1]-m_etaBins[eta1])*xx[eta1];
  }
  return value + m_constraint*pow((etaNorm-1),2);
}




//-------------------------------------------------
// ROOT::Math::Minimizer --------------------------
//-------------------------------------------------
ROOT::Math::Minimizer* NumericalMinimizer::NumericalMinimization1D(const char * minName,
                          const char *algoName,
                          int randomSeed )
{
 ROOT::Math::Minimizer* min = ROOT::Math::Factory::CreateMinimizer(minName, algoName);

   min->SetMaxFunctionCalls(5e4); // for Minuit/Minuit2
   min->SetMaxIterations(1e9);  // for GSL
   min->SetTolerance(1e-9);
   min->SetPrintLevel(1);
   min->SetStrategy(2);

   auto func = &NumericalMinimizer::LogLikelihood1Dfull;
   ROOT::Math::Functor f(this,func,m_NetaBins+m_NptBins);

   min->SetFunction(f);

   int index = 0;
   double stepSize = 1e-6;
   for (int eta = 1; eta <= m_NetaBins; eta++){
    std::ostringstream name;
    name << "eta" << eta;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    index++;
  }
  for (int pt = 1; pt <= m_NptBins; pt++){
    std::ostringstream name;
    name << "pt" << pt;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    index++;
  }

  min->Minimize();

  return min;
}



