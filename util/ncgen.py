import os

from tempfile import NamedTemporaryFile

import netCDF4
import numpy as np

from grids import bc_400m, canada_5k, world_125k, world_250k, timescales

def get_base_nc(fname, dims):
    nc = netCDF4.Dataset(fname, 'w')

    l = dims['lat']
    lat = nc.createDimension('lat', l['count'])
    var_lat = nc.createVariable('lat', 'f4', 'lat')
    var_lat.axis = 'Y'
    var_lat.units = 'degrees_north'
    var_lat.long_name = 'latitude'
    var_lat[:] = np.linspace(l['start'], l['start'] + l['step'] * l['count'], l['count'])

    l = dims['lon']
    lon = nc.createDimension('lon', l['count'])
    var_lon = nc.createVariable('lon', 'f4', 'lon')
    var_lon.axis = 'X'
    var_lon.units = 'degrees_east'
    var_lon.long_name = 'longitude'
    var_lon[:] = np.linspace(l['start'], l['start'] + l['step'] * l['count'], l['count'])

    return nc

def add_climo_1970_time(nc, unlim=False):
    dim_length = 17 if not unlim else 0
    time = nc.createDimension('time', dim_length)
    var_time = nc.createVariable('time', 'i4', 'time')
    #                J     F     M     A     M     J     J     A     S     O     N     D    DJF   MAM   JJA   SON   ANN
    var_time[0:17] = [5493, 5524, 5552, 5583, 5613, 5644, 5674, 5705, 5736, 5766, 5797, 5827, 5493, 5583, 5674, 5766, 5659] # FIXME: Are seasonal indices right?

    var_time.axis = 'T'
    var_time.units = 'days since 1970-01-01'
    var_time.calendar = 'gregorian'
    var_time.long_name = 'time'

    cb = nc.createDimension('bnds', 2)
    var_cb = nc.createVariable('climatology_bounds', 'i4', ('time', 'bnds'))
    climo_bnds = [0, 10988,
                 31, 11017,
                 59, 11048,
                 90, 11078,
                 120, 11109,
                 151, 11139,
                 181, 11170,
                 212, 11201,
                 243, 11231,
                 273, 11262,
                 304, 11292,
                 334, 11323,
                 0, 11017,
                 59, 11109,
                 151, 11201,
                 243, 11292,
                 0, 11323]
    var_cb[:] = np.array(climo_bnds).reshape(17, 2)
    
    return nc

def add_simple_time(nc, timescale, unlim=False):
    dim_length = len(timescale) if not unlim else 0
    time = nc.createDimension('time', dim_length)
    var_time = nc.createVariable('time', 'i4', 'time')
    var_time[:] = timescale
    var_time.axis = 'T'
    var_time.units = 'records since 1950-01-01'
    var_time.calendar = 'gregorian'
    var_time.long_name = 'time'
    return nc

def add_climo_data(nc, name, attributes={}, timemajor=True):
    if timemajor:
        var = nc.createVariable(name, 'f4', ('time', 'lat', 'lon'), fill_value=1e20)
    else:
        var = nc.createVariable(name, 'f4', ('lat', 'lon', 'time'), fill_value=1e20)
    for key, val in attributes.items():
        setattr(var, key, val)
    for i in range(var.shape[0]):
        var[i,:,:] = np.random.randn(var.shape[1], var.shape[2])
    return nc

def get_bc_highres_nc(fname, unlim=False, timemajor=True):
    nc = get_base_nc(fname, bc_400m)
    nc = add_climo_1970_time(nc, unlim)
    attributes = {'standard_name': 'air_temperature',
                  'long_name': 'Daily Maximum Near-Surface Air Temperature',
                  'units': 'K',
                  'missing_value': 1e20
                 }
    nc = add_climo_data(nc, 'tasmax', attributes, timemajor)
    return nc

def make_multivariable_nc(fname, num_vars=1, unlim=False):
    nc = get_base_nc(fname, bc_400m)
    nc = add_climo_1970_time(nc, unlim)

    for i in range(num_vars):
        nc = add_climo_data(nc, 'var_{}'.format(i))
    return nc

def make_nc(fname, num_vars=1, grid=bc_400m, timescale=timescales['seasonal'], unlim=False, timemajor=True):
    nc = get_base_nc(fname, grid)
    nc = add_simple_time(nc, timescale, unlim=unlim)

    for i in range(num_vars):
        nc = add_climo_data(nc, 'var_{}'.format(i), timemajor=timemajor)
    return nc

def make_canada_5k_climo_nc(fname, num_vars=1, unlim=False, timemajor=True):
    nc = get_base_nc(fname, canada_5k)
    nc = add_climo_1970_time(nc, unlim)

    for i in range(num_vars):
        nc = add_climo_data(nc, 'var_{}'.format(i))
    return nc

def make_world_125k_climo_nc(fname, num_vars=1, unlim=False, timemajor=True):
    nc = get_base_nc(fname, world_125k)
    nc = add_climo_1970_time(nc, unlim)

    for i in range(num_vars):
        nc = add_climo_data(nc, 'var_{}'.format(i))
    return nc

def make_world_250k_climo_nc(fname, num_vars=1, unlim=False, timemajor=True):
    nc = get_base_nc(fname, world_250k)
    nc = add_climo_1970_time(nc, unlim)

    for i in range(num_vars):
        nc = add_climo_data(nc, 'var_{}'.format(i))
    return nc

if __name__ == '__main__':
    from tempfile import NamedTemporaryFile

    for grid in [bc_400m, canada_5k, world_125k, world_250k]:
        with NamedTemporaryFile(dir=os.getcwd(), suffix='.nc') as f:
            nc = make_nc(f.name, grid=grid)
            print(nc)
