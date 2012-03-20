from supy.defaults import *
from supy import whereami

def mainTree() :
    return ("susyTree","tree")

def otherTreesToKeepWhenSkimming() :
    return [("lumiTree","tree")]

def trace() :
    return False #True

def useCachedFileLists() :
    return False #True

def cppFiles() :
    return ["../RootCore/scripts/load_packages.C",
            ]

def hadd() :
    return ['hadd', whereami()+'/bin/phaddy'][1]

def cppROOTDictionariesToGenerate() :
    return [
        ("pair<string,bool>", "string"),
        ("map<std::string,bool>", "string;map"),
        ("pair<string,string>", "string"),
        ("map<std::string,string>", "string;map"),
        ("ROOT::Math::Cartesian3D<float>", "Math/Point3D.h"),
        ("ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", "Math/Vector3D.h"),
        ("vector<ROOT::Math::DisplacementVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> >", "vector;Math/Vector3D.h"),
        ("ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>", "Math/Point3D.h"),
        ("vector<ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag> >", "vector;Math/Point3D.h"),
        #ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > etc. is addressed in linkdef.cxx
        ("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > >", "vector;Math/LorentzVector.h"),
        ("vector< vector< float > >", "vector"),
        ("vector< vector< unsigned int> >", "vector"),
        ("vector< vector< int> >", "vector"),
        ]
