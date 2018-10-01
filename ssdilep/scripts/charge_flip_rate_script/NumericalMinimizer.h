#ifndef NumericalMinimizer_H
#define NumericalMinimizer_H

#include "TH1.h"
#include "Math/Minimizer.h"
#include "TFile.h"


//-------------------------------------------------
// Numerical Minimizer Class ----------------------
//-------------------------------------------------
class NumericalMinimizer {

public:

	//Constructors
  
  NumericalMinimizer(TH1F* hOSCenter=nullptr, TH1F* hSSCenter=nullptr, TH1F* hOSSideband=nullptr, TH1F* hSSSideband=nullptr, double aa=1e9, double ptBins[]=nullptr, double etaBins[]=nullptr, int NetaBins = 0, int NptBins = 0);
  

	//Attributes
  TH1F* m_hOSCenter;
  TH1F* m_hSSCenter;
  TH1F* m_hOSSideband;
  TH1F* m_hSSSideband;

  
  double* m_ptBins;
  double* m_etaBins;

  const double m_constraint = 1e9;

  int m_NetaBins;
  int m_NptBins;

  ROOT::Math::Minimizer* m_min = nullptr;
  
  TH1D* m_flipRatePt = nullptr;
  TH1D* m_flipRateEta = nullptr;

  TFile* m_outFile = nullptr;
  

  //Methods

  ROOT::Math::Minimizer* NumericalMinimization1D(const char* minName = "Minuit2", const char* algoName = "MIGRAD" , int randomSeed = -1);
  
  double LogLikelihood1D(const double*);
  double LogLikelihood1Dfull(const double*);

};


#endif
