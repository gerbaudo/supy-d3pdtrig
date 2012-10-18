
import supy
from math import cosh, fabs
from T2L1_RoIParser import inputOutputJetCounter
from l15Calib import emResidualEtCorrFactor, emJesEnergyCorrFactor
import ROOT as r

GeV = 1000.
GeV2MeV=1000.
MeV2GeV=0.001

def l1jetAttributes() :
    return ["n", "eta", "phi", "et4x4", "et6x6", "et8x8", ]
def l1jetCollection() :
    return (("trig_L1_jet_", ""))
def l2jetAttributes() :
    return ["E", "eta", "phi", "ehad0", "eem0",
            "nLeadingCells", "hecf", "jetQuality", "emf", "jetTimeCells",
            "RoIWord", "InputType", "OutputType"]
def l2jetCollection() :
    return ("trig_L2_jet_", "")
def efJetAttributes() :
    return ["E", "pt", "m", "eta", "phi", "calibtags",]
def efJetCollection() :
    return ("trig_EF_jet_", "")
def offlineJetAttributes() :
    return ["E", "pt", "m", "eta", "phi", "isUgly", "isBadLoose"]
def offlineJetCollection() :
    return ('jet_AntiKt4TopoEM_','') # sm
    #return ("jet_AntiKt4TopoNewEM_", "") # susy
    #return ("jet_AntiKt4TopoEMJets_", "")

#___________________________________________________________
class IndicesL1(supy.wrappedChain.calculable) :
    "Build L1 jet indices; filter objects as needed"
    def __init__(self, collection = l1jetCollection(), maxEta=None):
        self.fixes = collection
        self.stash(l1jetAttributes())
        self.maxEta = maxEta
        self.moreName = ""
        if maxEta : self.moreName += "|eta|<%.1f"%maxEta
    @property
    def name(self):
        return 'IndicesL1Jets'
    def update(self, _) :
        maxEta = self.maxEta
        etas = self.source[self.eta]
        self.value = [j for j in range(self.source[self.n])
                      if not maxEta or fabs(etas.at(i)) <= maxEta]

class L1Jet(object) :
    def __init__(self, eta=0., phi=0., et4x4=0., et6x6=0., et8x8=0.):
        self.eta = eta
        self.phi = phi
        self.et4x4 = et4x4
        self.et6x6 = et6x6
        self.et8x8 = et8x8
    @property
    def et(self) :
        return self.et8x8

class L1Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l1jetCollection(), minimumEt=10.*GeV):
        self.fixes = collection
        self.stash(l1jetAttributes())
        self.minimumEt = minimumEt
    @property
    def name(self):
        return 'L1Jets'
    def update(self, _) :
        self.value = [L1Jet(eta, phi, et4x4, et6x6, et8x8)
                      for eta, phi, et4x4, et6x6, et8x8 in
                      zip(self.source[self.eta], self.source[self.phi],
                          self.source[self.et4x4], self.source[self.et6x6], self.source[self.et8x8])
                      if et8x8>self.minimumEt]
#___________________________________________________________
class IndicesL2(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection(), minEt = None, maxEta=5.0, input = None, output = None):
        self.minEt = minEt
        self.maxEta = maxEta
        self.input = input
        self.output = output
        self.fixes = collection
        self.stash(l2jetAttributes()+["n"])
        self.moreName = ""
        if minEt!=None : self.moreName += "et>%.1f"%minEt
        if maxEta!=None: self.moreName += "|eta|<%.1f"%maxEta
        if input!=None : self.moreName += "%s"%input
        if output!=None : self.moreName += "%s"%output
    @property
    def name(self):
        return 'IndicesL2Jets%s%s'%(self.input if self.input else '',
                                    self.output if self.output else '')
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        inputs = self.source[self.InputType]
        outputs = self.source[self.OutputType]
        words = self.source[self.RoIWord]

        indices = []
        for i in range(self.source[self.n]):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt : continue
            if self.maxEta and fabs(etas.at(i))>self.maxEta : continue
            if self.input and inputs.at(i) != self.input : continue
            if self.output and outputs.at(i) != self.output : continue
            indices.append(i)

        self.value = self.filtered(indices, words)
    # tmp method used to remove duplicated (input not set for A4CC_JES when seeded by L1.5)
    def filtered(self, inList, inWords) :
        out = []
        usedWords = []
        for iJet in inList :
            word = inWords[iJet]
            if word in usedWords : continue
            usedWords.append(word)
            out.append(iJet)
        return out

# should I define a base class jet with eta,phi,et?
class HltJet(object) :
    def __init__(self, **kargs) :
        for k,v in kargs.iteritems() :
            setattr(self,k,v)
    @property
    def et(self) :
        return self.E/cosh(self.eta)

