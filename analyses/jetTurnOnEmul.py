#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class jetTurnOnEmul(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v45-pro13_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "EF_5j55_a4tchad_L2FS",
                'refJetColl' : 'OfflineJets',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        drMin=0.7
        drMax=None
        drAnyJet=True
        etaMaxB=0.7 # barrel
        etaMaxG=1.5 # gap
        refJetColl=pars['refJetColl']
        offlineMaxEta=pars['maxJetEta']
        offlineMinEt=pars['minJetEt']
        minNofflineJets=pars['minNofflineJets']
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers([pars['refTrigger']]),
            #steps.filters.triggers(['EF_5j55_a4tchad_L2FSPS']),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineJets",min=minNofflineJets),
            steps.filters.triggers(['EmulatedOffline_5j70']),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_5j15', emulated=True, nTh=4),
            supy.steps.filters.multiplicity("IndicesOfflineJets",min=minNofflineJets+1),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j10', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j35', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j40', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j45', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j50', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15_L2_6j50', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15_L2FSPS_6j35', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15_L2FSPS_6j40', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15_L2FSPS_6j45', emulated=True, nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL15_6j15_L2FSPS_6j50', emulated=True, nTh=5),
            steps.filters.triggers(['EmulatedL15_5j15']),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j45', emulated=True, nTh=5),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=5, title="E_{T} %dth jet "%(5+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),
            steps.filters.triggers(['EmulatedL15_6j15']),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EmulatedL2PS_6j50', emulated=True, nTh=5),
            steps.histos.attribute(attrName='et', coll=refJetColl, nTh=5, title="E_{T} %dth jet "%(5+1)+"("+refJetColl+"); E_{T}; events",xLo=0.0,xUp=200.0*GeV),

            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        maxEta = pars['maxJetEta']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb("EF_mu18_medium"),
                              tb("EF_4j55_a4tchad_L2FS"),
                              tb("EF_4j55_a4tchad_L2FSPS"),
                              tb("EF_5j55_a4tchad_L2FS"),
                              tb("EF_5j55_a4tchad_L2FSPS"),
                              tb("EF_6j45_a4tchad_L2FS"),
                              tb("EF_6j55_a4tchad_L2FSPS"),
                              tb("L1_4J15"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),
                              #calculables.TrigD3PD.PassedTriggers(r'.*PS.*'),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='A4TT', output='L2CONE'),   # L2 seeded by L1.5
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='NONE', output='A10TT'),    # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, maxEta=maxEta, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsNON_L15L2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTL2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA10TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT_JES"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),
                              calculables.jet.EnergyL2Jets(input='A4TT', output='A4CC_JES'),
                              calculables.jet.IndicesEf(minEt=minEt, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),
                              ]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
        listOfCalculables += [
            emjb(jetColl='L2JetsNONEA4TT', label='L15', multi=5, minEt=15.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L15', multi=6, minEt=10.*GeV),
            emjb(jetColl='L2JetsNONEA4TT', label='L15', multi=6, minEt=15.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=35.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=40.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=45.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=50.*GeV),
            emjb(jetColl='L2JetsA4TTA4CC_JES', label='L2PS', multi=6, minEt=55.*GeV),
            emjb(jetColl='L2JetsNON_L15L2CONE', label='L2', multi=6, minEt=50.*GeV),
            emjb(jetColl='OfflineJets', label='Offline', multi=5, minEt=70.*GeV),            
            ]
        tba = calculables.TrigD3PD.TriggerBitAnd
        listOfCalculables += [
            tba(bit1='EmulatedL15_6j15', bit2='EmulatedL2_6j50', label='L15_6j15_L2_6j50'),
            tba(bit1='EmulatedL15_6j15', bit2='EmulatedL2PS_6j35', label='L15_6j15_L2FSPS_6j35'),
            tba(bit1='EmulatedL15_6j15', bit2='EmulatedL2PS_6j40', label='L15_6j15_L2FSPS_6j40'),
            tba(bit1='EmulatedL15_6j15', bit2='EmulatedL2PS_6j45', label='L15_6j15_L2FSPS_6j45'),
            tba(bit1='EmulatedL15_6j15', bit2='EmulatedL2PS_6j50', label='L15_6j15_L2FSPS_6j50'),
            ]

        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        castorBaseDir="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'

        lumiPerRun = {202668:26.0, 202712:29.85, 202740:7.28, 202798:52.6, # B1
                      202987:14.02, 202991:40.15, 203027:89.29, 203258:119.4, #B2
                      }
        exampleDict = supy.samples.SampleHolder()
        exampleDict.add("PeriodB_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB.txt"'
                        #+'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB_test.txt"'
                        +')',
                        lumi= sum(lumiPerRun.keys())
                        )
        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1 #1000
        return (
            supy.samples.specify(names="PeriodB_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()
