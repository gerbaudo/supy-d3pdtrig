
import supy
from math import cosh
from T2L1_RoIParser import inputOutputJetCounter

GeV = 1000.

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
    return ["n", "E", "pt", "m", "eta", "phi",
            "isUgly", "isBadLoose"]
def offlineJetCollection() :
    return ("jet_AntiKt4TopoEMJets_", "")
#___________________________________________________________
class IndicesL1(supy.wrappedChain.calculable) :
    "Build L1 jet indices; filter objects as needed"
    def __init__(self, collection = l1jetCollection()):
        self.fixes = collection
        self.stash(l1jetAttributes())
    @property
    def name(self):
        return 'IndicesL1Jets'
    def update(self, _) :
        self.value = range(self.source[self.n])
        # example filter:
        #self.value = [j for j in range(self.source[self.n]) if self.source[self.eta] > etamin]
class L1Jet(object) :
    def __init__(self, eta=0., phi=0., et4x4=0., et6x6=0., et8x8=0.):
        self.eta = eta
        self.phi = phi
        self.et4x4 = et4x4
        self.et6x6 = et6x6
        self.et8x8 = et8x8
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
    def __init__(self, collection = l2jetCollection(), minEt = None, input = None, output = None):
        self.minEt = minEt
        self.input = input
        self.output = output
        self.fixes = collection
        self.stash(l2jetAttributes()+["n"])
        self.moreName = ""
        if minEt!=None : self.moreName += "et>%.1f"%minEt
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
#___________________________________________________________
class IndicesEf(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), minEt = None, calibTag = None) :
        self.minEt = minEt
        self.calibTag = calibTag
        self.fixes = collection
        self.stash(efJetAttributes()+['n'])
        self.moreName = ""
        if minEt!=None : self.moreName += "et>%.1f"%minEt
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
            if self.calibTag and calibs.at(i) != self.calibTag : continue
            self.value.append(i)
        
class EfJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = efJetCollection(), indices = '') :
        self.indices = indices
        self.fixes = collection
        self.stash(efJetAttributes())
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

#___________________________________________________________
class IndicesOffline(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), minEt = None):
        self.minEt = minEt
        self.fixes = collection
        self.stash(offlineJetAttributes())
        self.moreName = ""
        if minEt!=None: self.moreName += "et>%.1f"%minEt
    @property
    def name(self):
        return 'IndicesOfflineJets'
    def update(self, _) :
        energies = self.source[self.E]
        etas = self.source[self.eta]
        self.value = []
        for i in range(self.source[self.n]):
            if self.minEt and energies.at(i)/cosh(etas.at(i)) < self.minEt: continue
            self.value.append(i)
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
#___________________________________________________________
class OfflineJet(object) :
    def __init__(self, E=0., pt=0., m=0., eta=0., phi=0., isUgly=0., isBadLoose=0.) :
        self.E = E
        self.pt = pt
        self.m = m
        self.eta = eta
        self.phi = phi
        self.isUgly = isUgly
        self.isBadLoose = isBadLoose
    def et(self) :
        return self.E/cosh(self.eta)
#___________________________________________________________
class OfflineJets(supy.wrappedChain.calculable) :
    def __init__(self, collection = offlineJetCollection(), minimumEt=10.*GeV):
        self.fixes = collection
        self.stash(offlineJetAttributes())
        self.minimumEt = minimumEt
    @property
    def name(self):
        return 'OfflineJets'
    def update(self, _) :
        self.value = [OfflineJet(E, pt, m, eta, phi, isUgly, isBadLoose)
                      for E, pt, m, eta, phi, isUgly, isBadLoose in
                      zip(self.source[self.E], self.source[self.pt],
                          self.source[self.m],
                          self.source[self.eta], self.source[self.phi],
                          self.source[self.isUgly], self.source[self.isBadLoose])
                      if E/cosh(eta)>self.minimumEt]

