##############################################################################
#
# Computes means over specified time periods:
#
# #############################################################################

import os
import numpy as np
from netCDF4 import Dataset
import cftime

from . import CMIPobject
from . import CMIPread

def meanSC(Model,EXP,ENS,var,vtype,styr,fnyr,outfile,gtype='gn'):
    modeldir = os.path.dirname(outfile)
    
    # Make directory if it doesn't exist:
    if not os.path.exists(modeldir):
        os.makedirs(modeldir)
    
    # Find all files needed for the computations:
    Files = Model.getFiles(var,EXP=EXP,ENS=ENS,vtype=vtype,gtype=gtype)
    nf = len(Files)
    
    # Get model information:
    dims  = CMIPobject.getDims(Files[0],var)
    nd    = len(dims)   
    nyr   = fnyr - styr + 1
    dtime = dims[0].name
    dlon  = dims[nd-1].name
    nx    = dims[nd-1].size
    dlat  = dims[nd-2].name
    ny    = dims[nd-2].size
    if nd == 4:
        dlev = dims[1].name
        nz   = dims[1].size
    if Model.OextraUV:  # Add more as required:
        if ((var == 'vo') | (var == 'uo') | (var == 'tauuo')):
            ny = ny + 1
                    
    # Get latitude and longitude:
    extra = False
    if vtype == 'Omon':
        nlon = Model.Olon
        nlat = Model.Olat
        reg  = Model.Oreg
        lon,lat = CMIPread.Olatlon(Model,Files[0],var)
    elif vtype == 'Amon':
        nlon = Model.Alon
        nlat = Model.Alat
        reg  = Model.Areg
        lon,lat = CMIPread.Alatlon(Model,Files[0],var)
    else:
        print((vtype + ' is an invalid/uncoded type'))
        
    # Loop through all files and add together the relavent years:
    if nd == 3:
        data = np.zeros((12,ny,nx),'float')
    elif nd == 4:
        data = np.zeros((12,nz,ny,nx),'float')  
    days = np.zeros((12),'float')
    bnds = np.zeros((12,2),'float')
    nn = 0

    # Loop through all files:
    for ff in range(0,nf):
        # Get time information from file:
        ncid = Dataset(Files[ff],'r')
        time   = ncid.variables[dtime][:]
        bounds = ncid.variables[dtime].bounds
        time_bnds = ncid.variables[bounds][:,:]
        cal   = ncid.variables[dtime].calendar
        units = ncid.variables[dtime].units
        ncid.close()
        if Model.name == 'FGOALS-g2':
            units = (units + '-01')  
            
        nt = np.size(time)
            
        for tt in range(0,nt):
            yr = cftime.num2date(time[tt],units,cal).year
            mm = cftime.num2date(time[tt],units,cal).month
            
            if ((yr >= styr) & (yr <= fnyr)):
                nn = nn + 1
                if vtype == 'Omon':
                    if nd == 3:
                        tmp = CMIPread.Oread2Ddata(Model,Files[ff],var,time=tt)
                    elif nd == 4:
                        tmp = CMIPread.Oread3Ddata(Model,Files[ff],var,time=tt) 
                elif vtype == 'Amon':
                    if nd == 3:
                        tmp = CMIPread.Aread2Ddata(Model,Files[ff],var,time=tt)
                    elif nd == 4:
                        print('Need to code 3D atmosphere reading in of data') 
                else:
                    print((vtype + ' is not coded yet!'))
                data[mm-1,:,:] = data[mm-1,:,:] + tmp
                days[mm-1]     = days[mm-1] + time[tt]
                bnds[mm-1,:]   = bnds[mm-1,:] + time_bnds[tt,:]

    data = data/nyr
    days = days/nyr
    bnds = bnds/nyr
    
    # Save data to file:
    ncid = Dataset(outfile, 'w', format='NETCDF4')
    # coordinates:
    ncid.createDimension(dlon,nx)
    ncid.createDimension(dlat,ny)
    if nd == 4:
        ncid.createDimension(dlev,nz)
    ncid.createDimension(dtime,None)
    ncid.createDimension('bnds',2)
    # variables:
    if reg:
        ncid.createVariable(nlon,'f8',(dlon,))
        ncid.createVariable(nlat,'f8',(dlat,))
    else:
        ncid.createVariable(nlon,'f8',(dlat,dlon,))
        ncid.createVariable(nlat,'f8',(dlat,dlon,))
    ncid.createVariable(dtime,'f8',(dtime,))
    ncid.createVariable(bounds,'f8',(dtime,'bnds',))
    if nd == 4:
        ncid.createVariable(dlat,'f8',(dlev,))
        ncid.createVariable(var,'f8',(dtime,dlev,dlat,dlon,))
    else:
        ncid.createVariable(var,'f8',(dtime,dlat,dlon,))
    
    
    ncid.variables[dtime].calendar = cal
    ncid.variables[dtime].units    = units
    ncid.variables[dtime].bounds   = bounds

    # fill variables:
    if reg:
        ncid.variables[nlon][:] = lon
        ncid.variables[nlat][:] = lat
    else:
        ncid.variables[nlon][:,:] = lon
        ncid.variables[nlat][:,:] = lat
    ncid.variables[dtime][0:12]   = days
    ncid.variables[bounds][:,:]   = bnds
    if nd == 3:
        ncid.variables[var][0:12,:,:] = data
    elif nd == 4:
        ncid.variables[var][0:12,:,:,:] = data

    # close:
    ncid.close()