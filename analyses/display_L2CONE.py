#!/usr/bin/env python
#
# Try to debug the l2cone jets observed by Marco.
#
# Features of the strange jets:
# - in: Non_l15, out: L2CONE
# - both flags c4ccem, c4cchad are 0
# - eem0+ehad0 = E
#
# davide.gerbaudo@gmail.com
# Jul 2013

import supy
import calculables,steps,samples, ROOT as r

GeV=1.0e+3
TeV=1.0e+3*GeV

class display_L2CONE(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[5-9]+j.*(em|had)$',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.triggers(['EmulatedOffline_6j70']),
            steps.filters.triggers(['EF_6j50_a4tchad_L2FS_5L2j15']),
            steps.filters.triggers(['EF_6j50_a4tchad_L2FSPS_5L2j15']).invert(),

            steps.displayer.displayer(doL1Jets=True, doL2Jets=True, doEfJets = True, doOfflineJets=True),
            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += [#calculables.TrigD3PD.Tdt(),
                              calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),
                              calculables.TrigD3PD.PassedTriggers(),
                              ]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("L2_5j15_a4TTem"),
                              calculables.TrigD3PD.TriggerBit("L2_5j15_a4TTem_5j50_a4cchad"),
                              calculables.TrigD3PD.TriggerBit("L2_6j15_a4TTem_6j50_a4cchad"),
                              #calculables.TrigD3PD.TriggerBit("EF_6j50_a4tchad_L2FS_5L2j15"),
                              calculables.TrigD3PD.TriggerBit('EF_6j50_a4tchad_L2FS_5L2j15'),
                              calculables.TrigD3PD.TriggerBit('EF_6j50_a4tchad_L2FSPS_5L2j15'),
                              ]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),

                              calculables.jet.L2Jets(indices="IndicesL2JetsNON_L15L2CONE"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsNONEA4TT_JES"),
                              calculables.jet.L2Jets(indices="IndicesL2JetsA4TTA4CC_JES"),
                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='A4CC_JES'), # A4CC HAD JES

                              calculables.jet.IndicesEf(minEt=minEt, calibTag='AntiKt4_topo_calib_EMJES'),
                              calculables.jet.EfJets(indices='IndicesEfJetsAntiKt4_topo_calib_EMJES'),

                              calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                          otherColls=['L2JetsA4TTA4CC_JES','L2JetsNONEA4TT']),
                              calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              ]
        listOfCalculables += [calculables.TrigD3PD.EmulatedMultijetTriggerBit(jetColl='L2JetsA4TTA4CC_JES',
                                                                              label='L2FSPS',
                                                                              multi=6, minEt=45.*GeV),
                              calculables.TrigD3PD.EmulatedMultijetTriggerBit(jetColl='L2JetsA4TTA4CC_JES',
                                                                              label='L2FSPS',
                                                                              multi=6, minEt=50.*GeV),
                              calculables.TrigD3PD.EmulatedMultijetTriggerBit(jetColl='L2JetsA4TTA4CC_JES',
                                                                              label='L2FSPS',
                                                                              multi=6, minEt=55.*GeV),
                              ]
        emjb = calculables.TrigD3PD.EmulatedMultijetTriggerBit
        listOfCalculables += [emjb(jetColl='OfflineJets', label='Offline', multi=6, minEt=70.*GeV)]

        return listOfCalculables

    def listOfSampleDictionaries(self) :
        skim = 'L1_4J15'
        #return [samples.skimmedPeriodD(skim=skim, run=208258)]
        return [samples.getMarcoSamples()]

    def listOfSamples(self,config) :
        test = True #False
        nEventsMax= 10000 if test else None
        nFilesMax=100 if test else None
        skim = 'L1_4J15'
        return ([] +
#                 supy.samples.specify(names="periodD.%s"%skim,
#                                      nEventsMax=nEventsMax,
#                                      nFilesMax=nFilesMax)
                supy.samples.specify(names="marcoSamples",
                                     nEventsMax=nEventsMax,
                                     nFilesMax=nFilesMax)
                 )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        org.scale(lumiToUseInAbsenceOfData=1000.)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      ).plotAll()
