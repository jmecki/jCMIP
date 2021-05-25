# Sets up a structure for a CMIP model object that can get more information about that particular model.

import glob
import calendar
from netCDF4 import Dataset

# Locations of CMIP data on JASMIN:
datadir5 = '/badc/cmip5/data/cmip5/output1/'
datadir6 = '/badc/cmip6/data/CMIP6/'

class CMIPmodel:
    def __init__(self,name,cmip=None,datadir=None,savedir=None,\
                 Ogrid=None,Omeshmask=None,Oreg=True,Olon='unknown',Olat='unknown',OflipNS=False,OextraUV=False,\
                 Agrid=None,Ameshmask=None,Areg=True,Alon='unknown',Alat='unknown',AflipNS=False,AextraUV=False,\
                 Igrid=None,Imeshmask=None,Ireg=True,Ilon='unknown',Ilat='unknown',IflipNS=False,IextraUV=False,\
                 Lgrid=None,Lmeshmask=None,Lreg=True,Llon='unknown',Llat='unknown',LflipNS=False,LextraUV=False):
        self.name = name
        self.cmip = cmip if cmip is not None else 'unknown'
        if datadir is None:
            if self.cmip == '5':
                self.datadir = datadir5
            elif self.cmip == '6':
                self.datadir = datadir6
            else:
                self.datadir = 'unknown'
        self.savedir = savedir if savedir is not None else 'unknown'
        
        # Ocean information:
        self.Ogrid     = Ogrid     if Ogrid     is not None else 'unknown'
        self.Omeshmask = Omeshmask if Omeshmask is not None else 'unknown'
        self.Oreg      = Oreg
        self.Olon      = Olon
        self.Olat      = Olat
        self.OflipNS   = OflipNS
        self.OextraUV  = OextraUV
        
        # Atmosphere information: 
        self.Agrid     = Agrid     if Agrid     is not None else 'unknown'
        self.Ameshmask = Ameshmask if Ameshmask is not None else 'unknown'
        self.Areg      = Areg
        self.Alon      = Alon
        self.Alat      = Alat
        self.AflipNS   = AflipNS
        self.AextraUV  = AextraUV
        
        # Ice information:
        self.Igrid     = Igrid     if Igrid     is not None else 'unknown'
        self.Imeshmask = Imeshmask if Imeshmask is not None else 'unknown'
        self.Ireg      = Ireg
        self.Ilon      = Ilon
        self.Ilat      = Ilat
        self.IflipNS   = IflipNS
        self.IextraUV  = IextraUV
        
        # Land information:
        self.Lgrid     = Lgrid     if Lgrid     is not None else 'unknown'
        self.Lmeshmask = Lmeshmask if Lmeshmask is not None else 'unknown'
        self.Lreg      = Lreg
        self.Llon      = Llon
        self.Llat      = Llat
        self.LflipNS   = LflipNS
        self.LextraUV  = LextraUV
        
        
    # Return institute of model (some models have multiple institutes):
    def getInstitute(self,EXP='*',ENS='*'):
        Inst = []
        if self.cmip == '5':
            tmp = glob.glob((self.datadir + '*/' +  self.name + '/' + EXP + '/*/*/*/' + ENS))
            for tt in tmp:
                Inst.append(tt.split('/')[-7])
            Inst = list(set(Inst))            
            Inst.sort()
        elif self.cmip == '6':
            tmp = glob.glob((self.datadir + '*/*/' + self.name + '/' + EXP + '/' + ENS))
            for tt in tmp:
                Inst.append(tt.split('/')[-4])
            Inst = list(set(Inst))
            Inst.sort()
        else:
            print('Not a valid CMIP')

        return Inst
    
    # Return experiments of model:
    def getMIPs(self,EXP='*',ENS='*',Inst='*'):
        MIPs = []        
        if self.cmip == '5':
            print('Not valid known option for CMIP5')
        elif self.cmip == '6':
            tmp = glob.glob((self.datadir + '*/' + Inst + '/' + self.name + '/' + EXP + '/' + ENS))
            for tt in tmp:
                MIPs.append(tt.split('/')[-5])
            MIPs = list(set(MIPs))
            MIPs.sort()
        else:
            print('Not a valid CMIP')

        return MIPs 
    
    # Return experiments of model:
    def getExperiments(self,ENS='*',Inst='*'):
        EXPs = []        
        if self.cmip == '5':
            tmp = glob.glob((self.datadir + Inst + '/' +  self.name + '/*/*/*/*/' + ENS))
            for tt in tmp:
                EXPs.append(tt.split('/')[-5])
            EXPs = list(set(EXPs))            
            EXPs.sort()
        elif self.cmip == '6':
            tmp = glob.glob((self.datadir + '*/' + Inst + '/' + self.name + '/*/' + ENS))
            for tt in tmp:
                EXPs.append(tt.split('/')[-2])
            EXPs = list(set(EXPs))
            EXPs.sort()
        else:
            print('Not a valid CMIP')

        return EXPs    
    
    # Return files of model for a specfied variable:
    def getFiles(self,var,EXP='*',ENS='*',vtype='*',gtype='gn'): #gtype only CMIP6
        FILEs = []        
        if self.cmip == '5':
            tmp = glob.glob((self.datadir + '*/' + self.name + '/' + EXP + '/*/*/' + vtype + '/' + ENS + '/latest/' + var + '/*'))
            for tt in tmp:
                FILEs.append(tt)
            FILEs = list(set(FILEs))            
            FILEs.sort()
        elif self.cmip == '6':
            tmp = glob.glob((self.datadir + '*/*/' + self.name + '/' + EXP + '/' + ENS + '/' + vtype + '/' + var + '/' + gtype + '/latest/*'))
            for tt in tmp:
                FILEs.append(tt)
            FILEs = list(set(FILEs))
            FILEs.sort()
        else:
            print('Not a valid CMIP')

        return FILEs 
    
    # Return ensemble members for model:
    def getENSs(self,var='*',EXP='*',vtype='*',gtype='gn'): #gtype only CMIP6
        ENSs = []        
        if self.cmip == '5':
            tmp = glob.glob((self.datadir + '*/' + self.name + '/' + EXP + '/*/*/' + vtype + '/*/latest/' + var + '/*'))
            for tt in tmp:
                ENSs.append(tt.split('/')[-4])
            ENSs = list(set(ENSs))            
            ENSs.sort()
        elif self.cmip == '6':
            tmp = glob.glob((self.datadir + '*/*/' + self.name + '/' + EXP + '/*/' + vtype + '/' + var + '/' + gtype + '/latest/*'))
            for tt in tmp:
                ENSs.append(tt.split('/')[-6])
            ENSs = list(set(ENSs))
            ENSs.sort()
        else:
            print('Not a valid CMIP')

        return ENSs 
    
