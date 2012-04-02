import ROOT as r
from supy import analysisStep

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
