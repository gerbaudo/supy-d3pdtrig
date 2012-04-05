#!/bin/env python

import ROOT as r



protocol = 'root://eosatlas/'
basedir = '/eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3466_r3467_p661/data11_7TeV.00189421.physics_EnhancedBias.merge.NTUP_TRIG.r3466_r3467_p661_tid754539_00/'
filenames = ['NTUP_TRIG.754539._000001.root.1',
             'NTUP_TRIG.754539._000002.root.1',
             'NTUP_TRIG.754539._000003.root.1',
             'NTUP_TRIG.754539._000004.root.1',
             'NTUP_TRIG.754539._000005.root.1',
             'NTUP_TRIG.754539._000006.root.1',
             ]

for fname in filenames :
    inputFile = r.TFile.Open(protocol+basedir+fname)
    metaDir = inputFile.Get('triggerMeta')
    if not metaDir :
        print 'missing metaDir for ',fname
        continue
    trigConfTree = metaDir.Get('TrigConfTree')
    if not trigConfTree :
        print 'missing TrigConfTree for ',fname
        continue
    print '%s TrigConfTree with %d entries'%(fname, trigConfTree.GetEntriesFast())
    inputFile.Close()
