from eppy import modeleditor
from eppy.modeleditor import IDF
import pandas as pd
import re
import os
import subprocess
from eppy.results import readhtml
from glob import glob
import multiprocessing
from time import time
from geometry_utils import *


iddfile = "Energy+.idd"
IDF.setiddname(iddfile)

city=["agadir","casa","errachidia","fes","marrakech","rabat","tanger"]
orientation=[0, 90, 180]
lengths=[10,30,50,70,90]
widths=[20,40,60,80,100]
heights=[3.5,7]
fenestration=[0.1,0.15,0.2,0.25,0.3,0.35,0.4]
fname=[]
for f in city:
    fname.append(f+".idf")
weather=["weather/"+w+".epw" for w in city]
total= len(fname)*len(orientation)*len(lengths)*len(widths)*len(heights)*len(fenestration)

def batch():
    t_id=[]
    city_id=[]
    length=[]
    width=[]
    height=[]
    window=[]
    orient=[]
    i=1
    for fname1 in fname:
        idf1 = IDF('baseline/'+fname1)
        for orientation1 in orientation:
            for length1 in lengths:
                for width1 in widths:
                    for height1 in heights:
                        for fenes in fenestration:
                                idf1.idfobjects["ZONE"][0].Direction_of_Relative_North=orientation1
                                idf1=surfaces(idf1, x=length1, y=width1, z=height1)
                                idf1=windows(idf1, p=fenes)
                                city1=re.search('(.*).idf',fname1).group(1)
                                t_id.append(i)
                                city_id.append(city1)
                                length.append(length1)
                                width.append(width1)
                                height.append(height1)
                                window.append(fenes)
                                orient.append(orientation1)
                                idf1.saveas('idf_files/'+city1+str(i)+'.idf')
                                print(str(i)+"/"+str(total))
                                i+=1
    data_raw={'id':t_id,
             'city': city_id,
             'length':length,
             'width': width,
             'height': height,
             'orientation':orient,
             'window_ratio': window
             }
    df=pd.DataFrame(data_raw)
    df.to_csv("model_inputs.csv",index=False)

def simulate(fname):
    subprocess.call("EnergyPlus -d sim_result -p "+fname+" -w weather/"+re.search("([a-z]+)([0-9]+).idf",fname).group(1)+".epw -r idf_files/"+fname, shell=True)

def multi_simulation(n_files=None):
    begin=time()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    if n_files==None:
        files = os.listdir('idf_files/')
    else:
        files = os.listdir("idf_files/")[:n_files]
    r = pool.map_async(simulate, files)
    r.wait()
    print("Finished in: "+str(time()-begin))


def results():
    t_id=[]
    cooling=[]
    heating=[]
    files=glob('sim_result/*.htm')
    i=1
    for file1 in files:
        filehandle = open(file1, 'r').read()
        htables = readhtml.titletable(filehandle)
        t_id.append(re.search('sim_result/([a-z]*)([0-9]*).idf(.*).htm',file1).group(2))
        cooling.append(htables[3][1][-1][4])
        heating.append(htables[3][1][-1][5])
        print(str(i)+"/"+str(total))
        i=i+1
    data_raw={'id':t_id,
              'cooling': cooling,
              'heating': heating
             }
    df=pd.DataFrame(data_raw)
    df.to_csv("model_outputs.csv",index=False)

def join_final():
    inputs=pd.read_csv('model_inputs.csv')
    outputs=pd.read_csv('model_outputs.csv')
    df=inputs.merge(outputs,on='id')
    df.to_csv("model_final.csv",index=False)

if __name__ == '__main__':
    batch()
    multi_simulation()
    results()
    join_final()
