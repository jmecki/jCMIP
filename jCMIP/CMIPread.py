# Reads in data from CMIP files, making adjustments.

from netCDF4 import Dataset
import numpy as np

# Reads in lat and lon data from ocean:
def Olatlon(Model,infile,var):
    ncid = Dataset(infile,'r')
    if (Model.name == 'MPI-ESM1-2-XR'):
        if (var == 'uo'):
            if Model.Oreg:
                lon = ncid.variables['lon_2'][:]
                lat = ncid.variables['lat_2'][:]
            else:
                lon = ncid.variables['lon_2'][:,:]
                lat = ncid.variables['lat_2'][:,:]
        elif  (var == 'vo'):
            if Model.Oreg:
                lon = ncid.variables['lon_3'][:]
                lat = ncid.variables['lat_3'][:]
            else:
                lon = ncid.variables['lon_3'][:,:]
                lat = ncid.variables['lat_3'][:,:]
        else:
            if Model.Oreg:
                lon = ncid.variables[Model.Olon][:]
                lat = ncid.variables[Model.Olat][:]
            else:
                lon = ncid.variables[Model.Olon][:,:]
                lat = ncid.variables[Model.Olat][:,:]           
    else:
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
        if not Model.Oreg:
            lon  = np.flip(lon,axis=0)
            
        
    # Extra row in u and v fields (coded only for regular grid):
    if Model.OextraT:
        if ((var == 'vo') | (var == 'uo') | (var == 'tauuo')):
            if Model.Oreg:
                lat = np.concatenate((lat,[-90,]),0)
            else:
                print('need to code')
        
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
        if not Model.Areg:
            lon  = np.flip(lon,axis=0)
        
    # Extra row in u and v fields (coded only for regular grid):
    if Model.AextraT:
        print('Need to code for AextraUV')
        
    return lon,lat

# Reads in data from a 2D ocean field:
def Oread2Ddata(Model,infile,var,time=None,lev=None,mask=False):
    ncid = Dataset(infile,'r')
    if mask:
        if time == None:
            if lev == None:
                data = 1-np.squeeze(ncid.variables[var][:,:]).mask
            else:
                data = 1-np.squeeze(ncid.variables[var][lev,:,:]).mask
        else:
            if lev == None:
                data = 1-np.squeeze(ncid.variables[var][time,:,:]).mask
            else:
                data = 1-np.squeeze(ncid.variables[var][time,lev,:,:]).mask
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
    if Model.OextraT:
        if ((var == 'vo') | (var == 'uo') | (var == 'tauuo')):
            data = np.concatenate((data,np.expand_dims(data[-1,:],0)),0)
        
    return data

# Reads in data from a 3D ocean field:
def Oread3Ddata(Model,infile,var,time=None,mask=False):
    ncid = Dataset(infile,'r')
    if mask:
        if time == None:
            data = 1-np.squeeze(ncid.variables[var][:,:,:]).mask
        else:
            data = 1-np.squeeze(ncid.variables[var][time,:,:,:]).mask
    else:
        if time == None:
            data = np.squeeze(ncid.variables[var][:,:,:]).data
        else:
            data = np.squeeze(ncid.variables[var][time,:,:,:]).data
    ncid.close()
    
    # Flip North-South:
    if Model.OflipNS:
        data = np.flip(data,axis=1)
        
    # Extra row in u and v fields:
    if Model.OextraT:
        if ((var == 'vo') | (var == 'uo') | (var == 'tauuo')):
            data = np.concatenate((data,np.expand_dims(data[:,-1,:],1)),1)
        
    return data

# Reads in data from a 2D atmosphere field:
def Aread2Ddata(Model,infile,var,time=None,lev=None,mask=False):
    ncid = Dataset(infile,'r')
    if mask:
        if time == None:
            if lev == None:
                data = 1-np.squeeze(ncid.variables[var][:,:]).mask
            else:
                data = 1-np.squeeze(ncid.variables[var][lev,:,:]).mask
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
