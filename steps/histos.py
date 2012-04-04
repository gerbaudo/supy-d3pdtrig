import ROOT as r
from supy import analysisStep
import supy

class deltaEta(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=-1.0,up=1.0,title="#Delta #eta") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem1.eta - elem2.eta, self.hName, self.N, self.low, self.up, title=self.title)
class deltaPhi(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=-1.0,up=1.0,title="#Delta #phi") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem1.phi - elem2.phi, self.hName, self.N, self.low, self.up, title=self.title)
class deltaR(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=0.0,up=1.0,title="#Delta R") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            j1lv = supy.utils.root.LorentzV(elem1.et(), elem1.eta, elem1.phi, 0.)
            j2lv = supy.utils.root.LorentzV(elem2.et(), elem2.eta, elem2.phi, 0.)
            self.book.fill(r.Math.VectorUtil.DeltaR(j1lv, j2lv), self.hName, self.N, self.low, self.up, title=self.title)
class deltaEt(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=-50.0,up=50.0,title="#Delta E_{T}") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem1.et() - elem2.et(), self.hName, self.N, self.low, self.up, title=self.title)
