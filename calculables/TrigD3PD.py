
import supy
import math,collections,bisect,itertools,re
import ROOT as r

class Tdt(supy.wrappedChain.calculable) :
    ""
    def __init__(self, treeName = "TrigConfTree", dirName = "triggerMeta") :
        self.treeNumber = None
        self.treeName = treeName
        self.dirName = dirName
    def update(self, _) :
        chain = self.source['chain'] # see supy.calculables.other
        self.cacheTdt(chain)
        self.value.GetEntry(self.source['entry'])
    def cacheTdt(self, chain) :
        treeNumber = chain.GetTreeNumber()
        if treeNumber != self.treeNumber :
            self.treeNumber = treeNumber
            confTree = chain.GetFile().Get("%s/%s"%(self.dirName, self.treeName))
            self.value = r.D3PD.PyTrigDecisionToolD3PD(chain, confTree)

class TriggerBit(supy.wrappedChain.calculable) :
    def __init__(self, trigName = "") :
        self.trigName = trigName
    def update(self, _) :
        self.value = self.source['Tdt'].IsPassed(self.trigName)
    @property
    def name(self):
        return self.trigName
class PassedTriggers(supy.wrappedChain.calculable) :
    def __init__(self,) :
        pass
    def update(self, _) :
        self.value = [x for x in self.source['Tdt'].GetPassedTriggers() ]

class Grlt(supy.wrappedChain.calculable) :
    def __init__(self, file='') :
        self.grlReader = r.Root.TGoodRunsListReader(file)
        self.grlReader.Interpret()
        self.grlIn = r.Root.TGoodRunsList(self.grlReader.GetMergedGoodRunsList())
        self.grlOut = r.Root.TGoodRunsList('outputGRL')
        self.value = self
    def update(self, _) :
        pass
class isGoodRun(supy.wrappedChain.calculable) :
    def __init__(self, runN='', lbn='' ) :
        self.runN = runN
        self.lbn = lbn
    def update(self, _) :
        run = self.source[self.runN]
        lbn = self.source[self.lbn]
        self.value = self.source['Grlt'].grlIn.HasRunLumiBlock(run, lbn)
        #print 'r %s l %s g %s' % (run, lbn, self.value)

class Indices(supy.wrappedChain.calculable) :
    """
    This is a calculable to build the collection of jets that have
    some pt min and eta max. It can be used also for other
    collections, as long as they have a pt and eta.
    """
    def __init__(self, collection = None, ptMin = None, etaMax = None):
        self.moreName = "pt>%f;|eta|<%f" % (ptMin, etaMax)
        for item in ["ptMin", "etaMax" ] :
            setattr(self, item, eval(item))
        self.fixes = collection
        self.stash(["pt", "eta"])

    def update(self, _) :
        pts = self.source[self.pt]  # prefix, suffix
        etas = self.source[self.eta]
        self.value = []
        for i in range(pts.size()):
            if pts.at(i)<self.ptMin: continue #put a break if too slow and coll is sorted
            if abs(etas.at(i))>self.etaMax: continue
            self.value.append(i)

class P4(supy.wrappedChain.calculable) :
    """
    Calculable to build Lorentz vectors from the standard D3PD collections.
    """
    def __init__(self, collection = None,):
        self.fixes = collection
        self.stash(["pt", "eta", "phi", "m"])
    def update(self, _) :
        self.value = [supy.utils.root.LorentzV(pt, eta, phi, m) for pt,eta,phi,m in zip(self.source[self.pt],
                                                                                        self.source[self.eta],
                                                                                        self.source[self.phi],
                                                                                        self.source[self.m])]

class M01(supy.wrappedChain.calculable) :
    """
    Calculable to compute the invariant mass of the first two objects
    in a collection.
    """
    def __init__(self, collection = None,):
        self.fixes = collection
        self.stash(["P4", "Indices"])
    def update(self, _) :
        P4 = self.source[self.P4]
        indices = self.source[self.Indices]
        jet0 = P4[indices[0]]
        jet1 = P4[indices[1]]
        self.value = (jet0+jet1).M()
        # self.value = sum([P4[indices[i]] for i in [0,1]]).M()