class L2Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection(), indices=''):
        self.indices = indices
        self.fixes = collection
        self.stash(l2jetAttributes())
    @property
    def name(self):
        return self.indices.replace("Indices","")
    def update(self, _) :
        self.value = []

        l2jetAttributeArrays = [self.source[getattr(self,x)] for x in l2jetAttributes()]
        jetIndices = self.source[self.indices]
        #print len(jetIndices),jetIndices
        for iJet in jetIndices :
            keys = l2jetAttributes()
            values = [x[iJet] for x in l2jetAttributeArrays]
            #kargs = {"E":3.4, "eta":2.5}
            kargs = dict(zip(keys, values))
            self.value.append(HltJet(**kargs))
        #lst = sorted([x.E for x in self.value])
        #print len(lst),lst
class L2JetsCalibL15(supy.wrappedChain.calculable) :
    "Take a L1.5 jet, and apply the L1.5 had calibration"
    def __init__(self, collection):
        self.collection = collection
    @property
    def name(self):
        return self.collection + "had"
    def update(self, _) :
        self.value = []
        l15UncalibratedJets = self.source[self.collection]
        keys = l2jetAttributes()
        for jet in l15UncalibratedJets :
            kargs = dict([(k,getattr(jet, k)) for k in keys])
            kargs['E'] *= emResidualEtCorrFactor(jet)
            emResidualCalibJet = HltJet(**kargs)
            kargs = dict([(k,getattr(emResidualCalibJet, k)) for k in keys])
            kargs['E'] *= emJesEnergyCorrFactor(emResidualCalibJet)
            self.value.append(HltJet(**kargs))
#___________________________________________________________
class IndicesEf(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), minEt = None, maxEta=5.0, calibTag = None) :
        self.minEt = minEt
        self.maxEta = maxEta
        self.calibTag = calibTag
        self.fixes = collection
        self.stash(efJetAttributes()+['n'])
        self.moreName = ""
        if minEt!=None : self.moreName += "et>%.1f"%minEt
        if maxEta!=None: self.moreName += "|eta|<%.1f"%maxEta
        if calibTag!=None : self.moreName += "%s"%calibTag
    @property
    def name(self):
        return 'IndicesEfJets%s'%(self.calibTag if self.calibTag else '')
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        calibs = self.source[self.calibtags]
        self.value = []
        for i in range(energies.size()):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt : continue
            if self.maxEta and fabs(etas.at(i))>self.maxEta : continue
            if self.calibTag and calibs.at(i) != self.calibTag : continue
            self.value.append(i)

def computeMinDr(jetCollection, drMinEt=None) :
    lv = supy.utils.root.LorentzV
    DeltaR = r.Math.VectorUtil.DeltaR
    for i, jet in enumerate(jetCollection) :
        minDr = None
        # using here LorentzV(pt,eta,phi,m) as (0.,eta,phi,0.); we only care about eta,phi.
        j1lv = lv(0., jet.eta, jet.phi, 0.)
        otherJets = jetCollection[:i] + jetCollection[i+1:]
        if drMinEt : otherJets = [j for j in otherJets if j.et>drMinEt]
        for j in otherJets :
            dr = DeltaR(j1lv, lv(0., j.eta, j.phi, 0.))
            if not minDr or minDr > dr : minDr = dr
        jet.minDr = minDr

class EfJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), indices = '', drMinEt=40.0*GeV) :
        self.indices = indices
        self.fixes = collection
        self.stash(efJetAttributes())
        self.drMinEt = drMinEt
    @property
    def name(self):
        return self.indices.replace("Indices","")
    def update(self, _) :
        self.value = []
        efjetAttributeArrays = [self.source[getattr(self,x)] for x in efJetAttributes()]
        jetIndices = self.source[self.indices]
        for iJet in jetIndices :
            keys = efJetAttributes()
            values = [x[iJet] for x in efjetAttributeArrays]
            kargs = dict(zip(keys, values))
            self.value.append(HltJet(**kargs))
        computeMinDr(self.value, self.drMinEt)

#___________________________________________________________
class IndicesOffline(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), minEt=10.0*GeV, maxEta=5.0, etSorted=True, tag='', attributesToSkip=[]):
        self.minEt = minEt
        self.maxEta = maxEta
        self.etSorted = etSorted
        self.tag = tag
        self.fixes = collection
        self.stash([a for a in offlineJetAttributes()+['n'] if a not in attributesToSkip])
        self.moreName = ""
        if minEt!=None : self.moreName += "E_T>%.1f"%minEt
        if maxEta!=None : self.moreName += "|eta|<%.1f"%maxEta
        if tag : self.moreName += tag
    @property
    def name(self):
        return 'IndicesOfflineJets'+self.tag

    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        self.value = []
        for i in range(self.source[self.n]):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt: continue
            if self.maxEta and fabs(etas.at(i))>self.maxEta : continue
            self.value.append(i)
        if self.etSorted : self.value = sorted([i for i in self.value], key = lambda i : energies.at(i)/cosh(etas.at(i)), reverse = True)
