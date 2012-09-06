#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

# todo: also try with FSPS as ref (do the events for which A4CC jets
# are not saved bias our selection?

class example_trig(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                #'grlFile' : "data11_7TeV.periodAllYear_DetStatus-v36-pro10_CoolRunQuery-00-04-08_SMjets.xml",
                'grlFile' : "data/data12_8TeV.periodAllYear_DetStatus-v45-pro13_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "EF_5j55_a4tchad_L2FS",
                'refJetColl' : 'OfflineJets', # 'EfJetsAntiKt4_topo_calib_EMJES'
                'refJetCollLabel' : 'OfflineJets',
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        drMin=0.7
        drMax=None
        etaMaxB=0.7 # barrel
        etaMaxG=1.5 # gap
        refJetColl=pars['refJetColl']
        refJetCollLabel=pars['refJetCollLabel']
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.goodRun().onlyData(),
            steps.filters.triggers(["L1_4J15"]),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineJets",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            steps.filters.triggers([pars['refTrigger']]),
            #steps.filters.triggers(['EF_5j55_a4tchad_L2FSPS']).invert(),
            steps.filters.triggers(['L2_5j15_a4TTem_6j45_a4cchad']).invert(),

#--            supy.steps.printer.printstuff(['PassedTriggers',]),
#--
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                         title="jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", A4CC); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                         nTh=4,
#--                                         title="4th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", A4CC); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                         nTh=4,
#--                                         title="4th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", NON_L15L2CONE); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                         nTh=5,
#--                                         title="5th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", A4CC); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                         nTh=5,
#--                                         title="5th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", NON_L15L2CONE); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                         nTh=6,
#--                                         title="6th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", A4CC); E_{T}^{offline} [GeV]; eff"),
#--            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                         nTh=6,
#--                                         title="6th jet matching efficiency vs. E_{T} matched ("+refJetCollLabel+", NON_L15L2CONE); E_{T}^{offline} [GeV]; eff"),
#--
#--            supy.steps.histos.multiplicity(var='IndicesL2JetsA4TTA4CC_JES', max=20),
#--            #supy.steps.printer.printstuff(['PassedTriggers',]),
#--            #supy.steps.printer.printstuff(["IndicesL2JetsA4TTA4CC_JES",
#--            #                               "EnergyL2JetsA4TTA4CC_JES",
#--            #                               "IndicesL2JetsNON_L15L2CONE",
#--            #                               "IndicesEfJetsAntiKt4_topo_calib_EMJES"]),
#--            supy.steps.histos.multiplicity(var='IndicesL2JetsA4TTA4CC_JES', max=20),
#--            supy.steps.histos.multiplicity(var='IndicesL2JetsNON_L15L2CONE', max=20),
#--            supy.steps.histos.multiplicity(var='IndicesEfJetsAntiKt4_topo_calib_EMJES', max=20),
#--
#--            #steps.filters.triggers(["EF_4j55_a4tchad_L2FS", "EF_4j55_a4tchad_L2FSPS",]),
#--            #steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]),
#--            #steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]).invert(),
#--
#--            #--supy.steps.histos.multiplicity(var = "vx_Indices", max = 20),
#--            #supy.steps.histos.multiplicity(var="IndicesL2Jets",max=20),
#--            #steps.trigger.jetPt(collection="RunNumber"),
#--
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL1Jets',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', L1); #Delta #eta; jets'),
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', L2CONE); #Delta #eta; jets'),
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL2JetsA4TTL2CONE',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', A4TTL2CONE); #Delta #eta; jets'),
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', A4TT); #Delta #eta; jets'),
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL2JetsNONEA10TT',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', A10TT); #Delta #eta; jets'),
#--#-dg-            steps.histos.deltaEta(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--#-dg-                                  title='#Delta #eta matched ('+refJetCollLabel+', A4CC); #Delta #eta; jets'),
#--#-dg-
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL1Jets',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', L1); #Delta #phi; jets'),
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', L2CONE); #Delta #phi; jets'),
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL2JetsA4TTL2CONE',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', ATTL2CONE); #Delta #phi; jets'),
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', A4TT); #Delta #phi; jets'),
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL2JetsNONEA10TT',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', A10TT); #Delta #phi; jets'),
#--#-dg-            steps.histos.deltaPhi(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--#-dg-                                  title='#Delta #phi matched ('+refJetCollLabel+', A4CC); #Delta #phi; jets'),
#--#-dg-
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL1Jets',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', L1); #Delta R; jets'),
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', L2CONE); #Delta R; jets'),
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL2JetsA4TTL2CONE',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', A4TTL2CONE); #Delta R; jets'),
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', A4TT); #Delta R; jets'),
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL2JetsNONEA10TT',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', A10TT); #Delta R; jets'),
#--#-dg-            steps.histos.deltaR(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--#-dg-                                  title='#Delta R matched ('+refJetCollLabel+', A4CC); #Delta R; jets'),
#--
#--            #steps.histos.deltaEt(matchCollPair=refJetColl+'MatchL1Jets',
#--            #                      title='#Delta E_{T} matched ('+refJetCollLabel+', L1); #Delta E_{T}; jets'),
#--            #steps.histos.deltaEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--            #                      title='#Delta E_{T} matched ('+refJetCollLabel+', L2CONE); #Delta E_{T}; jets'),
#--            #steps.histos.deltaEt(matchCollPair=refJetColl+'MatchL2JetsA4TTL2CONE',
#--            #                      title='#Delta E_{T} matched ('+refJetCollLabel+', A4TTL2CONE); #Delta E_{T}; jets'),
#--            #steps.histos.deltaEt(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--            #                      title='#Delta E_{T} matched ('+refJetCollLabel+', A4TT); #Delta E_{T}; jets'),
#--            #steps.histos.deltaEt(matchCollPair=refJetColl+'MatchL2JetsNONEA10TT',
#--            #                      title='#Delta E_{T} matched ('+refJetCollLabel+', A10TT); #Delta E_{T}; jets'),
#--
#--            supy.steps.histos.value(var='RunNumber', N=500, low=202600, up=203100,),
#--            #steps.filters.triggers(["EF_5j55_a4tchad_L2FS"]),
#--            #steps.filters.triggers(["EF_5j55_a4tchad_L2FSPS"]).invert(),
#--            #steps.filters.triggers(["EF_6j45_a4tchad_L2FS"]),
#--            #steps.filters.triggers(['EmulatedL2FSPS_6j45']).invert(),
#--            #steps.filters.triggers(['EmulatedL2FSPS_6j45']).invert(),
#--            steps.filters.triggers(['EF_6j50_a4tchad_L2FS_5L2j15']),
#--            #steps.filters.triggers(['EmulatedL2FSPS_6j50']).invert(),
#--            steps.filters.triggers(['EmulatedL15_6j15_L2FSPS_6j45']).invert(),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A4TT); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL1Jets',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', L1); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', L2CONE); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsA4TTL2CONE',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A4TTL2CONE); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A4TT); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsNONEA10TT',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A10TT); #Delta E_{T}/E_{T}; jets'),
#--            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A4CC); #Delta E_{T}/E_{T}; jets'),
#--
#--            steps.histos.etaPhiMap(coll='L1Jets', title="L1 jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='L2JetsA4TTA4CC_JES', title="L2 A4CC jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='L2JetsNON_L15L2CONE', title="L2 cone jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='L2JetsA4TTL2CONE', title="L2 cone (A4TT seeded) jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='L2JetsNONEA4TT', title="L2 A4TT jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='L2JetsNONEA10TT', title="L2 A10TT jets #phi vs. #eta"),
#--            steps.histos.etaPhiMap(coll='EfJetsAntiKt4_topo_calib_EMJES', title="Ef jets #phi vs. #eta"),
            ]
        nThJet=5
        dEtTitle="#Delta E_{T}/E_{T} matched "
        dEtaTitle="#Delta #eta matched"
        titleX="#eta %dth jet"
        titleYdEt="#Delta E_{T}/E_{T}"
        titleYdEta="#Delta#eta"
        l2psJetColl='L2JetsA4TTA4CC_JES'
        l2coneJetColl='L2JetsNON_L15L2CONE'
        outList += [
            steps.histos.attribute(attrName='eta', coll=refJetColl, nTh=nThJet, title="#eta %dth jet "%(nThJet+1)+"("+refJetColl+"); eta; events"),
            steps.histos.attribute(attrName='eta', coll=l2psJetColl, nTh=nThJet-3, title="#eta %dth jet "%(nThJet+1-3)+"("+l2psJetColl+"); eta; events"),
            steps.histos.attribute(attrName='eta', coll=l2psJetColl, nTh=nThJet-2, title="#eta %dth jet "%(nThJet+1-2)+"("+l2psJetColl+"); eta; events"),
            steps.histos.attribute(attrName='eta', coll=l2psJetColl, nTh=nThJet-1, title="#eta %dth jet "%(nThJet+1-1)+"("+l2psJetColl+"); eta; events"),
            steps.histos.attribute(attrName='eta', coll=l2psJetColl, nTh=nThJet-0, title="#eta %dth jet "%(nThJet+1-0)+"("+l2psJetColl+"); eta; events"),
            steps.histos.etaPhiMap(coll=refJetColl, nTh=nThJet, title="%dth jet "%(nThJet+1)+"("+refJetColl+"); #eta; #phi"),
            steps.histos.etaPhiMap(coll=l2psJetColl, nTh=nThJet-3, title="%dth jet "%(nThJet+1-3)+"("+l2psJetColl+"); #eta; #phi"),
            steps.histos.etaPhiMap(coll=l2psJetColl, nTh=nThJet-2, title="%dth jet "%(nThJet+1-2)+"("+l2psJetColl+"); #eta; #phi"),
            steps.histos.etaPhiMap(coll=l2psJetColl, nTh=nThJet-1, title="%dth jet "%(nThJet+1-1)+"("+l2psJetColl+"); #eta; #phi"),
            steps.histos.etaPhiMap(coll=l2psJetColl, nTh=nThJet-0, title="%dth jet "%(nThJet+1-0)+"("+l2psJetColl+"); #eta; #phi"),


            supy.steps.histos.value(var='RunNumber', N=500, low=202600, up=203100,),

            steps.histos.deltaEt(matchCollPair=l2psJetColl+'Match'+refJetColl,
                                 nTh=nThJet,
                                 title='#Delta E_{T} matched ('+l2psJetColl+', '+refJetColl+'); #Delta E_{T}; jets'),
            steps.histos.deltaEt(matchCollPair=l2psJetColl+'Match'+l2coneJetColl,
                                 nTh=nThJet,
                                 title='#Delta E_{T} matched ('+l2psJetColl+', '+l2coneJetColl+'); #Delta E_{T}; jets'),

#--            steps.histos.deltaEtaVsEtaMap(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                          nTh=nThJet,
#--                                          title=dEtaTitle+' ('+refJetCollLabel+', NON_L15L2CONE);'+titleX%(nThJet+1)+titleYdEta),
#--            steps.histos.deltaEtaVsEtaMap(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                          nTh=nThJet,
#--                                          title=dEtaTitle+' ('+refJetCollLabel+', A4CC);'+titleX%(nThJet+1)+titleYdEta),
#--
#--            steps.histos.deltaEtFracVsEtaMap(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                             nTh=nThJet,
#--                                             yLo=-2.0, yUp=+2.0,
#--                                             title=dEtTitle+' ('+refJetCollLabel+', NON_L15L2CONE);'+titleX%(nThJet+1)+titleYdEt),
#--            steps.histos.deltaEtFracVsEtaMap(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#--                                             nTh=nThJet,
#--                                             yLo=-2.0, yUp=+2.0,
#--                                             title=dEtTitle+' ('+refJetCollLabel+', A4CC);'+titleX%(nThJet+1)+titleYdEt),
#--            steps.histos.deltaEtFracVsMinDrMap(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#--                                               nTh=nThJet,
#--                                               title=dEtTitle+' ('+refJetCollLabel+', NON_L15L2CONE);'+titleX%(nThJet+1)+titleYdEt),
#--
#            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#                                         nTh=4,
#                                         title="matching efficiency vs. E_{T} matched ('+refJetCollLabel+', A4TT); E_{T}^{offline} [GeV]; eff"),
#            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#                                         nTh=4,
#                                         title="matching efficiency vs. E_{T} matched ('+refJetCollLabel+', L2CONE); E_{T}^{offline} [GeV]; eff"),
#            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#                                         nTh=4,
#                                         title="matching efficiency vs. E_{T} matched ('+refJetCollLabel+', A4CC); E_{T}^{offline} [GeV]; eff"),
#            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNONEA4TT',
#                                         nTh=5,
#                                         title="matching efficiency vs. E_{T} matched ('+refJetCollLabel+', A4TT); E_{T}^{offline} [GeV]; eff"),
#            steps.histos.matchingEffVsEt(matchCollPair=refJetColl+'MatchL2JetsNON_L15L2CONE',
#                                         nTh=5,
#                                         title="matching efficiency vs. E_{T} matched ('+refJetCollLabel+', L2CONE); E_{T}^{offline} [GeV]; eff"),

#            steps.histos.deltaEtFrac(matchCollPair=refJetColl+'MatchL2JetsA4TTA4CC_JES',
#                                     title='#Delta E_{T}/E_{T} matched ('+refJetCollLabel+', A4CC) FS !FSPS; #Delta E_{T}/E_{T}; jets'),

            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        #listOfCalculables += supy.calculables.zeroArgs(calculables.vertex)
        #listOfCalculables += [calculables.TrigD3PD.Tdt(),]
        listOfCalculables += [calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_mu18_medium"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              #calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FS"),
                              #calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_6j45_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FSPS"),
                              #calculables.TrigD3PD.TriggerBit("L2_4j15_a4TTem_4j50_a4cchad "),
                              calculables.TrigD3PD.TriggerBit("L2_5j15_a4TTem_6j45_a4cchad"),
                              calculables.TrigD3PD.TriggerBit("L1_4J15"),
                              calculables.TrigD3PD.TriggerBit("EF_6j50_a4tchad_L2FS_5L2j15"),
                              calculables.TrigD3PD.TriggerBit("EF_6j50_a4tchad_L2FSPS_5L2j15"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.Grlt(pars['grlFile']),
                              calculables.TrigD3PD.isGoodRun(runN='RunNumber',lbn='lbn'),
                              calculables.TrigD3PD.PassedTriggers(),
                              #calculables.TrigD3PD.PassedTriggers(r'.*PS.*'),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),

                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='L2CONE'),   # L2 seeded by L1.5
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A10TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT_JES'), # L1.5 HAD JES
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='A4CC_JES'), # A4CC HAD JES
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
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]

        for jColl in ['L1Jets', 'L2JetsNON_L15L2CONE', 'L2JetsA4TTL2CONE',
                      'L2JetsNONEA4TT', 'L2JetsNONEA10TT', 'L2JetsA4TTA4CC_JES',
                      'EfJetsAntiKt4_topo_calib_EMJES'] :
            listOfCalculables += [calculables.jet.MatchedJets(coll1=pars['refJetColl'],
                                                              otherColls=[jColl])]
        listOfCalculables += [calculables.jet.MatchedJets(coll1='L2JetsA4TTA4CC_JES', otherColls=['L2JetsNON_L15L2CONE']),
                              calculables.jet.MatchedJets(coll1='L2JetsA4TTA4CC_JES', otherColls=['OfflineJets']),
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
                              calculables.TrigD3PD.EmulatedMultijetTriggerBit(jetColl='L2JetsNON_L15L2CONE',
                                                                              label='L2',
                                                                              multi=6, minEt=50.*GeV),
                              calculables.TrigD3PD.EmulatedMultijetTriggerBit(jetColl='L2JetsNONEA4TT',
                                                                              label='L15',
                                                                              multi=6, minEt=15.*GeV),
                              ]
        listOfCalculables += [
            calculables.TrigD3PD.TriggerBitAnd(bit1='EmulatedL15_6j15', bit2='EmulatedL2_6j50', label='L15_6j15_L2_6j50'),
            calculables.TrigD3PD.TriggerBitAnd(bit1='EmulatedL15_6j15', bit2='EmulatedL2FSPS_6j45', label='L15_6j15_L2FSPS_6j45'),
            calculables.TrigD3PD.TriggerBitAnd(bit1='EmulatedL15_6j15', bit2='EmulatedL2FSPS_6j50', label='L15_6j15_L2FSPS_6j50'),
            ]

        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        castorBaseDir="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'

        exampleDict = supy.samples.SampleHolder()

