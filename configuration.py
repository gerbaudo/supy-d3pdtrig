from supy.defaults import *
import supy

def mainTree() :
    return ("/","trigger")

def otherTreesToKeepWhenSkimming() :
    return []

def trace() :
    return False #True

def useCachedFileLists() :
    return False #True

def cppFiles() :
    return ["../RootCore/scripts/load_packages.C",
            "cpp/linkdef.cxx",
            ]

def haddErrorsToIgnore() :
    return supy.defaults.haddErrorsToIgnore() + \
           ["Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<bool>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<char>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<short>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<long>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<unsigned-char>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<unsigned-short>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<unsigned-int>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<unsigned-long>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<float>=vector.dll vectorbool.dll> for level 0; ignored\n"
            +"Warning in <TEnvRec::ChangeValue>: duplicate entry <Library.vector<double>=vector.dll vectorbool.dll> for level 0; ignored\n",
            ]

def initializeROOT(r, cppFiles = []) :
    supy.defaults.initializeROOT(r, cppFiles)
    r.load_packages()
