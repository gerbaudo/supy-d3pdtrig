#!/bin/env python

import collections, operator
import ROOT as r
r.gROOT.SetBatch(1)

filename = '/tmp/user.chapleau.001130.EXT0._00082.NTUP.root'
filename = '/tmp/gerbaudo/dq2/user.chapleau.001130.EXT0._00082.NTUP.root'
treename = 'trigger'
confTreeName = 'triggerMeta/TrigConfTree'
maxEntries = 100

class L2jet(object):
    def __init__(self, E=0., eta=0., phi=0., inputType='', outputType='', roi=0) :
        self.E = E
        self.eta = eta
        self.phi = phi
        self.inputType = inputType
        self.outputType = outputType
        self.roi = roi
    def str(self):
        return '%4.1f %4.1f %4.1f %s %s %d' % (self.E,
                                               self.eta,
                                               self.phi,
                                               self.inputType,
                                               self.outputType,
                                               self.roi)
#____________________________________________________________

r.gROOT.ProcessLine('.x ../RootCore/scripts/load_packages.C+' )                     

inputFile = r.TFile.Open(filename)
tree = inputFile.Get(treename)
confTree = inputFile.Get(confTreeName)

tdt = r.D3PD.PyTrigDecisionToolD3PD( tree, confTree )

nEntries = tree.GetEntries()
crossCounts = collections.defaultdict(int)
for iEntry in xrange(nEntries):
    tree.GetEntry(iEntry)
    tdt.GetEntry(iEntry)
    passedTriggers = [x for x in tdt.GetPassedTriggers()]
    l2Triggers = [t for t in passedTriggers if t.startswith('L2')]
    #print [tree.trig_L2_jet_E,
    # tree.trig_L2_jet_eta,
    # tree.trig_L2_jet_phi,
    # tree.trig_L2_jet_InputType,
    # tree.trig_L2_jet_OutputType,
    # tree.trig_L2_jet_RoIWord]
    l2jets = [L2jet( E, eta, phi, it, ot, roi) 
              for E, eta, phi, it, ot, roi in zip(tree.trig_L2_jet_E,
                                                  tree.trig_L2_jet_eta,
                                                  tree.trig_L2_jet_phi,
                                                  tree.trig_L2_jet_InputType,
                                                  tree.trig_L2_jet_OutputType,
                                                  tree.trig_L2_jet_RoIWord)]
    # count duplicates in all jets
    processedRois = []
    duplicatededRois = []
    for j in l2jets:
        if j.roi in processedRois : duplicatededRois.append(j.roi)
        else : processedRois.append(j.roi)
    if iEntry<maxEntries :
        print "[%d] %s duplicated jets in total"%(iEntry, len(duplicatededRois))
        #print '\n'.join([j.str() for j in l2jets])
    
    # count duplicates in A4CC jets
    processedRois = []
    duplicatededRois = []
    roiCounts = collections.defaultdict(int)
    # sort the jets, easier to spot duplicates
    jetsA4cc = sorted([j for j in l2jets if str(j.inputType)=='NONE' and str(j.outputType)=='A4CC_JES'],
                      key = lambda j:j.E, reverse = True)
    for j in jetsA4cc:
        roiCounts[j.roi] += 1
        if j.roi in processedRois : duplicatededRois.append(j.roi)
        else : processedRois.append(j.roi)
    # the replication should be the same for all rois:
    duplicateFactors = list(set(roiCounts.values()))
    assert len(duplicateFactors) in [0, 1], 'duplicateFactors: %s'%duplicateFactors
    duplicateFactor = 0
    if not len(duplicateFactors) : continue
    duplicateFactor = duplicateFactors[0]
    if iEntry<maxEntries :
        print "[%d] %s duplicated jets in A4CC_JES"%(iEntry, len(duplicatededRois))
        print 'roi counts: ',roiCounts
        #print '\n'.join([j.str() for j in jetsA4cc if j.roi in duplicatededRois])
    for t1 in passedTriggers :
        for t2 in passedTriggers :
            key12 = "%s:%s"%(t1,t2)
            key21 = "%s:%s"%(t2,t1)
            crossCounts[key12] += duplicateFactor
            crossCounts[key21] += duplicateFactor
    #print l2Triggers
    #print [t for t in l2Triggers if 'a4cc' in t.lower()]
    if iEntry>maxEntries: break
#print crossCounts
topNduplTriggers = sorted(crossCounts.iteritems(), key=operator.itemgetter(1), reverse=True)[:40]
print topNduplTriggers
print 'max crossCounts',max(crossCounts.values())
