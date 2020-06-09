# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 20:26:06 2020

@author: Hongyong
"""

import pandas as pd
import os

#计数器
A='tat' #set your station name

TimeHour=range(24)
TimeMinite=range(60)

def GetCount(x):
    if x<10:
        x='0'+str(x)
    else:
        x=str(x)
    return(x)
    
def GetMean(data,variable):
    thisdata=data[variable]
    thisdata2=thisdata.mean()
    #nullnum=thisdata.isnull().sum()
    #nullrate=nullnum/len(thisdata)
    return(thisdata2)

#set your variable name like BSRN1 file
#you can copy it from BSRN1 data
variabletoRead=['Date/Time','Latitude','Longitude', \
           'Direct radiation [W/m**2]', 'Long-wave downward radiation [W/m**2]', \
           'Long-wave upward radiation [W/m**2]', 'Air temperature [deg C]', \
           'Humidity, relative [%]', 'Station pressure [hPa]']
variabletoGet=['Date/Time', \
           'Direct radiation [W/m**2]', 'Long-wave downward radiation [W/m**2]', \
           'Long-wave upward radiation [W/m**2]', 'Air temperature [deg C]', \
           'Humidity, relative [%]', 'Station pressure [hPa]']

filePlace="F://BSRNyear//"+A+"//"
fileList=os.listdir(filePlace)

newStation='F://BSRNhour//'
okstation=os.listdir(newStation)
if (A in okstation)== False:
    os.mkdir(newStation+A)
    
targetPlace=newStation+A+'//'

for i in range(len(fileList)): 
    thisyearhourData=pd.DataFrame(columns=variabletoGet)  #set your variable name
    fileName=filePlace+fileList[i]
    dataOne = pd.read_table(fileName,sep=",",names=variabletoRead,header=0) 
    usedata=dataOne[variabletoGet]
    yearforthis=fileList[i][4:8] ### if station name>3 need to change this number
    startday=usedata['Date/Time'].loc[0]
    startday=startday[5:7]+startday[8:10]
    endday=usedata['Date/Time'].loc[len(usedata)-1]
    endday=endday[5:7]+endday[8:10]
    TimeList=pd.date_range(yearforthis+startday, yearforthis+endday,freq='1D') 
#start to calculate

    for date in range(len(TimeList)):
        for hours in range(24):

            if (hours!=0)==True:
                standardtime1=str(TimeList[date].strftime("%Y-%m-%d"))+'T'+GetCount(hours-1)+':'+'30'
                standardtime2=str(TimeList[date].strftime("%Y-%m-%d"))+'T'+GetCount(hours)+':'+'30'
                avgtime1=usedata[usedata['Date/Time']==standardtime1].index[0]
                avgtime2=usedata[usedata['Date/Time']==standardtime2].index[0] 
                #thisSlice is important for data extraction
                thisSlice=usedata[avgtime1:avgtime2+1]
            elif (hours==0)==True:
                if (date!=0)==True:
                    standardtime1=str(TimeList[date-1].strftime("%Y-%m-%d"))+'T'+GetCount(23)+':'+'30' 
                    standardtime2=str(TimeList[date].strftime("%Y-%m-%d"))+'T'+GetCount(0)+':'+'30'                
                    avgtime1=usedata[usedata['Date/Time']==standardtime1].index[0]
                    avgtime2=usedata[usedata['Date/Time']==standardtime2].index[0] 
                    #thisSlice is important for data extraction
                    thisSlice=usedata[avgtime1:avgtime2+1]
                elif (date==0)==True:
                    if (i==0)==True:
                        thisSlice=thisyearhourData
                    elif (i!=0)==True:
                        piece1=usedata[:31]
                        j=i-1
                        fileNameP=filePlace+fileList[j]
                        dataOneP=pd.read_table(fileNameP,sep=",",names=variabletoRead,header=0) 
                        usedataP=dataOneP[variabletoGet]
                        piece2=usedataP[-30:]
                        thisSlice=pd.concat([piece2,piece1],ignore_index=True)
                        thisSlice=thisSlice.reset_index(drop=True)
                    
            mytime=str(TimeList[date].strftime("%Y-%m-%d"))+'T'+GetCount(hours)+':'+'00'        

            thisyearhourData=thisyearhourData.append(pd.DataFrame({variabletoGet[0]:[mytime], \
                                           variabletoGet[1]:[GetMean(thisSlice,variabletoGet[1])], \
                                           variabletoGet[2]:[GetMean(thisSlice,variabletoGet[2])], \
                                           variabletoGet[3]:[GetMean(thisSlice,variabletoGet[3])], \
                                           variabletoGet[4]:[GetMean(thisSlice,variabletoGet[4])], \
                                           variabletoGet[5]:[GetMean(thisSlice,variabletoGet[5])], \
                                           variabletoGet[6]:[GetMean(thisSlice,variabletoGet[6])]}),ignore_index=True)
        print(yearforthis,date,' has been completed, you smart ass.')
    thisyearhourData.to_csv(targetPlace+A+'__'+str(yearforthis)+'.txt', sep=' ', \
                  header=True,index=False,encoding = 'utf_8_sig')
    print(yearforthis,' has successfully generated.')
            
        