# Return list of models:
def getModels(cmip,EXP='*',ENS='*',var='*',vtype='*',gtype='gn'): #gtype only CMIP6
    Models = []
    if var == '*':
        if ENS == '*':
            if cmip == '5':
                tmp = glob.glob((datadir5 + '*/*/' + EXP))
                for tt in tmp:
                    Models.append(tt.split('/')[-2])
                Models = list(set(Models))            
                Models.sort()
            elif cmip == '6':
                tmp = glob.glob((datadir6 + '*/*/*/' + EXP))
                for tt in tmp:
                    Models.append(tt.split('/')[-2])
                Models = list(set(Models))
                Models.sort()
            else:
                print('Not a valid CMIP')
        else:
            if cmip == '5':
                tmp = glob.glob((datadir5 + '*/*/' + EXP + '/*/*/*/' + ENS))
                for tt in tmp:
                    Models.append(tt.split('/')[-6])
                Models = list(set(Models))            
                Models.sort()
            elif cmip == '6':
                tmp = glob.glob((datadir6 + '*/*/*/' + EXP + '/' + ENS))
                for tt in tmp:
                    Models.append(tt.split('/')[-3])
                Models = list(set(Models))
                Models.sort()
            else:
                print('Not a valid CMIP')
    else:
        if cmip == '5':
            tmp = glob.glob((datadir5 + '*/*/' + EXP + '/*/*/' + vtype + '/' + ENS + '/latest/' + var + '/*'))
            for tt in tmp:
                Models.append(tt.split('/')[-9])
            Models = list(set(Models))            
            Models.sort()
        elif cmip == '6':
            tmp = glob.glob((datadir6 + '*/*/*/' + EXP + '/' + ENS + '/' + vtype + '/' + var + '/' + gtype + '/latest/*'))
            for tt in tmp:
                Models.append(tt.split('/')[-8])
            Models = list(set(Models))
            Models.sort()
        else:
            print('Not a valid CMIP')

    return Models 

# Determine dimensions using a given file and variable:
def getDims(infile,var):
    ncid = Dataset(infile,'r')
    dims = ncid.variables[var].get_dims()
    ncid.close
    
    return dims

# Checks and fixes time if calendars don't match:
def fixTime(units,units2,cal,time,time_bnds):
    if units2 != units:
        yr_init = int(units.split(' ')[2][0:4])
        yr_new  = int(units2.split(' ')[2][0:4])
        nleap   = 0 
        if ((cal == 'standard') | (cal == 'gregorian')):
            days = 365
            for yy in range(yr_init,yr_new):
                if calendar.isleap(yy):
                    nleap = nleap + 1
        elif cal == 'noleap':
            days = 365
        else:
            days = int(cal[0:3])
        offset = days*(yr_new-yr_init) + nleap
        time      = time      + offset
        time_bnds = time_bnds + offset
        
    return time, time_bnds