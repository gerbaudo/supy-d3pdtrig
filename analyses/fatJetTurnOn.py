
import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV


class fatJetTurnOn(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        mode = 'j460a4_L2FS' # 'j35' 'j460a10' 'j460a4' 'j460a4_L2FS', 'j460a10_L2FS'
        toTrigs =  {'j35':'EF_j35_a10tcem', 'j460a10':'EF_j460_a10tclcw', 'j360a4':'EF_j360_a4tclcw', 'j460a4':'EmulatedEF_j460_a4tclcw',
                    'j460a4_L2FS' : 'EmulatedEF_j460_a4tclcw_L2FS_j75',
                    'j460a10_L2FS': 'EmulatedEF_j460_a10tclcw_L2FS_j75'}
        refTrigs = {'j35':'L1_RD0_FILLED',  'j460a10':'EF_j240_a10tcem',  'j360a4':'EF_j280_a4tchad', 'j460a4':'EF_j280_a4tchad',
                    'j460a4_L2FS' : 'EF_j280_a4tchad',
                    'j460a10_L2FS': 'EF_j240_a10tcem'}
        skims = {'j35':'L1_RD0_FILLED',  'j460a10':'EF_A4_OR_A10',  'j360a4':'EF_A4_OR_A10', 'j460a4':'EF_A4_OR_A10',
                 'j460a10_L2FS':'EF_A4_OR_A10', 'j460a4_L2FS':'EF_A4_OR_A10'}
        return {'mode':mode,
                'minJetEt' : 30.0*GeV,
                'maxJetEta' : 3.2,
                'minNofflineJets' : 5,
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v51-pro13-04_CoolRunQuery-00-04-08_All_Good.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : refTrigs[mode],
                'turnOnTrigger' : toTrigs[mode],
                'skim' : skims[mode],
                'refJetColl' : 'OfflineJets',
                'refFatJetColl' : 'OfflineJetsA10',
                'offlineFatJetColl':'jet_AntiKt10LCTopo_',
                'efCalibTag':'AntiKt4_lctopo',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        mode = pars['mode']
        refTrigger = pars['refTrigger']
        tonTrigger = pars['turnOnTrigger']
        refJetColl = pars['refJetColl']
        offlineFatJetColl = pars['offlineFatJetColl']
        refFatJetColl = pars['refFatJetColl']
        xMin, xMax = 0. , (200. if mode=='j35' else 600.)
        binWidth = 5 if mode=='j35' else 10.
        nBins = int((xMax-xMin)/binWidth)
        emulated = True if mode in ['j460a4','j460a4_L2FS','j460a10_L2FS'] else False

        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            supy.steps.filters.multiplicity(refJetColl, min=1),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers([refTrigger]),
            #supy.steps.printer.printstuff(['PassedTriggers',]),
            ]
        outList += [supy.steps.histos.multiplicity(jc, max=20)
                    for jc in [refJetColl, refFatJetColl]]
        #outList += [steps.printer.JetPrinter(jc) for jc in [refJetColl, refFatJetColl]]
        outList += [steps.histos.attribute(attrName='et', coll=jc, nTh=0,
                                           title="E_{T} %dth jet "%(0+1)+"("+jc+"); E_{T}; events",
                                           xLo=xMin,xUp=xMax*GeV)
                    for jc in [refJetColl,refFatJetColl]
                    ]
        outList += [steps.histos.turnOnJet(trigger=tonTrigger, jetColl=jc,
                                            nTh=0,N=nBins,low=xMin,up=xMax,
                                            emulated=emulated,
                                            title=tonTrigger+" efficiency; 1st %s jet E_{T} [GeV];eff"%jcl)
                     for jc, jcl in zip([refJetColl, refFatJetColl],
                                        ['AntiKt4TopoNewEM', 'AntiKt10LCTopo'])
                     ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        maxEta = pars['maxJetEta']
        offlineFatJetColl = pars['offlineFatJetColl']
        calibTag = pars['efCalibTag']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        tb = calculables.TrigD3PD.TriggerBit
        listOfCalculables += [tb('L1_RD0_FILLED'),
                              tb('EF_j35_a10tcem'),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL2(input='NONE', output='A10TT',maxEta=maxEta),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA10TT"),
                              ]
        listOfCalculables += [calculables.jet.IndicesEf(minEt=minEt, maxEta=maxEta, calibTag=calibTag),
                              calculables.jet.EfJets(indices='IndicesEfJets'+calibTag),
                              ]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt, maxEta=maxEta),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              calculables.jet.IndicesOffline(collection=(offlineFatJetColl,''),maxEta=maxEta,minEt=minEt,
                                                             tag='A10',attributesToSkip=['isUgly','isBadLoose']),
                              calculables.jet.OfflineJets(collection=(offlineFatJetColl,''),indices='IndicesOfflineJetsA10',
                                                          attributesToSkip=['isUgly','isBadLoose']),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit # todo: fix this jet collection
        listOfCalculables += [emjb(multi=1, minEt=75.*GeV, jetColl='L2JetsNONEA10TT', label='L2FS')]
        listOfCalculables += [emjb(multi=1, minEt=460.*GeV, jetColl='EfJets'+calibTag, label='EF',suffix='_a4tclcw')]
        tba = calculables.TrigD3PD.TriggerBitAnd
        listOfCalculables += [
            tba(bit1='EmulatedL2FS_j75', bit2='EmulatedEF_j460_a4tclcw', label='EF_j460_a4tclcw_L2FS_j75')
            ]

        return listOfCalculables

    def listOfSampleDictionaries(self) :
        skim = self.parameters()['skim']
        return [samples.skimmedPeriodD(skim=skim)]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 10000 if test else -1
        nFilesMax=10 if test else -1
        skim = self.parameters()['skim']
        return ([] + supy.samples.specify(names="periodD.%s"%skim, nEventsMax=nEventsMax, nFilesMax=nFilesMax))

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        mode = self.parameters()['mode']
        mode, skim = self.parameters()['mode'], self.parameters()['skim']
        #org.mergeSamples(targetSpec = {"name":"Data 2011", "color":r.kBlack, "markerStyle":20},
        #                 sources=["%d.%s"%(run,skim) for run in [208184,208258,208261,208354,208485,208662]])
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      doLog = False,
                      blackList = ['num_.*', 'den_.*'],
                      ).plotAll()
