#!/usr/bin/env python

import supy
import calculables,steps,samples, ROOT as r
import re

GeV=1.0e+3
TeV=1.0e+3*GeV

class jetTurnOn(supy.analysis) :
    def otherTreesToKeepWhenSkimming(self) : return []
    def parameters(self) :
        return {'minJetEt' : 10.0*GeV,
                'grlFile' : "data11_7TeV.periodAllYear_DetStatus-v36-pro10_CoolRunQuery-00-04-08_SMjets.xml",
                'L2jetChain' : 'L2_[0-9]*j.*',
                'L2multiJetChain' : 'L2_[4-9]+j.*(em|had)$',
                'refTrigger' : "EF_5j55_a4tchad_L2FS",
                }

    def listOfSteps(self,config) :
        pars = self.parameters()
        drMin=0.7
        drMax=None
        etaMaxB=0.7 # barrel
        etaMaxG=1.5 # gap
        refJetColl='EfJetsAntiKt4_topo_calib_EMJES'
        outList=[
            supy.steps.printer.progressPrinter(),
            steps.filters.triggers(["L1_4J15"]),
            supy.steps.filters.multiplicity("vxp_Indices",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineJets",min=1),
            supy.steps.filters.multiplicity("IndicesOfflineBadJets",max=0),
            steps.filters.triggers([pars['refTrigger']]),

            supy.steps.filters.label('EF, 4th and 5th jet'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_4j55_a4tchad_L2FSPS', nTh=3),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_5j55_a4tchad_L2FSPS', nTh=4),
            # 6j
            supy.steps.filters.label("EF_6j45"),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tclcw_L2FS_5L2j15', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j45_a4tchad_L2FS_5L2j15', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label("EF_6j50"),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tclcw_L2FS_5L2j15', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j50_a4tchad_L2FS_5L2j15', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5),
            supy.steps.filters.label("EF_6j55"),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_6j55_a4tchad_L2FSPS', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),

            # L2 (6th, 7th, 8th jet for several L2 triggers)
            supy.steps.filters.label('L2_5j15_a4TTem'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem', nTh=7, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('L2_5j15_a4TTem_*_a4cchad'),
            supy.steps.filters.label('L2 5th jet'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j50_a4cchad', nTh=4, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_5j55_a4cchad', nTh=4, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('L2 6th jet'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_6j45_a4cchad', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_6j15_a4TTem_6j50_a4cchad', nTh=5, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('L2 7th jet'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_7j35_a4cchad', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_7j15_a4TTem_7j50_a4cchad', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('L2 8th jet'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='L2_5j15_a4TTem_8j30_a4cchad', nTh=7, etaMin=etaMaxB, etaMax=etaMaxG),

            # 7j
            supy.steps.filters.label('EF_7j*'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tclcw_L2FS_5L2j15', nTh=6),
            supy.steps.filters.label('EF_7j*_a4tchad_5L2j15'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j35_a4tchad_5L2j15', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j45_a4tchad_5L2j15', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('EF_7j40_a4tchad_L2FS_5L2j15'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j40_a4tchad_L2FS_5L2j15', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('EF_7j55_a4tchad_L2FSPS'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_7j55_a4tchad_L2FSPS', nTh=6, etaMin=etaMaxB, etaMax=etaMaxG),
            # 8j
            supy.steps.filters.label('EF_8j*'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tclcw_L2FS_5L2j15', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tclcw_L2FS_5L2j15', nTh=7),
            supy.steps.filters.label('EF_8j35_a4tchad_L2FSPS_5L2j15'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FSPS_5L2j15', nTh=7, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('EF_8j35_a4tchad_L2FS_5L2j15'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j35_a4tchad_L2FS_5L2j15', nTh=7, etaMin=etaMaxB, etaMax=etaMaxG),
            supy.steps.filters.label('EF_8j40_a4tchad_L2FS_5L2j15'),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7, drMax=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7, drMin=drMin),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7, etaMax=etaMaxB),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7, etaMin=etaMaxG),
            steps.histos.turnOnJet(jetColl=refJetColl, trigger='EF_8j40_a4tchad_L2FS_5L2j15', nTh=7, etaMin=etaMaxB, etaMax=etaMaxG),


            ]
        return outList

    def listOfCalculables(self,config) :
        pars = self.parameters()
        minEt = pars['minJetEt']
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.TrigD3PD.Tdt(treeName = "TrigConfTree", dirName = "susyMeta"),]
        listOfCalculables += [calculables.TrigD3PD.TriggerBit("EF_mu18_medium"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_4j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_5j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("EF_6j45_a4tchad_L2FS"),
                              calculables.TrigD3PD.TriggerBit("EF_6j55_a4tchad_L2FSPS"),
                              calculables.TrigD3PD.TriggerBit("L1_4J15"),
                              ]
        listOfCalculables += [calculables.TrigD3PD.PassedTriggers(),
                              #calculables.TrigD3PD.PassedTriggers(r'.*PS.*'),
                              ]
        listOfCalculables += [calculables.vertex.Indices(collection=('vxp_',''),
                                                         zPosMax=100, nTracksMin=4),]
        listOfCalculables += [calculables.jet.IndicesL1(collection=("trig_L1_jet_", "")),
                              calculables.jet.L1Jets(),
                              calculables.jet.IndicesL2(minEt=minEt, input='NON_L15', output='L2CONE'),# regular L2
                              calculables.jet.IndicesL2(minEt=minEt, input='A4TT', output='L2CONE'),   # L2 seeded by L1.5
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A4TT'),     # L1.5 EM
                              calculables.jet.IndicesL2(minEt=minEt, input='NONE', output='A10TT'),    # L1.5 EM
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
        for jColl in ['L1Jets', 'L2JetsNON_L15L2CONE', 'L2JetsA4TTL2CONE',
                      'L2JetsNONEA4TT', 'L2JetsNONEA10TT', 'L2JetsA4TTA4CC_JES'] :
            listOfCalculables += [calculables.jet.MatchedJets(coll1='EfJetsAntiKt4_topo_calib_EMJES',
                                                              otherColls=[jColl])]
        listOfCalculables += [calculables.jet.IndicesOffline(minEt=minEt),
                              calculables.jet.OfflineJets(),
                              calculables.jet.IndicesOfflineBad(),
                              ]
        return listOfCalculables

    def listOfSampleDictionaries(self) :
        protocol="root://xrootd-disk.pic.es/"
        basedir="/pnfs-disk/pic.es/at3/projects/TOPD3PD/2011/Skimming/DPD_prod01_02_October11"
        castorBaseDir="/castor/cern.ch/grid/atlas/tzero/prod1/perm/data12_8TeV/express_express"
        castorDefaultOpt ='fileExt="NTUP_TRIG",pruneList=False'

        lumiPerRun = {202668:26.0, 202712:29.85, 202740:7.28, 202798:52.6, # B1
                      202987:14.02, 202991:40.15, 203027:89.29, #B2
                      }
        exampleDict = supy.samples.SampleHolder()
        exampleDict.add("PeriodB_L1_4J15",
                        'utils.fileListFromTextFile('
                        +'fileName="/afs/cern.ch/work/g/gerbaudo/public/trigger/MyRootCoreDir/supy-d3pdtrig/data/periodB.txt"'
                        +')',
                        lumi= sum(lumiPerRun.keys())
                        )
        return [exampleDict]

    def listOfSamples(self,config) :
        nEventsMax=-1#10000
        return (
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
                      doLog = False,
                      blackListRe = [re.compile(r'num_'), re.compile(r'den_')],
                      ).plotAll()
