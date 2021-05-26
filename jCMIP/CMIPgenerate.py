##############################################################################
#
# Generates list of CMIP model objects:
#
# #############################################################################

import _pickle as pickle
import CMIPobject as co

def generateList(outfile):
    print(outfile)
    
    Models = co.getModels(cmip='6')
    print(Models)