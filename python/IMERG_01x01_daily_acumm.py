import glob
import re
import numpy as np
import pandas as pd
import clima_anom as ca
from netCDF4 import Dataset

import matplotlib.pyplot as plt

import matplotlib.cbook
import matplotlib.gridspec as gridspec

import cartopy
import cartopy.crs as ccrs

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-yr", "--year", type=str, required=True)
parser.add_argument("-se", "--season", type=str, required=True)

args = vars(parser.parse_args())
year = vars(parser.parse_args())['year']
season = vars(parser.parse_args())['season']

if season == 'summer' or season == 1:
    list_month = [0, 1, 11] # Summer
elif season == 'autumn' or season == 2:
    list_month = [2, 3, 4] # Autumn
elif season == 'winter' or season == 3:
    list_month = [5, 6, 7] # Winter
elif season == 'spring' or season == 4:
    list_month = [8, 9, 10] # Spring
else:
    print(f'Season: {season} not exist')
    exit()

for t in list_month:#range(12):

    month = str(t+1).zfill(2)
    de, _, _, name = ca.days_number(year,month)
    
    lista = glob.glob('/media/arturo/Arturo/Data/IMERG/raw/'+ year +'/*.nc4')
    lista = np.sort(lista)

    lista_month = []
    for tt in range(len(lista)):
        
        filename_split = re.split(r'[/.-]+', lista[tt])[13]
        
        yy = filename_split[0:4]
        mm = filename_split[4:6]
        
        if yy == year and mm == month:

            lista_month.append(lista[tt])

    salida = np.zeros([de,801,650])

    a = 0
    for mm in range(de):

        # print('dia: ',mm+1)
        dd_ref = str(mm+1).zfill(2)
        total_dia = 0

        for nn in range(len(lista_month)):

            filename_split = re.split(r'[/.-]+', lista_month[nn])[13]
            dd = filename_split[6:8]

            if dd == dd_ref:

                data = Dataset(lista_month[nn],mode="r")
                prec = data["precipitationCal"][0,:,:].data.T
                prec[prec==np.min(prec)]=0

                if a == 0:

                    total_dia = np.copy(prec)

                    lat = np.array(data['lat'])
                    lon = np.array(data['lon'])

                    lat_bnd = np.where((lat >= -60) & (lat <= 15))[0]
                    lat = lat[lat_bnd]
                    lon_bnd = np.where((lon >= -90) & (lon <= -30))[0]
                    lon = lon[lon_bnd]

                total_dia = total_dia + prec

            salida[mm,:,:] = total_dia

        a = a + 1

    salida = salida[:,lat_bnd[0]:lat_bnd[-1]+1,lon_bnd[0]:lon_bnd[-1]+1]
    ntime, nlat, nlon = np.shape(salida)

    file_name_out = "/mnt/Data/Data/IMERG/Daily_01x01/IMERG_"+ year +"_"+ month + "_01x01_daily.nc"
    print()
    print(file_name_out)

    info = {'file': file_name_out,
            'title': 'IMERG precipitation data IR + microwave + gauge 0.1x0.1', 
            'year_start':int(year),'month_start':int(month),'day_start':1,'hour_start':0,'minute_start':0,
            'year_end':int(year),'month_end':int(month),'day_end':de,'hour_end':23,'minute_end':55,
            'time_frequency': 'daily', 
            'time_interval': 1,
            'var_name': 'prec', 
            'var_units': 'mm/dia'}

    print()
    ca.create_netcdf(info,salida,lat,lon)
    print()