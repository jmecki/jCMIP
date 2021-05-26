##############################################################################
#
# Computes means over specified time periods:
#
# #############################################################################

def meanSC(Model,EXP,ENS,var,styr,fnyr,dtype='gn'):
    modeldir = (Model.savedir + EXP + '/')

    outfile = (modeldir + var + '_' + Model.name + '_'
               + EXP + '_' + ENS + '_' + dtype + '_'
               + str(styr) + '01-' + str(fnyr) + '12_SC.nc')
    print(outfile)
'''
if os.path.isfile(outfile):
    print('file already exists - no need to compute')
else:
    # Make directory if it doesn't exist:
    if not os.path.exists(modeldir):
        os.makedirs(modeldir)
    
    # Extract all files needed for the computations:

    Files = Model.getFilesOmon(EXP,ENS,var)
    nf = len(Files)
    
    ncid = Dataset((Model.savedir + 'mesh_mask.nc'),'r')
    dims = ncid.variables['tmask'].get_dims()
    ncid.close
    
    nx = dims[3].size
    ny = dims[2].size
    nz = dims[1].size
    nyr = fnyr-styr+1

    # Get latitude and longitude:
    vlon = Model.vlon
    vlat = Model.vlat
    
    print(Files[0])
    
    if Model.reg:
        lon = read.read1Dflat(Model.name,Files[0],vlon)
        lat = read.read1Dflat(Model.name,Files[0],vlat)
    else:
        lon = read.read2Dflat(Model.name,Files[0],vlon)
        lat = read.read2Dflat(Model.name,Files[0],vlat)
        
    if ((Model.name[0:7] == 'HadGEM2') & ((var == 'uo') | (var == 'vo'))):
        lat = np.concatenate((lat,[-90,]),0)
        
    lev = read.read1Dflat(Model.name,Files[0],dims[1].name)

    # Loop through all files and add together the relavent years:

    data = np.zeros((12,nz,ny,nx),'float')
    days = np.zeros((12),'float')
    bnds = np.zeros((12,2),'float')
    nn = 0

    # Loop through all files:
    for ff in range(0,nf):
        # Get time information from file:
        ncid = Dataset(Files[ff],'r')
        time  = ncid.variables[dims[0].name][:]
        bounds = ncid.variables[dims[0].name].bounds
        time_bnds = ncid.variables[bounds][:,:]
        cal   = ncid.variables[dims[0].name].calendar
        units = ncid.variables[dims[0].name].units
        ncid.close()
        if Model.name == 'FGOALS-g2':
            units = (units + '-01')  
            
        nt = np.size(time)
            
        for tt in range(0,nt):
            yr = cftime.num2date(time[tt],units,cal).year
            mm = cftime.num2date(time[tt],units,cal).month
            
            if ((yr >= styr) & (yr <= fnyr)):
                nn = nn + 1
                ncid = Dataset(Files[ff],'r')
                tmp = read.read3D(Model.name,Files[ff],var,tt)
                ncid.close()
                data[mm-1,:,:,:] = data[mm-1,:,:,:] + tmp
                days[mm-1] = days[mm-1] + time[tt]
                bnds[mm-1,:] = bnds[mm-1,:] + time_bnds[tt,:]

    data = data/nyr
    days = days/nyr
    bnds = bnds/nyr

    # Save data to file:
    ncid = Dataset(outfile, 'w', format='NETCDF4')
    # coordinates:
    ncid.createDimension(dims[3].name,nx)
    ncid.createDimension(dims[2].name,ny)
    ncid.createDimension(dims[1].name,nz)
    ncid.createDimension(dims[0].name,None)
    ncid.createDimension('bnds',2)
    # variables:
    if Model.reg:
        ncid.createVariable(vlon,'f8',(dims[3].name,))
        ncid.createVariable(vlat,'f8',(dims[2].name,))
    else:
        ncid.createVariable(vlon,'f8',(dims[2].name,dims[3].name,))
        ncid.createVariable(vlat,'f8',(dims[2].name,dims[3].name,))
    ncid.createVariable(dims[1].name,'f8',(dims[1].name,))
    ncid.createVariable(dims[0].name,'f8',(dims[0].name,))
    ncid.createVariable(bounds,'f8',(dims[0].name,'bnds',))
    ncid.createVariable(var,'f8',(dims[0].name,dims[1].name,dims[2].name,dims[3].name,))
    
    
    ncid.variables[dims[0].name].calendar = cal
    ncid.variables[dims[0].name].units    = units
    ncid.variables[dims[0].name].bounds   = bounds

    # fill variables:
    if Model.reg:
        ncid.variables[vlon][:] = lon
        ncid.variables[vlat][:] = lat
    else:
        ncid.variables[vlon][:,:] = lon
        ncid.variables[vlat][:,:] = lat
    ncid.variables[dims[1].name][:] = lev
    ncid.variables[dims[0].name][0:12] = days
    ncid.variables[bounds][:,:] = bnds
    ncid.variables[var][0:12,:,:,:] = data

    # close:
    ncid.close()

# Delete submit file after successful computation:
lfile = ('mean_' + var + '_' + Model.name + '_' +  EXP + '_' + ENS + '_SC.slurm')
os.remove(lfile)

'''
