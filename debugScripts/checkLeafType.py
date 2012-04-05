#!/bin/env python

import ROOT as r

treeName = 'trigger'
fileName = '/tmp/gerbaudo/eos/data12_8TeV.00200804.physics_JetTauEtmiss.merge.NTUP_TRIG.x191_m1109/data12_8TeV.00200804.physics_JetTauEtmiss.merge.NTUP_TRIG.x191_m1109._0001.1.root'

inputFile = r.TFile.Open(fileName)
tree = inputFile.Get(treeName)

for leaf in tree.GetListOfLeaves() :
    ltype = leaf.GetTypeName()
    lname = leaf.GetName()
    if lname.startswith('v') : print lname
    if ltype.count('vector') > 2 :
        print "%s : %s" % (ltype, lname)
