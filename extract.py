# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 13:01:48 2017

@author: Ankit Singh
"""
import tarfile
import gzip
import os
import cPickle as pickle
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import seaborn as sns
from scipy import stats

outputdump=[]
def extract(fname,filetowrite,g,logger):
    if (fname.endswith("tar.gz")):
        tar = tarfile.open(fname, "r:gz")
        tar.extractall()
        tar.close()
    elif (fname.endswith("tar")):
        tar = tarfile.open(fname, "r:")
        tar.extractall()
        tar.close()
    elif (fname.endswith("gz")):
        Parse(fname,filetowrite,g,logger)
        
        
def func(files,filetowrite,g,logger):
    for file in files:
        if os.path.isdir(file):
            g=os.path.abspath(file)
            func(os.listdir(g),filetowrite,g,logger)
        else:
            extract(file,filetowrite,g,logger)
 
def Parse(fname,filetowrite,g,logger):
    fname=os.path.join(g,fname)
    f=gzip.open(fname, 'rb')
    #shutil.copyfileobj(f,filetowrite)
#    with open(file, 'r') as f:
    firstline = f.readline().rstrip() 
    identifier=firstline[2:]
    if firstline[5]=='a':
        typeof='alcoholic'
    else:
        typeof='control'
    f.readline()
    f.readline()
    obj=f.readline().split()
    try:
        subject=obj[1]
    except IndexError:
        subject='NotAvailable'
        logger.write("Eror in {0} and {1} " .format(fname,obj))
    while True:
        info=f.readline().split()
        if not info: break
        try:
            channel=info[3]
            logger.write("Eror in {0} and {1} ".format(fname,info))
        except IndexError:
            channel="NotAvailable"
        global outputdump
        #list strcutire['identifier',typeof,subject,channel,trial,sensor position,sample number,sensor value]
    
        for x in xrange(256):
           inputparam=f.readline().rstrip().split()
           try:
               temp=identifier,typeof,subject,channel,inputparam[0],inputparam[1],inputparam[2],inputparam[3]
    #       print temp
               outputdump.append(temp)
           except:
               continue
#    pickle.dump(outputdump,filetowrite)
    #MainProcessing start

        
        
        
        
if __name__=='__main__':
    databasename='output.dat'
#try:
    fil=open(databasename,"rb")
    dataset=pickle.load(fil)
    df = pd.DataFrame(data = dataset, columns=['identifier','typeof','subject','channel','trial','sensorPosition','sampleNumber','sensorValue'])
    #        ild=df[df['subject']=='S1']
#    print df
#    iff=df.groupby(df['channel']).count()
#    ch=df.groupby([df['channel']])['sensorValue'].first()
#    ch=ch.reset_index()
#    #        fig, ax1 = plt.subplots(figsize=(10, 10))
#    ch=ch.astype(float)
#    plt.bar(ch['channel'],ch['sensorValue'])
#    sns.plt.show()
#    pt=df[df['channel']=='56']
#    pt=pt[['channel','sensorValue']]
#    pt=pt.astype(float)
#    x=pt['sensorValue']
#    plt.plot(pt['sensorValue'])
##    plt.plot(ch['channel'])
#    sns.plt.show()
#    q2=pt=df[df['channel']=='56']
#    q2=q2.groupby([df['trial']])['sensorValue'].first()
#    q2=q2.reset_index()
#    print q2
#    q2=q2.astype(float)
#    plt.bar(q2['trial'],q2['sensorValue'])
#    plt.show()
##    q3=df[['channel','trial','sensorValue']]
##    q3=q3.astype(float)
##    q3=q3.groupby([q3['channel'],q3['trial']])['sensorValue'].mean()
##    q3=q3.reset_index()
##    result = df.pivot(index=q3['channel'], columns=q3['trial'], values=q3['sensorValue'])
###    sns.heatmap(result, annot=True, fmt="g", cmap='viridis')
###    plt.show()
##    print q3
#    q3=df[['channel','trial','sensorValue']]
#    q3=q3.astype(float)
#    q3=q3.groupby([q3['channel'],q3['trial']])['sensorValue'].mean()
#    q3=q3.reset_index()
##    print q3
#    plt.figure(figsize=(11,11))
#    result = q3.pivot('channel','trial','sensorValue')
#    sns.heatmap(result, annot=True, fmt="g", cmap='viridis')
#    plt.show()
#    
    
#    maxtillnow=-100000000000
#    electrode1=None
#    electrode2=None
#    listedtrials=df[df['subject']=='S1']
#    listedtrials=listedtrials.groupby([listedtrials['trial']])['sensorValue'].first()
##    print listedtrials
#    listedtrials=listedtrials.reset_index()
#    alltrials=listedtrials['trial'].get_values()
#    for trial in alltrials:
#        q4=df[df['trial']==trial]
#        q4[['channel','sensorValue']]=q4[['channel','sensorValue']].apply(pd.to_numeric)
#        for x in xrange(64):
#            
#            input1=q4[q4['channel']==x]
#            input11=input1['sensorValue']
#            for y in xrange(64):
#                if x == y :
#                    y=y+1
#                    continue
#                input2=q4[q4['channel']==y]
#                input12=input2['sensorValue']
#                out=np.correlate(input11,input12)
#                if out>maxtillnow:
#                    maxtillnow=out
#                    electrode1=input1['sensorPosition'].get_values()[0]
#                    electrode2=input2['sensorPosition'].get_values()[0]
#                y=y+1
#            x=x+1
#        p1=df.groupby(df['sensorPosition']).count()
#        p1=p1.reset_index()
#        print p1[p1['sensorPosition']==electrode1]
#        print p1[p1['sensorPosition']==electrode2]
#        print electrode1,electrode2,maxtillnow
    
    
# creating two groups
    sp=df[['trial','channel','sensorValue']]
    sp=sp.astype(float)
    sns.pairplot(sp)
    listedtrials=df.groupby([df['sensorPosition']])['sensorValue'].first()
#    print listedtrials

    listedtrials=listedtrials.reset_index()
    alltrials=listedtrials['sensorPosition'].get_values()
    trial='CZ'
#for trial in alltrials:
    group1=df[(df['typeof']=='alcoholic') & (df['subject']=='S2') &(df['sensorPosition']==trial)] 
    group1=group1.reset_index()
    group1=group1[['sensorValue']]
    group1=group1.astype(float)
    
    group2=df[(df['typeof']=='control') & (df['subject']=='S2')&(df['sensorPosition']==trial)] 
    group2=group2.reset_index()
    group2=group2[['sensorValue']]
    group2=group2.astype(float)
    
    print group1.describe()
    print group2.describe()
    plt.plot(group1)
    plt.plot(group2)
    plt.show()
    
    sns.distplot(group1)
    sns.distplot(group2)
    plt.show()
    
    print stats.ttest_rel(group1,group2)
    sns.boxplot(group1,color="red")
    plt.show()
    sns.boxplot(group2,color="green")

    plt.show()
    
    print stats.ttest_1samp(group1,0)
    print stats.ttest_ind(group1,group2)

    
#        sns.plt.figure(df)
#        seaborn.barplot(x='Factor', y='Value', hue='Variable', data=tidy, ax=ax1)
#        sns.despine(fig)
#    except:
#        try:
#            filetowrite=open(databasename,"wb") 
#            loggerfile=open('trace.txt',"wb")
#            files=os.listdir(os.getcwd())
#            func(files,filetowrite,os.getcwd(),loggerfile)
#            pickle.dump(outputdump,filetowrite)
#        finally:
#            filetowrite.close()
#            loggerfile.close()