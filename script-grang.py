#Import libraries:OK
import pandas as pd #dataframes
from pandas import Series
from statsmodels.tsa.stattools import adfuller
from collections import namedtuple #tuples
import scipy.stats #F-test
import numpy as np #array operations 
import matplotlib.pyplot as plt #plots
from scipy.stats.stats import pearsonr #standard statistics
from statsmodels.tsa.stattools import grangercausalitytests as gct #grenger test  
#/Import libraries

#Parameters#
show_adf=1;lag=3;#ADF tests
show_granger=1;#Granger test

show_plots=1;#Show plots
show_corr=show_plots
show_slope=show_corr;

x_string='D'#X
y_string='S'#Y
#/Parameters#

#Read files .csv
dpr=pd.read_csv("RU/dpr.csv",sep=',',index_col=0,skiprows=1,encoding='utf-8')
ins=pd.read_csv("RU/ins.csv",sep=',',index_col=0,skiprows=1,encoding='utf-8')
srs=pd.read_csv("RU/srs.csv",sep=',',index_col=0,skiprows=1,encoding='utf-8')
scd=pd.read_csv("RU/scd.csv",sep=',',index_col=0,skiprows=1,encoding='utf-8')
#/Read files .csv

#DF differences#
dpr_diff=dpr.diff();dpr_diff.drop(dpr_diff.head(1).index, inplace=True);dpr_diff=dpr_diff.values;dpr_diff=[int(item) for item in dpr_diff]
ins_diff=ins.diff();ins_diff.drop(ins_diff.head(1).index, inplace=True);ins_diff=ins_diff.values;ins_diff=[int(item) for item in ins_diff]
srs_diff=srs.diff();srs_diff.drop(srs_diff.head(1).index, inplace=True);srs_diff=srs_diff.values;srs_diff=[int(item) for item in srs_diff]
scd_diff=scd.diff();scd_diff.drop(scd_diff.head(1).index, inplace=True);scd_diff=scd_diff.values;scd_diff=[int(item) for item in scd_diff]
#/DF differences#

#ADF-test#
if show_adf==1: 
  result=adfuller(dpr_diff)
  print('ADF Statistic-Depression: %f' % result[0]);print('p-value: %f' % result[1]);print('Critical Values:')
  for key, value in result[4].items():print('\t%s: %.3f' % (key, value))
  
  result=adfuller(ins_diff)
  print('ADF Statistic-Insomnia: %f' % result[0]);print('p-value: %f' % result[1]);print('Critical Values:')
  for key, value in result[4].items():print('\t%s: %.3f' % (key, value))

  result=adfuller(srs_diff)
  print('ADF Statistic-Stress: %f' % result[0]);print('p-value: %f' % result[1]);print('Critical Values:')
  for key, value in result[4].items():print('\t%s: %.3f' % (key, value))

  result=adfuller(scd_diff)
  print('ADF Statistic-Suicide: %f' % result[0]);print('p-value: %f' % result[1]);print('Critical Values:')
  for key, value in result[4].items():print('\t%s: %.3f' % (key, value))
#/ADF-test#

#Labels#
if x_string=='D' and y_string=='I':
  x_var=dpr.values;x_label=str(dpr.columns[0]).partition(':')[0].title()
  y_var=ins.values;y_label=str(ins.columns[0]).partition(':')[0].title()
  x_diff=dpr_diff;y_diff=ins_diff
  
if x_string=='I' and y_string=='D':
  x_var=ins.values;x_label=str(ins.columns[0]).partition(':')[0].title()
  y_var=dpr.values;y_label=str(dpr.columns[0]).partition(':')[0].title()
  x_diff=ins_diff;y_diff=dpr_diff
  
if x_string=='D' and y_string=='S':
  x_var=dpr.values;x_label=str(dpr.columns[0]).partition(':')[0].title()
  y_var=srs.values;y_label=str(srs.columns[0]).partition(':')[0].title()
  x_diff=dpr_diff;y_diff=srs_diff
  
