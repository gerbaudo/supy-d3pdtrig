import collections, re
import supy
import ROOT as r

class triggerCounts(supy.analysisStep) :
    "histogram the counts for each trigger; based on susycaf.steps.trigger.triggerScan"
    def __init__(self, pattern = r'.*', passedTriggers = 'PassedTriggers') :
        self.pattern = pattern
        self.passedTriggers = passedTriggers
        self.moreName = self.pattern
        self.counts = collections.defaultdict(int)
    def varsToPickle(self) :
        return ['counts']
    def uponAcceptance(self, eventVars) :
        for key in eventVars[self.passedTriggers]:
            if not re.match(self.pattern,key): continue
            self.counts[key] += 1
    def mergeFunc(self, products) :
        self.counts = collections.defaultdict(int)
        for dct in products["counts"]:
            for key,value in dct.iteritems():
                self.counts[key] += value
        print self.counts
        names = sorted(self.counts.keys())
        hist = r.TH1D('triggerCounts',
                      "Trigger counts;;events",
                      len(names), 0, len(names))
        for i,name in enumerate(names) :
            hist.GetXaxis().SetBinLabel(i+1,name)
            hist.SetBinContent(i+1, self.counts[name])
        hist.Write()
            
            
         
class jetPt(supy.analysisStep) :
    # to be fixed
    def __init__(self, collection='') :
        self.collection = collection
    def uponAcceptance(self, eventVars) :
        jets = eventVars[self.collection]
        self.book.fill(jets,"%sPt"%self.collection, 50,275.0, 2775.0, title = ";H_{T} (GeV); jets/bin")
#        for jet in jets:
#            self.book.fill(jet.Et,"%sPt%s"%self.collection, 50,275.0, 2775.0, title = ";H_{T} (GeV); jets/bin")
