# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:29:51 2020

@author: Hongyong
"""

import os
import pandas as pd

A='tat' #set your station name

monthStation='F://BSRNuse//'+A+'//'   #'F://BSRNuse//' is the place to have original data
newStation='F://BSRNyear//'  #'F://BSRNyear//' is the place to have the annual data after running this code
okstation=os.listdir(newStation)
if (A in okstation)== False:
    os.mkdir(newStation+A)
year2Station=newStation+A+'//'

variable=['Date/Time','Latitude','Longitude', \
           'Direct radiation [W/m**2]', 'Long-wave downward radiation [W/m**2]', \
           'Long-wave upward radiation [W/m**2]', 'Air temperature [deg C]', \
           'Humidity, relative [%]', 'Station pressure [hPa]'] #your can select the variable by check the original data file
#start to merge

monthlist=os.listdir(monthStation)
for yearcount in range(1992,2020,1): #set your years
    yearfile=[]
    for i in range(len(monthlist)):
        if (str(yearcount) in monthlist[i])==True:
            yearfile.append(monthlist[i])
    if len(yearfile) !=0 :
        thisyearData=pd.DataFrame(columns=variable)
        for j in range(len(yearfile)):
            fileName=monthStation+yearfile[j]
            dataOne = pd.read_table(fileName,sep='	',header=0)
            #dataOne.columns.values.tolist()
            #use that to get the variable you want
            dataOne=dataOne[variable]
            thisyearData=pd.concat([thisyearData,dataOne],ignore_index=True)
            thisyearData=thisyearData.reset_index(drop=True) 
            print('Absorb ',fileName, ', please wait...')
        thisyearData.to_csv(year2Station+A+'_'+str(yearcount)+'.txt', sep=',', \
                  header=True,index=False,encoding = 'utf_8_sig')
        print('Get this data: ', A+'_'+str(yearcount))

