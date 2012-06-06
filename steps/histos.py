import ROOT as r
from supy import analysisStep
import supy
from math import fabs, pi

# for all the deltas, the first value is the reference one, so
# delta = val_i+1 - val_1
# deltaFrac = (val_i+1 - val_1)/val_1

MeV2GeV = 1.0e-3
def phi_mpi_pi(value) :
    "same as r.Math.GenVector.VectorUtil.Phi_mpi_pi (for some reason cannot import it...)"
    pi = r.TMath.Pi()
    if value > pi and value <= pi:
        return value
    while value <= -pi: value = value+2.*pi
    while value >  +pi: value = value-2.*pi
    return value
class attribute(analysisStep) :
    def __init__(self, attrName='', coll='', nX=100,xLo=-5.0,xUp=5.0,title="") :
        for item in ['attrName', 'coll','nX','xLo','xUp','title'] : setattr(self,item,eval(item))
        self.hName = '%s_%s'%(coll,attrName)
    def uponAcceptance(self, eventVars) :
        coll = eventVars[self.coll]
        for elem in coll :
            self.book.fill(getattr(elem,self.attrName), self.hName, self.nX, self.xLo, self.xUp, title=self.title)
class deltaEta(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=-0.5,up=+0.5,title="#Delta #eta") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem2.eta - elem1.eta, self.hName, self.N, self.low, self.up, title=self.title)
class deltaPhi(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=-0.5,up=+0.5,title="#Delta #phi") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'delta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            self.book.fill(elem2.phi - elem1.phi, self.hName, self.N, self.low, self.up, title=self.title)
class deltaR(analysisStep) :
    def __init__(self, matchCollPair='', var='',N=100,low=0.0,up=0.5,title="#Delta R") :
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
            self.book.fill(MeV2GeV*(elem2.et() - elem1.et()), self.hName, self.N, self.low, self.up, title=self.title)
