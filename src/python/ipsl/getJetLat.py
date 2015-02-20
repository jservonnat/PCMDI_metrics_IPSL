import cdutil,cdms2
import MV2 as MV
import numpy as np


def compute(dm,hemisphere="NHEX"):
    """ Search for the latitude of the Subtropical jet"""
    """ Works on ua_200 """
    """ Separate NH and SH """
    """ returns both the values and diff with the reference """
    # -- Set the bounds
    #cdutil.setTimeBoundsMonthly(dm)
    # -- Get the hemisphere and compute the zonal mean
    if hemisphere=="NHEX":
       zonmean=cdutil.averager(dm(lat=(20.,80.)),axis='x')
    if hemisphere=="SHEX":
       zonmean=cdutil.averager(dm(lat=(-80.,-20.)),axis='x')
    # -- get the latitude values
    latitudes = np.array(zonmean.getLatitude())
    # -- Get the latitude of the max of the zonal mean
    if len(dm.shape)==2:
       max_index = np.where(zonmean == zonmean.max())[0]
    if len(dm.shape)==3:
       max_index = np.where(zonmean == zonmean.max())[1]
    
    # calcul des coefficients a, b et c de l'equation ax2 + bx + c regression des 3 points autour du maximum
    if len(zonmean.shape)==1:
       y1 = zonmean[max_index[0]-1]
       y2 = zonmean[max_index[0]]
       y3 = zonmean[max_index[0]+1]
    if len(zonmean.shape)==2:
       y1 = zonmean[0,max_index[0]-1]
       y2 = zonmean[0,max_index[0]]
       y3 = zonmean[0,max_index[0]+1]
    
    x1 = latitudes[max_index[0]-1]
    x2 = latitudes[max_index[0]]
    x3 = latitudes[max_index[0]+1]

    a = ((x2-x3)*(y1-y2) - (x1-x2)*(y2-y3)) / ((x1**2-x2**2)*(x2-x3) - (x2**2-x3**2)*(x1-x2))
    b = ((y1-y2) - a*(x1**2-x2**2)) / (x1-x2);
    #c = y1 - a*x1**2 - b*x1;
    
    # sommet de la parabole
    xmax = -b / (2*a)

    # --> For the model and the reference
    # --> return the value for NH and SH
    #return MV.float(MV.average(MV.subtract(dm,do))
    return xmax
    #return NHbias,SHbias,NHmaxULat_model,SHmaxULat_model,NHmaxULat_ref,SHmaxULat_ref

