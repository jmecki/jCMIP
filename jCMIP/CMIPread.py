# Reads in data from CMIP files, making adjustments.

from netCDF4 import Dataset
import numpy as np

# Reads in lat and lon data from ocean:
def Olatlon(Model,infile,var):
    ncid = Dataset(infile,'r')
    if Model.Oreg:
        lon = ncid.variables[Model.Olon][:]
        lat = ncid.variables[Model.Olat][:]
    else:
        lon = ncid.variables[Model.Olon][:,:]
        lat = ncid.variables[Model.Olat][:,:]
    ncid.close()
    
    # Flip North-South:
    if Model.OflipNS:
        lat  = np.flip(lat,axis=0)
        
    # Extra row in u and v fields (coded only for regular grid):
    if Model.OextraUV:
        if ((var == 'vo') | (var == 'uo') | (var == 'tauuo')):
            lat = np.concatenate((lat,[-90,]),0)
        
    return lon,lat

# Reads in lat and lon data from atmosphere:
def Alatlon(Model,infile,var):
    ncid = Dataset(infile,'r')
    if Model.Areg:
        lon = ncid.variables[Model.Alon][:]
        lat = ncid.variables[Model.Alat][:]
    else:
        lon = ncid.variables[Model.Alon][:,:]
        lat = ncid.variables[Model.Alat][:,:]
    ncid.close()
    
    # Flip North-South:
    if Model.AflipNS:
        lat  = np.flip(lat,axis=0)
        
    # Extra row in u and v fields (coded only for regular grid):
    if Model.AextraUV:
        print('Need to code for AextraUV')
        
    return lon,lat

# Reads in data from a 2D ocean field:
def Oread2Ddata(Model,infile,var,time=None,lev=None,mask=False):
    ncid = Dataset(infile,'r')
    if mask:
        if time == None:
            if lev == None:
                data = np.squeeze(ncid.variables[var][:,:]).mask
            else:
                data = np.squeeze(ncid.variables[var][lev,:,:]).mask
        else:
            if lev == None:
                data = np.squeeze(ncid.variables[var][time,:,:]).mask
            else:
                data = np.squeeze(ncid.variables[var][time,lev,:,:]).mask
    else:
        if time == None:
            if lev == None:
                data = np.squeeze(ncid.variables[var][:,:]).data
            else:
                data = np.squeeze(ncid.variables[var][lev,:,:]).data
        else:
            if lev == None:
                data = np.squeeze(ncid.variables[var][time,:,:]).data
            else:
                data = np.squeeze(ncid.variables[var][time,lev,:,:]).data
    ncid.close()
    
    # Flip North-South:
    if Model.OflipNS:
        data = np.flip(data,axis=0)
        
    # Extra row in u and v fields:
    if Model.OextraUV:
        if ((var == 'vo') | (var == 'uo')):
            data = np.concatenate((data,np.expand_dims(data[-1,:],0)),0)
        
    return data

# Reads in data from a 2D atmosphere field:
def Aread2Ddata(Model,infile,var,time=None,lev=None,mask=False):
    ncid = Dataset(infile,'r')
    if mask:
        if time == None:
            if lev == None:
                data = np.squeeze(ncid.variables[var][:,:]).mask
            else:
                data = np.squeeze(ncid.variables[var][lev,:,:]).mask
        else:
            if lev == None:
                data = np.squeeze(ncid.variables[var][time,:,:]).mask
            else:
                data = np.squeeze(ncid.variables[var][time,lev,:,:]).mask
    else:
        if time == None:
            if lev == None:
                data = np.squeeze(ncid.variables[var][:,:]).data
            else:
                data = np.squeeze(ncid.variables[var][lev,:,:]).data
        else:
            if lev == None:
                data = np.squeeze(ncid.variables[var][time,:,:]).data
            else:
                data = np.squeeze(ncid.variables[var][time,lev,:,:]).data
    ncid.close()
    
    # Flip North-South:
    if Model.AflipNS:
        data = np.flip(data,axis=0)
        
    return data