#        exampleDict.add("Pythia_ttbar_bWincbHminus",
#                '["/tmp/gerbaudo/eos/NTUP_TRIG.742401._000002.root.1"]',
#                        lumi = 1.0e+3 ) #/pb
# get these files from
# eos ls /eos/atlas/atlasdatadisk/data11_7TeV/NTUP_TRIG/r3408_r3410_p661/data11_7TeV.00191628.physics_EnhancedBias.merge.NTUP_TRIG.r3408_r3410_p661_tid742401_00
# (these are the suspicious eventd from Brian's email)
        exampleDict.add("foo",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/bugfixCheck/TrigT2CaloJet-00-01-29"),
                        lumi = 1.0e3)
        exampleDict.add("data12_8TeV.00200804",
                        # need export STAGE_SVCCLASS=atlcal for this castor area
                        'utils.fileListFromCastor('
                        +'location='
                        +'"/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/physics_JetTauEtmiss/00200804/'
                        +'data12_8TeV.00200804.physics_JetTauEtmiss.merge.NTUP_TRIG.x191_m1109"'
                        +',pruneList=False)',
                        lumi = 0.03547) #/pb
        exampleDict.add("data12_8TeV.00200863",
                        'utils.fileListFromTextFile(fileName="//afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/data12_8TeV.00200863.txt")',
                        lumi = 3.505)
        exampleDict.add("data12_8TeV.00200913",
                        'utils.fileListFromTextFile(fileName="//afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/data12_8TeV.00200913.txt")',
                        lumi = 2.786)
        exampleDict.add("data12_8TeV.00200926",
                        'utils.fileListFromTextFile(fileName="//afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/data12_8TeV.00200926.txt")',
                        lumi = 9.226)
        exampleDict.add("data12_8TeV.00202609",
                        'utils.fileListFromTextFile(fileName="//afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/data12_8TeV.00202609.txt")',
                        lumi = 0.313)
        exampleDict.add("TrigT2CaloJet-00-01-29",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/bugfixCheck/TrigT2CaloJet-00-01-29"),
                        lumi = 1.0e3)
        exampleDict.add("TrigT2CaloJet-00-01-31",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/bugfixCheck/TrigT2CaloJet-00-01-31"),
                        lumi = 1.0e3)
        exampleDict.add("data12_8TeV.00202660",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBaseDir+'/00202660/data12_8TeV.00202660.express_express.merge.NTUP_TRIG.x199_m1129/')
                        +','+castorDefaultOpt+')',
                        lumi = 2.178)
        exampleDict.add("data12_8TeV.00202668",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBaseDir+'/00202668/data12_8TeV.00202668.express_express.merge.NTUP_TRIG.f443_m1139/')
                        +','+castorDefaultOpt+')',
                        lumi = 26.11)

        exampleDict.add("202668_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202668.skim.L1_4J15"),
                        lumi = 26.11)
        exampleDict.add("202712_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202712.skim.L1_4J15"),
                        lumi = 29.85)
        exampleDict.add("202712_L1_4J15_2",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202712.skim.L1_4J15_2"),
                        lumi = 29.85)
        exampleDict.add("202740_L1_4J15",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202740.skim.L1_4J15"),
                        lumi = 7.281)
        exampleDict.add("202798_L1_4J15",
                         '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202798.skim.L1_4J15"),
                         #'%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202798.skim.L1_4J15"),
                         lumi = 52.6)
        exampleDict.add("PeriodB_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB.txt"'
                        +')',
                        lumi=26.11+29.85+7.281+52.6+119.4)

        exampleDict.add("data12_8TeV.00203277",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBaseDir+'/00203277/data12_8TeV.00203277.express_express.merge.NTUP_TRIG.f444_m1141/')
                        +','+castorDefaultOpt+')',
                        lumi = 99.3)
        exampleDict.add("data12_8TeV.00203335",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBaseDir+'/00203335/data12_8TeV.00203335.express_express.merge.NTUP_TRIG.f446_m1146/')
                        +','+castorDefaultOpt+')',
                        lumi = 61.81),
        exampleDict.add("data12_8TeV.00203336",
                        'utils.fileListFromCastor('
                        +'location="%s"'%(castorBaseDir+'/00203336/data12_8TeV.00203336.express_express.merge.NTUP_TRIG.f446_m1146/')
                        +','+castorDefaultOpt+')',
                        lumi = 61.25)
        exampleDict.add("test_eos",
                        '%s%s")'%(supy.sites.eos(), "/eos/atlas/user/g/gerbaudo/trigger/skim/SUSYD3PD.202668.skim.L1_4J15"),
                        lumi = 10.)
        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1 #100
        return (
            #supy.samples.specify(names = "data12_8TeV.00200804", color = r.kBlack)
            #supy.samples.specify(names = "Zmumu_skimMu", color = r.kRed, effectiveLumi = 10.0e+3)
            #supy.samples.specify(names=['data12_8TeV.00202660', 'data12_8TeV.00202668',
            #                            'data12_8TeV.00202712', 'data12_8TeV.00202740', 'data12_8TeV.00202798',],
            #                     color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)

            #supy.samples.specify(names="data12_8TeV.00203336", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            #supy.samples.specify(names="202668_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            #+supy.samples.specify(names="202712_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1, markerStyle=r.kOpenCircle)
            #+supy.samples.specify(names="202740_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            #+supy.samples.specify(names="202798_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            supy.samples.specify(names="PeriodB_L1_4J15", color = r.kBlack, nEventsMax=nEventsMax, nFilesMax=-1)
            )

    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
        # mergeSamples doesn't work with the special step matchingEffVsEt that implements mergeFunc
        #org.mergeSamples(targetSpec = {"name":"Period B (part)", "color":r.kBlack}, allWithPrefix="202")
        #org.mergeSamples(targetSpec = {"name":"Period B (part)", "color":r.kBlack},
        #                 sources=['202668_L1_4J15', '202712_L1_4J15', '202740_L1_4J15', '202798_L1_4J15'])
        #org.scale(lumiToUseInAbsenceOfData=1000.)
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      #linYafter = ("triggers", "L1_4J15"),
                      doLog = False,
                      #samplesForRatios = ("Example_Skimmed_900_GeV_Data","Example_Skimmed_900_GeV_MC"),
                      #sampleLabelsForRatios = ("data","sim"),
                      blackList = ['num_', 'den_'],
                      ).plotAll()
