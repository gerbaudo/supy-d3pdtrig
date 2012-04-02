#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r

GeV=1.0e+3
TeV=1.0e+3*GeV

class example_trig(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                'grlFile' : "data11_7TeV.periodAllYear_DetStatus-v36-pro10_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[5-9]+j.*(em|had)$',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        outList=[
            supy.steps.printer.progressPrinter(),
            supy.steps.histos.multiplicity(var='IndicesL2JetsNONEA4CC_JES', max=20),
            #supy.steps.printer.printstuff(["IndicesL2JetsNONEA4CC_JES",]),
            steps.trigger.triggerCounts(pattern=r'.*5j55.*'),
            steps.trigger.triggerCounts(pattern=r'%s'%pars['L2multiJetChain']),
            #steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]),
            #steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]).invert(),
            #--steps.filters.triggers(["EF_mu18_medium",]),
            #supy.steps.printer.printstuff(["EF_mu18_medium",]),
            #--supy.steps.filters.multiplicity("vx_Indices",min=1),
            #--supy.steps.filters.multiplicity("IndicesOfflineJets",min=1),
            #--supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            #--supy.steps.histos.multiplicity(var = "vx_Indices", max = 20),
            #--steps.filters.goodRun().onlyData(),
            #supy.steps.histos.multiplicity(var="IndicesL2Jets",max=20),
            #steps.trigger.jetPt(collection="RunNumber"),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4CC_JES',
                                  title='#Delta #eta ; #Delta #eta matched (EfJetsAntiKt4, A4CC); jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNON_L15L2CONE',
                                  title='#Delta #eta ; #Delta #eta matched (EfJetsAntiKt4, L2CONE); jets'),
            steps.histos.deltaEta(matchCollPair='EfJetsAntiKt4_topo_calib_EMJESMatchL2JetsNONEA4TT',
                                  title='#Delta #eta ; #Delta #eta matched (EfJetsAntiKt4, A4TT); jets'),

            #supy.steps.printer.printstuff(['PassedTriggers',]),
            #supy.steps.filters.multiplicity(min = 4, var = "jet_Indices"),
            #supy.steps.histos.multiplicity(var = "jet_Indices", max = 20),
            #supy.steps.histos.eta(var = "jet_P4", N = 20, low = -2., up = +2., indices = "jet_Indices"),
            #supy.steps.histos.value(var = "jet_M01" , N = 50, low = 0., up = 1.0e+3*GeV),
            #supy.steps.filters.value(var = "jet_M01", min = 1.0*TeV),
            #supy.steps.other.skimmer()
            ]
        return outList
    
    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += [calculables.TrigD3PD.Tdt(),]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_mu18_medium"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              ]
        listOfCalculables += [#calculables.TrigD3PD.Grlt(pars['grlFile']),
                              #calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vx_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),

                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4CC_JES'), # A4CC HAD JES
                              calculables.jet.L2Jets(indices="IndicesL2JetsNON_L15L2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT_JES"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4CC_JES"),

                              calculables.jet.IndicesEf(minEt=minEt, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4CC_JES','L2JetsNONEA4TT']),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4CC_JES']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNON_L15L2CONE']),
                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsNONEA4TT']),
                              calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        exampleDict = supy.samples.SampleHolder()
#        exampleDict.add("Pythia_ttbar_bWincbHminus",
#                '["/tmp/gerbaudo/eos/NTUP_TRIG.742401._000002.root.1"]',
#                        lumi = 1.0e+3 ) #/pb
# get these files from
# eos ls /eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3408_r3410_p661/data11_7TeV.00191628.physics_EnhancedBias.merge.NTUP_TRIG.r3408_r3410_p661_tid742401_00
# (these are the suspicious eventd from Brian's email)
        exampleDict.add("Pythia_ttbar_bWincbHminus",
                        #'utils.fileListFromDisk(location = "/tmp/gerbaudo/eos/NTUP*.root*", isDirectory = False)',
                        #'utils.fileListFromDisk(location = "/tmp/gerbaudo/dq2/*.root*", isDirectory = False)',
                        'utils.fileListFromDisk(location = "/tmp/gerbaudo/eos/r3466_r3467_p661/*.root*", isDirectory = False)',
                        #'[""]',
                        lumi = 1.0e+3 ) #/pb
        return [exampleDict]

    def listOfSamples(self,config) :
        return (supy.samples.specify(names = "Pythia_ttbar_bWincbHminus", color = r.kBlack, markerStyle = 20,
                                     #nFilesMax = 100,
                                     #nEventsMax=10,
                                     )
                #supy.samples.specify(names = "Zmumu_skimMu", color = r.kRed, effectiveLumi = 10.0e+3) +
                #supy.samples.specify(names = "ttbar_skimMu", color = r.kViolet, effectiveLumi = 10.0e+3)
                )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1000.)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      #samplesForRatios = ("Example_Skimmed_900_GeV_Data","Example_Skimmed_900_GeV_MC"),
                      #sampleLabelsForRatios = ("data","sim"),
                      ).plotAll()