#___________________________________________________________
class IndicesOfflineBad(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection()) :
        self.fixes = collection
        self.stash(["isBadLoose"])
    def update(self, _) :
        self.value = []
        badLoose = self.source[self.isBadLoose]
        for i in range(badLoose.size()) :
            if badLoose.at(i)==1: self.value.append(i)
    @property
    def name(self):
        return "IndicesOfflineBadJets"

class OfflineJet(HltJet) :
    def __init__(self, **kargs) :
        super(OfflineJet, self).__init__(**kargs)
    @property
    def et(self) :
        return self.E/cosh(self.eta)

class OfflineJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), indices = 'IndicesOfflineJets', drMinEt=40.0*GeV, attributesToSkip=[]) :
        self.indices = indices
        self.attributesToSkip = attributesToSkip
        self.fixes = collection
        self.stash([a for a in offlineJetAttributes() if a not in attributesToSkip])
        self.drMinEt = drMinEt
        print self.name
    @property
    def name(self):
        return self.indices.replace("Indices","")
    def update(self, _) :
        self.value = []
        keys = [a for a in offlineJetAttributes() if a not in self.attributesToSkip]
        ofJetAttributeArrays = [self.source[getattr(self,x)] for x in keys]
        jetIndices = self.source[self.indices]
        for iJet in jetIndices :
            values = [x[iJet] for x in ofJetAttributeArrays]
            kargs = dict(zip(keys, values))
            self.value.append(OfflineJet(**kargs))
        computeMinDr(self.value, self.drMinEt)
#___________________________________________________________

class MatchedJets(supy.wrappedChain.calculable) :
    "Loop over coll1 and find the matches otherColls; requires et, eta, phi."
    def __init__(self, coll1 = None, otherColls = [], maxDr = 0.4) :
        self.coll1 = coll1
        self.otherColls = otherColls
        self.maxDr = maxDr
    @property
    def name(self):
        return "%sMatch%s"%(self.coll1, ''.join(self.otherColls))
    def update(self, _) :
        self.value = []
        jets1 = sorted([j for j in self.source[self.coll1]], key = lambda j:j.et, reverse = True)
        otherJets = [sorted([j for j in self.source[coll]], key = lambda j:j.et, reverse = True)
                     for coll in self.otherColls]
        # using here LorentzV(pt,eta,phi,m) as (et,eta,phi,0.), but we only care about eta,phi.
        for j1 in jets1:
            j1lv = supy.utils.root.LorentzV(j1.et, j1.eta, j1.phi, 0.)
            jetWithMatches = [j1]
            for jets2 in otherJets:
                matchedJet = None
                for j2 in jets2:
                    j2lv = supy.utils.root.LorentzV(j2.et, j2.eta, j2.phi, 0.)
                    if r.Math.VectorUtil.DeltaR(j1lv, j2lv) < self.maxDr :
                        matchedJet = j2
                        jets2.pop(jets2.index(j2)) # avoid double match and speed up
                        break
                jetWithMatches.append(matchedJet)
            self.value.append(tuple(jetWithMatches))

class UnmatchedJets(supy.wrappedChain.calculable) :
    "Take MatchedJets, and give you a collection of the jets that don't have any match"
    def __init__(self, coll = '') :
        self.coll = coll
    @property
    def name(self) : return "Unmatched%s"%self.coll
    def update(self, _) :
        self.value = [jets[0] for jets in self.source[self.coll] if not any(jets[1:])]

class EnergyL2Jets(supy.wrappedChain.calculable) :
    def __init__(self, collection = l2jetCollection(), input = None, output = None):
        self.input = input
        self.output = output
        self.fixes = collection
        self.stash(l2jetAttributes()+["n"])
    @property
    def name(self):
        return 'EnergyL2Jets%s%s'%(self.input if self.input else '',
                               self.output if self.output else '')
    def update(self, _) :
        allEnergies = self.source[self.E]
        inputs = self.source[self.InputType]
        outputs = self.source[self.OutputType]
        energies = []
        for i in range(self.source[self.n]):
            if self.input and inputs.at(i) != self.input : continue
            if self.output and outputs.at(i) != self.output : continue
            energies.append(allEnergies[i])

        self.value = energies
class SumEt(supy.wrappedChain.calculable) :
    "Sum Et for a given collection; requires et"
    def __init__(self, coll = None) :
        self.coll = coll
    @property
    def name(self):
        return "SumEt%s"%self.coll
    def update(self, _) :
        self.value = sum([j.et for j in self.source[self.coll]])