if x_string=='S' and y_string=='D':
  x_var=srs.values;x_label=str(srs.columns[0]).partition(':')[0].title()
  y_var=dpr.values;y_label=str(dpr.columns[0]).partition(':')[0].title()
  x_diff=srs_diff;y_diff=dpr_diff
  
if x_string=='I' and y_string=='S':
  x_var=ins.values;x_label=str(ins.columns[0]).partition(':')[0].title()
  y_var=srs.values;y_label=str(srs.columns[0]).partition(':')[0].title()
  x_diff=ins_diff;y_diff=srs_diff
  
if x_string=='S' and y_string=='I':
  x_var=srs.values;x_label=str(srs.columns[0]).partition(':')[0].title()
  y_var=ins.values;y_label=str(ins.columns[0]).partition(':')[0].title()
  x_diff=srs_diff;y_diff=ins_diff

if x_string=='S' and y_string=='C':
  x_var=srs.values;x_label=str(srs.columns[0]).partition(':')[0].title()
  y_var=scd.values;y_label=str(scd.columns[0]).partition(':')[0].title()
  x_diff=srs_diff;y_diff=scd_diff

if x_string=='D' and y_string=='C':
  x_var=dpr.values;x_label=str(dpr.columns[0]).partition(':')[0].title()
  y_var=scd.values;y_label=str(scd.columns[0]).partition(':')[0].title()
  x_diff=dpr_diff;y_diff=scd_diff

if x_string=='I' and y_string=='C':
  x_var=ins.values;x_label=str(ins.columns[0]).partition(':')[0].title()
  y_var=scd.values;y_label=str(scd.columns[0]).partition(':')[0].title()
  x_diff=ins_diff;y_diff=scd_diff   
#/Labels#

#Granger causaility test# 
if show_granger==1:
  print(50*'-');print(str(y_label)+'['+str(x_label)+']'); 
  matrix=np.column_stack([y_diff,x_diff])#array: y_var/x_var
  gt=gct(matrix,3,verbose=False)#[y-x] cause
  gr_test=[item for item in gt.get(lag)[0]['params_ftest']];
  F_crit=int(round(scipy.stats.f.ppf(q=(1-gr_test[1]), dfn=gr_test[3], dfd=gr_test[2])))
  print("Lag="+str(lag))#F/F_crit
  print('p='+str(format(gr_test[1], '.5f')))#p-value
  print("[F/F_crit]="+str(format(gr_test[0]/F_crit, '.2f')))#F/F_crit
#/Granger causality test#    

#Correlation#
if show_corr==1:
  CFV=pearsonr(x_var,y_var)
  CF=str(round(100*CFV[0][0]))
  S=str(round(100*(1-CFV[1][0])))
  CF_T='CF='+CF+'%'+' '+'S[p]='+S+'%\n'
  print('CF='+CF+'%'+' '+'S[p]='+S+'%')
  print('N='+str(len(x_var))+' months');
#/Correlation#

#Regression#
x_var=[int(item) for item in x_var]
y_var=[int(item) for item in y_var]
reg=np.polyfit(x_var,y_var,1)

if show_slope==1:
  k=('Slope k='+str(round(10*reg[0])/10))#Regression slope
  print(k);
#/Regression

#Plot#
if show_plots==1:
  fig=plt.figure(x_label+' '+'vs'+' '+y_label+' - с 2004 г.')
  plt.xlabel(x_label);plt.ylabel(y_label) 
  plt.title(CF_T+'N='+str(len(x_var))+' months'+' k='+str(format(reg[0],'.1f')))
  plt.plot(x_var,y_var,'ro')
  plt.plot(x_var,(reg[0]*np.asarray(x_var)+reg[1]),'-')
  plt.show()
#Plot#

#OK-State#
print(50*'-')  
print('Finished!')  
#OK-State# 
















