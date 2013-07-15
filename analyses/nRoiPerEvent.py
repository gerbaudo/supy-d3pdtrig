#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV


class size(supy.wrappedChain.calculable) :
    @property
    def name(self) : return self.label+'size'
    def __init__(self, label = '') :
        self.label = label
    def update(self, ignored) :
        self.value = len(self.source[self.label])

class nRoiPerEvent(supy.analysis) :
    l2JetsIo = {
        'l2ps'   : ('A4TT','A4CC_JES'),
        'l15'    : ('NONE','A4TT'),
        'l15had' : ('NONE','A4TThad'),
        'l2cone' : ('A4TT','L2CONE'),
        }
    def otherTreesToKeepWhenSkimming(self) : return []

    def parameters(self) :
        efJetCalibTag='AntiKt4_topo_calib_EMJES'
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 2.8, #3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v51-pro13-04_CoolRunQuery-00-04-08_All_Good.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : 'EF_4j80_a4tchad_L2FS',
                'skim' : 'L1_4J15',
                'offJetColl' : 'OfflineJets',
                'efJetCalibTag' : efJetCalibTag,
                'efJetColl' : "EfJets%s"%efJetCalibTag,
                'l2psJetColl' : 'L2JetsA4TTA4CC_JES',
                'l15JetColl' : 'L2JetsNONEA4TT',
                'l2coneJetColl': 'L2JetsA4TTL2CONE',
                }
    def listOfSteps(self,config) :
        pars = self.parameters()
        etaMaxB=0.7 # barrel
        etaMaxG=1.5 # gap
        offJetColl = pars['offJetColl']
        refJetColl = offJetColl
        refJetCollLabel = 'OfflineJets'
        l2JetsIo = self.l2JetsIo
        efJetCalibTag = pars['efJetCalibTag']
        filterMult, histoMult = supy.steps.filters.multiplicity, supy.steps.histos.multiplicity
        histoVal, histoGen = supy.steps.histos.value, supy.steps.histos.generic
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers(["L1_4J15"]),
            filterMult("vxp_Indices",min=1),
            filterMult("IndicesOfflineJets",min=1),
            filterMult("IndicesOfflineBadJets",max=0),
            steps.filters.triggers([pars['refTrigger']]),
            ]
        ojC = ['L1Jets'] #+ ["L2Jets%s%s"%(i,o) for i,o in l2JetsIo.values()] + ["EfJets%s"%efJetCalibTag]
        ojL = ['L1'] #+ ["L2 %s%s"%(i,o) for i,o in l2JetsIo.values()] + ['EF']
        outList += [histoVal('vxp_n',41,-0.5,40.5)]
        outList += [histoVal('averageIntPerXing',100,0.0,50.0)]
        outList += [histoGen(('vxp_n','L1Jetssize'),(41,31),(-0.5,-0.5),(40.5,30.5)),
                    histoGen(('averageIntPerXing','L1Jetssize'),(51,31),(-0.5,-0.5),(50.5,30.5)),
                    ]
        
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''), zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        multiJetTrigs = ['L1_4J15']
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb(t) for t in multiJetTrigs]
        ofi, ofj = calculables.jet.IndicesOffline, calculables.jet.OfflineJets
        ofbi = calculables.jet.IndicesOfflineBad
        minEt = pars['minJetEt']
        maxEta = pars['maxJetEta']
        listOfCalculables += [ofi(minEt=minEt, maxEta=maxEta), ofj(), ofbi()]
        l1i, l1j = calculables.jet.IndicesL1, calculables.jet.L1Jets
        listOfCalculables += [l1i(collection=("trig_L1_jet_", ""), maxEta=maxEta), l1j()]
        listOfCalculables += [size('L1Jets')]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        skim = self.parameters()['skim']
        return [samples.skimmedPeriodD(skim=skim, run=208258)]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 100000 if test else None
        nFilesMax=100 if test else None
        skim = self.parameters()['skim']
        return ([] + supy.samples.specify(names="periodD.%s"%skim, nEventsMax=nEventsMax, nFilesMax=nFilesMax))


    def conclude(self,pars) :
        org = self.organizer(pars)
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     doLog = False,
                     ).plotAll()
