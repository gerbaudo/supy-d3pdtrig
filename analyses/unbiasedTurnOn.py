#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

triggers = ['EF_j15_a4tchad','EF_j25_a4tchad','EF_j35_a4tchad',
            'EF_j35_a10tcem','EF_j35_a4tclcw',
            ]

class unbiasedTurnOn(supy.analysis) :
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
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.goodRun().onlyData(),
            filterMult("vxp_Indices",min=1),
            filterMult("IndicesOfflineJets",min=1),
            filterMult("IndicesOfflineBadJets",max=0),
            ]
        turnon = steps.histos.turnOnJet
        outList += [turnon(jetColl=refJetColl, trigger=t, nTh=0) for t in triggers]
        

#        #rjC, rjL = refJetColl, refJetCollLabel
#        isoRefJetColl, isoRefJetCollLabel = 'Isolated'+refJetColl, 'Iso. '+refJetCollLabel
#        ojC = ['L1Jets'] + ["L2Jets%s%s"%(i,o) for i,o in l2JetsIo.values()] + ["EfJets%s"%efJetCalibTag]
#        ojL = ['L1'] + ["L2 %s%s"%(i,o) for i,o in l2JetsIo.values()] + ['EF']
#        outList += [histoMult(var=var, max=20) for var in ojC+[refJetColl, isoRefJetColl]]
#        hDeta, hDphi, hDr = steps.histos.deltaEta, steps.histos.deltaPhi, steps.histos.deltaR
#        hDet, hDetFrac = steps.histos.deltaEt, steps.histos.deltaEtFrac
#        templateTitle="#Delta %(var)s matched (%(j1)s, %(j2)s); #Delta %(var)s; jets"
#        outList += [h(matchCollPair="%sMatch%s"%(rjC,jC),
#                      title=templateTitle%{'var':var, 'j1':rjL, 'j2':jL},
#                      N=200)
#                    for rjC, rjL in zip([refJetColl, isoRefJetColl],
#                                        [refJetCollLabel, isoRefJetCollLabel])
#                    for h,var in zip([hDeta, hDphi, hDr, hDet],
#                                     ['#eta', '#phi', 'R', 'E_{T}'])
#                    for jC, jL in zip(ojC, ojL)]
#        outList += [h(matchCollPair="%sMatch%s"%(rjC,jC),
#                      title=templateTitle%{'var':var, 'j1':rjL, 'j2':jL},
#                      N=200)
#                    for rjC, rjL in zip([refJetColl, isoRefJetColl],
#                                        [refJetCollLabel, isoRefJetCollLabel])
#                    for h,var in zip([hDetFrac,],
#                                     ['E_{T}/E_{T}',])
#                    for jC, jL in zip(ojC, ojL)]
#        hDetFracEt = steps.histos.deltaEtFracVsEtMap
#        templateTitle="%(varY)s vs. %(varX)s matched (%(j1)s, %(j2)s); %(varX)s; %(varY)s"
#        outList += [h(matchCollPair="%sMatch%s"%(rjC,jC),
#                      title=templateTitle%{'varX':varX, 'varY':varY, 'j1':rjL, 'j2':jL})
#                    for rjC, rjL in zip([refJetColl, isoRefJetColl],
#                                        [refJetCollLabel, isoRefJetCollLabel])
#                    for h,varX,varY in zip([hDetFracEt,],
#                                           ['E_{T,off}',],
#                                           ['#Delta E_{T}/E_{T}',])
#                    for jC, jL in zip(ojC, ojL)]

        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        offJetColl = pars['offJetColl']
        refJetColl = offJetColl
        isoRefJetColl = "Isolated"+refJetColl
        l2JetsIo = self.l2JetsIo
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''), zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb(t) for t in triggers]
        l1i, l1j = calculables.jet.IndicesL1, calculables.jet.L1Jets
        l2i, l2j = calculables.jet.IndicesL2, calculables.jet.L2Jets
        efi, efj = calculables.jet.IndicesEf, calculables.jet.EfJets
        ofi, ofj = calculables.jet.IndicesOffline, calculables.jet.OfflineJets
        ofbi = calculables.jet.IndicesOfflineBad
        listOfCalculables += [l1i(collection=("trig_L1_jet_", "")), l1j()]
        listOfCalculables += [l2i(input=i, output=o) for i,o in l2JetsIo.values()]
        listOfCalculables += [l2j(indices="IndicesL2Jets%s%s"%(i,o)) for i,o in l2JetsIo.values()]
        efCal = pars['efJetCalibTag']
        listOfCalculables += [efi(calibTag=efCal), efj(indices="IndicesEfJets%s"%efCal)]
        maxEta = pars['maxJetEta']
        listOfCalculables += [ofi(minEt=minEt, maxEta=maxEta), ofj(), ofbi()]
        isoJ = calculables.jet.IsolatedJets
        listOfCalculables += [isoJ(coll='OfflineJets')]
        mj = calculables.jet.MatchedJets
        listOfCalculables += [mj(coll1=rj, otherColls=[jColl])
                              for rj in [refJetColl, isoRefJetColl]
                              for jColl in
                              ['L1Jets']
                              +["L2Jets%s%s"%(i,o) for i,o in l2JetsIo.values()]
                              +["EfJets%s"%efCal]]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        return [samples.minbiasPeriodD()]

    def listOfSamples(self,config) :
        test = False #True
        nEventsMax= 100000 if test else None
        nFilesMax=100 if test else None
        skim = self.parameters()['skim']
        return ([] + supy.samples.specify(names="periodDrd0", nEventsMax=nEventsMax, nFilesMax=nFilesMax))


    def conclude(self,pars) :
        org = self.organizer(pars)
        supy.plotter(org,
                     pdfFileName = self.pdfFileName(org.tag),
                     doLog = False,
                     ).plotAll()
