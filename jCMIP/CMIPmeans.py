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

# Mean of seasonal cycle over several years:
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
    
# Compute seasonal mean:
def seasonal_means(Model,EXP,ENS,var,vtype,mons,outfile,gtype='gn'):
    # Number of months for mean:
    nm = len(mons)

    # List all files:
    files = Model.getFiles(var,EXP=EXP,ENS=ENS,vtype=vtype,gtype=gtype)
    ns = len(files)
    files.sort()
    print(files)

    # Read information from first file:
    ncid  = Dataset(files[0],'r')
    cal   = ncid.variables['time'].calendar
    units = ncid.variables['time'].units
    ncid.close()
    # Check if model has a regular grid:
    if vtype == 'Omon':
        lon,lat = CMIPread.Olatlon(Model,files[0],var)
        if Model.Oreg:
            lon,lat = np.meshgrid(lon,lat)
    elif vtype == 'Amon':
        lon,lat = CMIPread.Alatlon(Model,files[0],var)
        if Model.Areg:
            lon,lat = np.meshgrid(lon,lat)
        
    else:
        print('need to code')
        sys.exit()

    ni = np.size(lon,axis=1)
    nj = np.size(lon,axis=0)

    # Specify and initiate output file:
    modeldir = os.path.dirname(outfile)
    # Make directory if it doesn't exist:
    if not os.path.exists(modeldir):
        os.makedirs(modeldir)
        
    if not os.path.isfile(outfile):
        ncid = Dataset(outfile,'w')
        # Dimensions:
        ncid.createDimension('year',None)
        ncid.createDimension('x',ni)
        ncid.createDimension('y',nj)

        # Variables:
        ncid.createVariable('year','f8',('year',))
        ncid.createVariable('lon', 'f8',('y','x',))
        ncid.createVariable('lat', 'f8',('y','x',))
        ncid.createVariable(var, 'f8',('year','y','x',))

        # Data:
        ncid.variables['lon'][:,:] = lon
        ncid.variables['lat'][:,:] = lat

        ncid.close()  

    # Loop through each file:
    yy = 0
    for ss in range(0,ns):
        infile = files[ss]
        print(infile)
        ncid      = Dataset(infile,'r')
        time      = ncid.variables['time'][:]
        time_bnds = ncid.variables[ncid.variables['time'].bounds][:,:]
        units2    = ncid.variables['time'].units
        ncid.close()

        # Fix dates if they are different:
        if units2 != units:
            print('need to fix dates! - probably not but check!')

        nt = np.size(time,axis=0)
        # Initialize if first file:
        if ss == 0:
            mm   = 0
            days = 0
            tmp  = np.zeros((nj,ni),'float')

        for tt in range(0,nt):
            # Check if one of the months going into the average:
            if (cftime.num2date(time[tt],units2,cal).month == int(mons[mm])):
                days = days + time_bnds[tt,1] - time_bnds[tt,0]
                if vtype == 'Omon':
                    tmp = tmp + CMIPread.Oread2Ddata(Model,infile,var,tt)*(time_bnds[tt,1] - time_bnds[tt,0])
                elif vtype == 'Amon':
                    tmp = tmp + CMIPread.Aread2Ddata(Model,infile,var,tt)*(time_bnds[tt,1] - time_bnds[tt,0])
                else:
                    print('need to code')
                mm = mm + 1
                # Save if it is last month and if so save:
                if mm == nm:
                    year  = cftime.num2date(time[tt],units2,cal).year
                    print(year)
                    ncido = Dataset(outfile, 'a', format='NETCDF4')
                    ncido.variables['year'][yy]  = year
                    ncido.variables[var][yy,:,:] = tmp/days
                    ncido.close()

                    mm   = 0
                    days = 0
                    tmp  = np.zeros((nj,ni),'float')
                    yy = yy + 1 # Count years

    print('-= DONE =-')