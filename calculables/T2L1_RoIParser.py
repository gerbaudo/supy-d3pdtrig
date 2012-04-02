
# Decode the RoI word associated with a TrigT2Jet.
#
# The RoI word is an unsigned integer encoding information about the jet (provenance etc.)
# see Trigger/TrigAlgorithms/TrigT2CaloJet/trunk/TrigT2CaloJet/T2L1Tools.h for the definition of these constants.
# We do not use the 32 bits available in an unsigned int.
# The lower eight bits are used to identify the jet number ('counter').
# In addition, we use two 8-bit words: one to define the input, and one for the output
# see here for L1.5 specific info : https://twiki.cern.ch/twiki/bin/viewauth/Atlas/TrigJetL15

eightBits = 255

roi_type_dictionary = {
    "NONE"           : 0x01,
    "L1SW8x8"        : 0x02,
    "L2CONE"         : 0x03,
    "A4TT"           : 0x04,
    "A4TT_JES"       : 0x05,
    "A4TT_TC"        : 0x06,
    "A4TT_TC_JES"    : 0x07,
    "A4TT_PU_SUB"    : 0x08,
    "A10TT"          : 0x09,
    "A4JE"           : 0x10,
    "A4JE_JES"       : 0x11,
    "A4JE_TC"        : 0x12,
    "A4JE_TC_JES"    : 0x13,
    "A4JE_PU_SUB"    : 0x14,
    "A4CC"           : 0x15,
    "A10JE"          : 0x20,
    "UNCALIBRATED"   : 0x30,
    "CALIBRATED"     : 0x31,
    "UNKNOWN"        : 0x40,
    "SET_INPUT"      : 0x10000,
    "GET_INPUT"      : 0x10000 * eightBits,
    "SET_OUTPUT"     : 0x100,
    "GET_OUTPUT"     : 0x100 * eightBits,
}

SET_INPUT  = roi_type_dictionary["SET_INPUT"]
GET_INPUT  = roi_type_dictionary["GET_INPUT"]
SET_OUTPUT = roi_type_dictionary["SET_OUTPUT"]
GET_OUTPUT = roi_type_dictionary["GET_OUTPUT"]
BLANKWORD  = 0x70000000
inputMask = BLANKWORD + GET_INPUT
outputMask = BLANKWORD + GET_OUTPUT

# generate dictionaries with (key=bit, value=label)
roiInputBits = dict([(BLANKWORD + SET_INPUT * v, k) for k,v in roi_type_dictionary.iteritems()])
roiOutputBits = dict([(BLANKWORD + SET_OUTPUT * v, k) for k,v in roi_type_dictionary.iteritems()])

def input(word, verbose=False):
    iw = word & inputMask  # input word
    inputType = roiInputBits.get(iw, "UNKNOWN")
    return inputType

def output(word, verbose=False) :
    ow = word & outputMask # output word
    outputType = roiOutputBits.get(ow, "UNKNOWN")
    return outputType

def counter(word, verbose=False) :
    return  word & eightBits

def inputOutput(word, verbose=False) :
    return input(word, verbose), output(word, verbose)

def inputOutputJetCounter(word, verbose=False) :
    return input(word, verbose), output(word, verbose), counter(word, verbose)