class deltaEtFrac(analysisStep) :
    # todo: merge it with deltaEt
    def __init__(self, matchCollPair='', var='',N=200,low=-5.0,up=5.0,title="#Delta E_{T}/E_{T}") :
        for item in ['matchCollPair', 'var','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'fracDelta%s%s'%(var,matchCollPair)
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for pair in matchCollPair :
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 or not elem2 : continue
            et1, et2 = elem1.et(), elem2.et()
            if et1 :
                self.book.fill((et2-et1)/et1, self.hName, self.N, self.low, self.up, title=self.title)

class etaPhiMap(analysisStep) :
    def __init__(self, coll='', nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-pi,yUp=+pi,title="") :
        for item in ['coll','nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'etaPhiMap%s'%coll
    def uponAcceptance(self, eventVars) :
        coll = eventVars[self.coll]
        for elem in coll :
            self.book.fill((elem.eta, phi_mpi_pi(elem.phi)),
                           "%s_eta_phi"%self.coll,
                           (self.nX, self.nY), (self.xLo, self.yLo), (self.xUp, self.yUp),
                           title="%s;#eta;#phi"%self.title)

class deltaEtaVsEtaMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-0.5,yUp=+0.5,title="") :
        for item in ['matchCollPair','nTh','nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtaVsEtaMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "%s;#eta; #Delta #eta"%self.hName
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one best precision (reference)
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            self.book.fill((elem1.eta, elem1.eta-elem2.eta),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title=self.title)
class deltaEtFracVsEtaMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=-5.0,xUp=5.0,nY=100,yLo=-5.0,yUp=+5.0,title="") :
        for item in ['matchCollPair', 'nTh', 'nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFracVsEtFracMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "%s;#eta; #Delta E_{T}/E_{T}"%self.hName
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one best precision (reference)
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            etRef = elem1.et()
            if not etRef : continue
            self.book.fill((elem1.eta, (elem2.et() - etRef)/etRef),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title="%s;#eta; #Delta E_{T}/E_{T}"%self.hName if not self.title else self.title)

class deltaEtFracVsMinDrMap(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, nX=100,xLo=0.,xUp=5.0,nY=100,yLo=-5.0,yUp=+5.0,title="") :
        for item in ['matchCollPair', 'nTh', 'nX','xLo','xUp','nY','yLo','yUp','title'] : setattr(self,item,eval(item))
        self.hName = 'deltaEtFracVsMinDrMap%s%s'%(matchCollPair, "_%dthJet"%nTh if nTh else "")
        if not self.title : self.title = "#Delta(E_{t})/E_{T} %s;#min #Delta R; #Delta E_{T}/E_{T}"%("" if not nTh else "%dth jet"%(nTh+1))
    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            # the first collection is the one with minDr
            elem1 = pair[0]
            elem2 = pair[1]
            if not elem1 : continue
            if not elem2 : continue
            etRef = elem1.et()
            self.book.fill((elem1.minDr, (elem2.et() - etRef)/etRef),
                           self.hName,
                           (self.nX, self.nY),
                           (self.xLo, self.yLo),
                           (self.xUp, self.yUp),
                           title=self.title)

class matchingEffVsEt(analysisStep) :
    def __init__(self, matchCollPair='', nTh=None, N=100,low=0.0,up=100.0,title="matching efficiency vs. E_{T}") :
        for item in ['matchCollPair','nTh','N','low','up','title'] : setattr(self,item,eval(item))
        self.hName = 'matchingEffVsEt%s%s'%(matchCollPair,"_%dthJet"%nTh if nTh else "")
        self.numTitle = 'num_%s'%self.hName
        self.denTitle = 'den_%s'%self.hName
        self.effTitle = 'eff_%s'%self.hName

    def uponAcceptance(self, eventVars) :
        matchCollPair = eventVars[self.matchCollPair]
        for i,pair in enumerate(matchCollPair) :
            if self.nTh and not self.nTh==i : continue
            elem1 = pair[0]
            elem2 = pair[1]
            # the first collection is the one with higher eff (denominator)
            if not elem1 : continue
            self.book.fill(MeV2GeV*elem1.et(), self.denTitle, self.N, self.low, self.up, title="denominator: %s;E_{T};jets"%self.denTitle)
            if not elem2 : continue
            self.book.fill(MeV2GeV*elem1.et(), self.numTitle, self.N, self.low, self.up, title="numerator: %s;E_{T};jets"%self.numTitle)
    def mergeFunc(self, products) :
        num = r.gDirectory.Get(self.numTitle)
        den = r.gDirectory.Get(self.denTitle)
        if not num and den : return
        eff = num.Clone(self.effTitle)
        eff.SetTitle(self.title)
        eff.Divide(num,den,1,1,"B")
        for bin in [0,self.N+1] :
            eff.SetBinContent(bin,0)
            eff.SetBinError(bin,0)
        eff.Write()

class turnOnJet(analysisStep) :
    def __init__(self, jetColl='', trigger='', passedTriggers='PassedTriggers', nTh=None,
                 emulated=False,
                 drMin=None, drMax=None, drAnyjet=None,
                 etaMin=None, etaMax=None,
                 N=100,low=0.0,up=100.0,title='') :
        requiredPars = ['jetColl', 'trigger', 'passedTriggers', 'nTh', 'emulated']
        filterPars = ['drMin', 'drMax', 'drAnyjet', 'etaMin', 'etaMax']
        histPars = ['N','low','up','title']
        for item in requiredPars + filterPars + histPars : setattr(self,item,eval(item))
        self.hName = ('turnOn%s%s'%(trigger, jetColl)
                      +("_%dthJet"%nTh if nTh else "")
                      +('_'.join(['']+['%s_%.1f'%(k,v) for k,v in
                                       zip(filterPars,
                                           [getattr(self,x) if hasattr(self,x) else None for x in filterPars]) if v])))
        self.numName = 'num_%s'%self.hName
        self.denName = 'den_%s'%self.hName
        self.effName = 'eff_%s'%self.hName
        if not self.title :
            reqLabel = ', '.join(['%s=%.1f'%(k,v) for k,v in zip(filterPars, [getattr(self,x) if hasattr(self,x) else None for x in filterPars]) if v])
            self.title = "%s efficiency %s; %sth jet E_{T} [GeV];eff"%(trigger, "" if not reqLabel else "(%s)"%reqLabel, nTh+1)
    def uponAcceptance(self, eventVars) :
        jetColl = eventVars[self.jetColl]
        if self.nTh >= len(jetColl) : return
        jet = jetColl[self.nTh]
        if self.drAnyjet and self.drMin and any(j.minDr and j.minDr > self.drMin for j in jetColl) : return
        if self.drAnyjet and self.drMax and any(j.minDr and j.minDr > self.drMax for j in jetColl) : return
        if self.drMin and jet.minDr and jet.minDr < self.drMin : return
        if self.drMax and jet.minDr and jet.minDr > self.drMax : return
        if self.etaMin and fabs(jet.eta) < self.etaMin : return
        if self.etaMax and fabs(jet.eta) > self.etaMax : return
        jetEt = jet.et()*MeV2GeV
        self.book.fill(jetEt, self.denName, self.N, self.low, self.up, title="denominator: %s;E_{T};jets"%self.denName)
        if self.trigger in eventVars[self.passedTriggers] \
               or \
               self.emulated and eventVars[self.trigger] :
            self.book.fill(jetEt, self.numName, self.N, self.low, self.up, title="numerator: %s;E_{T};jets"%self.numName)
    def mergeFunc(self, products) :
        num = r.gDirectory.Get(self.numName)
        den = r.gDirectory.Get(self.denName)
        if not num and den : return
        eff = num.Clone(self.effName)
        eff.SetTitle(self.title)
        eff.Divide(num,den,1,1,"B")
        for bin in [0,self.N+1] :
            eff.SetBinContent(bin,0)
            eff.SetBinError(bin,0)
        eff.Write()
