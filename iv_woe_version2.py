# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 10:12:16 2017

@author: 
"""
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 13:37:14 2017

@author: lizhiping02
"""

'''
各个维度上的IV/woe值的计算
需要更改的变量：feature/label
分组的组数N
只对 数值型的变量进行计算，按照大小排序，分组
'''

import types
import xlrd
from operator import itemgetter, attrgetter
from scipy import stats
import numpy
import math
import time
import pandas as pd
from dateutil.parser import parser

#data2 = xlrd.open_workbook('D:/18 YMD_iv/caoyujia/extraction_numv2.xlsx')
data2 = xlrd.open_workbook('D:/18 YMD_iv/html5/YMD_DATA_3b.xlsx')
#data2 = xlrd.open_workbook('D:/06 医疗教育维度评价及筛选/new_data/YMD_NEW.xlsx')
table = data2.sheets()[0]    
N_cols = table.ncols
table_label = table.col_values(N_cols-3)

'''
Global variables
'''



#ALL_paras.append(('name_','lost_rate_','woe_','iv_','ks_rate'))
'''
增加label的处理
'''
#for k in range(1,len(table_label)):
#    if(table_label[k]>0.0):
#        table_label[k] = 1


'''
只对连续型变量进行操作，
    挑选出非str类型的变量，计算IV值
'''
ALL_paras = []
ALL_paras.append(('name_','bin','lost_rate_','woe_','iv_'))
N = 20

for j in range(N_cols-2):   #N_cols-2  
    n_str = 0;n_num = 0
    flag_2 = True
    print(j)
    while(flag_2):
       
        feature_ = table.col_values(j) 
        for kk in range(len(feature_)):
            if(type(feature_[kk]) is str):
                n_str +=1
            if(type(feature_[kk]) is float):
                n_num += 1
        if(n_str >= n_num):
            j = j+1
        else:
            flag_2 = False         
    combine_data = []
    feature_ = table.col_values(j)       
    name_ = feature_[0]
    lost_nums =0
    for i in range(1,len(feature_)): 
        feature_[i] = str(feature_[i])
        if(feature_[i] == '-9999' or feature_[i] == '-9999.0' or feature_[i] == '-999999.0' ):
            lost_nums +=1; continue             
        if(feature_[i] == -9999 or feature_[i] == -9999.0 or feature_[i] == -999999.0 ):
            lost_nums +=1;continue
        if(feature_[i] =='NULL'):
            lost_nums +=1;continue                
        if(feature_[i] == '[]'):
            lost_nums +=1; continue             
        if(feature_[i] == ''):
            lost_nums +=1 ;continue   
                 
            #feature_2 = float(feature_[i]);label_ = float(table_label[i]);temp = [feature_2, label_]
        try:    
            feature_2 = float(feature_[i]);label_ = float(table_label[i]);
            temp = [feature_2, label_]
            combine_data.append(temp)
        except Exception  as err0:
            print("NO string",err0)
    if(len(combine_data)!=0):
        combine_data_sorted = sorted(combine_data,reverse = False,key = itemgetter(0))   
        len_valid = len(combine_data_sorted)
            #zhibiao
        lost_rate_ = float(lost_nums/(len(feature_)-1)) 
        data_1 = [t[0] for t in combine_data_sorted];inx_ = 0
        for jj in range(len(data_1)-1):
            if(data_1[jj] == 0):
                inx_ += 1
#        if(lost_rate_ != 1):
#            #name_,bin_,woe_,iv_ = IV_WOE_(combine_data_sorted,N,name_)           
#            #bin_,woe_,iv_= unique_BIN(combine_data_sorted,20)
#            bin_,woe_,iv_= unique_BIN(combine_data,20)
#            #name_,bad_h,good_h,bad_rate,good_rate,ks_rate = KS_(combine_data_sorted,N)
#        else:
#            woe_ = 0.0;iv_ = 0.0
        bin_,woe_,iv_= unique_BIN(combine_data,N)
        ALL_paras.append((name_,bin_,lost_rate_,woe_,iv_))   
    else:
        ALL_paras.append((name_,0,lost_rate_,0,0)) 
        
#data_11.to_csv('D:/TEST/IV_WOE_LOSSRATE_final_ttttt.csv')
import csv
import os
#if(os.path.exists('D:/TEST/IV_WOE_LOSSRATE_final_aa.csv')):
#         os.remove('D:/TEST/IV_WOE_LOSSRATE_final_aa.csv')   
with open('D:/TEST/IV_WOE_LOSSRATE_3b_.csv', 'w') as csvfile:
    #fieldnames = ['name_', 'id', 'bad','good','bad rate','good rate','ks']
    #writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
    csvWriter = csv.writer(csvfile,delimiter=',')
    for data in ALL_paras:
        csvWriter.writerow(data)   



#def KS_(data,N):
#    
#    ks_zhi_rate = 0.0;ks_zhi = [];ks_zhi_temp = 0.0
#    for k in range(1,N+1):
#        step_ = int(len(data)/N)
#        data_all = data
#        data_1 = [t[0] for t in data_all] #feature
#        data_2 = [t[1] for t in data_all] #label
#        data_h = data_2[0:k*step_-1]  
#        if(k== N):
#            data_h = data_2
#        #标签为1的表示坏人
#        bad_all = sum(data_2);good_all = len(data_2)-bad_all;
#        bad_h = sum(data_h);good_h = len(data_h)-bad_h
#        bad_rate =bad_h/bad_all
#        good_rate = good_h/good_all
#        ks_rate = bad_rate-good_rate
#        print(ks_rate)
#        if(ks_zhi_temp <= ks_rate):
#            ks_zhi_temp = ks_rate
        #temp_all = (name_,bad_h,good_h,bad_rate,good_rate,ks_rate)    
    #return (name_,bad_h,good_h,bad_rate,good_rate,ks_rate)  
def unique_BIN(combine_data_sorted,N):
      
    data_all = combine_data_sorted
    data_1 = [t[0] for t in data_all] #feature
    data_2 = [t[1] for t in data_all] #label
   
    data_11 = pd.DataFrame(data_1)
    data_11['label_'] = pd.DataFrame(data_2)
    woe_ = 0.0;iv_temp =0.0
    bad_all = 0
    #data_11['feature_'] = pd.DataFrame(data_1)
    for mm in range(len(data_2)): 
            if(data_2[mm] == 1.0 or data_2[mm] == '1.0' or data_2[mm]== '1' ):
                bad_all += 1
      #bad_all = sum(data_2);
    good_all = len(data_2)-bad_all;   
    
    try:
        data_11['group_bins'] = pd.qcut(data_1,N,duplicates = 'drop')    
        data_11['categories'] = pd.qcut(data_1,N,duplicates = 'drop').codes
        n_sets = list(set(pd.qcut(data_1,N,duplicates = 'drop').codes))
        bad_man = 0;good_man = 0;woe_ = 0.0;iv_temp = 0.0
        good_man_lost = 0;bad_man_lost = 0
        for uu in n_sets:
            bad_man = 0;good_man = 0
            for kk in range(len(data_1)):              
                if(data_11['categories'][kk] == uu):
                    if(data_11['label_'][kk] == 1 or data_11['label_'][kk] == '1' or \
                       data_11['label_'][kk] == 1.0):
                        bad_man += 1
                    if(data_11['label_'][kk] == 0 or data_11['label_'][kk] == '0' or \
                       data_11['label_'][kk] == 0.0):
                        good_man += 1  
            
            good_rate = good_man/good_all;bad_rate = bad_man/bad_all
            if(good_man>0 and bad_man>0):
                woe_ = woe_+ abs(math.log(bad_rate/good_rate))
                iv_temp = iv_temp +(bad_rate-good_rate)*math.log(bad_rate/good_rate) 
                good_man_lost = 0;bad_man_lost = 0
                good_man_add = 0;bad_man_add = 0
            else:
                good_man_lost = good_man_add;
                bad_man_lost = bad_man_add;
            print(uu,woe_,iv_temp)        
        return(len(n_sets),woe_,iv_temp)       
    except Exception as err:
        print("qcut failed",err)
        return (0,woe_,iv_temp)
        
#        dd = data_11.groupby(['group_bins','label_']).size().tolist()
#        good_all = 0;k=0
#        while(k<len(dd)):
#            good_all = dd[k]+good_all;
#            k = k+2
#        
#        bad_all = sum(dd)-good_all
#        if(good_all>0 and bad_all>0 ):
#            for bin_ in range(math.floor(len(dd)/2)):
#                
#                good_rate = dd[2*bin_+0]/good_all
#                bad_rate = dd[2*bin_+1]/bad_all
#                if(good_rate>0 and bad_rate>0):
#                    woe_ = woe_+ abs(math.log(bad_rate/good_rate))
#                    iv_temp = iv_temp +(bad_rate-good_rate)*math.log(bad_rate/good_rate)
#        return (math.floor(len(dd)/2),woe_,iv_temp)
#                
#    except Exception as err:
#        print(err)
#        return (0,woe_,iv_temp)
#


def IV_WOE_(combine_data_sorted,N,name_):
    iv_temp = 0.0;woe_ = 0.0;flag_ =  0 #分组是否成功
    count_ = 0;bad_all = 0;bad_h = 0
    bin_ = 0
    data_all = combine_data_sorted
    data_1 = [t[0] for t in data_all] #feature
    data_2 = [t[1] for t in data_all] #label
    for mm in range(len(data_2)): 
            if(data_2[mm] == 1.0 or data_2[mm] == '1.0' or data_2[mm]== '1' ):
                bad_all += 1
      #bad_all = sum(data_2);
    good_all = len(data_2)-bad_all;   
    count_k = 0
    if(good_all>0 and bad_all>0):    
        for k in range(N):
            #print(k,good_h,bad_h,good_all,bad_all,good_rate,bad_rate,woe_,iv_temp)
            good_h = 0;bad_h = 0       
            step_ = int(len(combine_data_sorted)/N)
            data_h = data_2[k*step_:(k+1)*step_-1]  
            if(k== (N-1)):
                data_h = data_2[(N-1)*step_:len(data_2)-1] 
                #标签为1的表示坏人     
            for nn in range(len(data_h)): 
                if(data_2[nn] == 1.0 or data_2[nn] == '1.0' or data_2[nn]== '1' ):
                    bad_h += 1  
            good_h = len(data_h)-bad_h
            bad_rate =bad_h/bad_all
            good_rate = good_h/good_all
            if(flag_ == 0):
                if(bad_rate>0 and good_rate>0):
                    #print("0",flag_)
                    woe_ = woe_+ abs(math.log(good_rate/bad_rate))
                    iv_temp = iv_temp +(good_rate-bad_rate)*math.log(good_rate/bad_rate)
                    bin_ = bin_+1
                else:
                    flag_ = 1
                    count_ = count_+1
            if(flag_ == 1):
                if(k== (N-1)):
                    data_h = data_2[(N-1)*step_:len(data_2)-1]    
                data_h = data_2[(k-count_)*step_:(k+1)*step_-1]
                
                for nn in range(len(data_h)): 
                    if(data_2[nn] == 1.0 or data_2[nn] == '1.0' or data_2[nn]== '1' ):
                        bad_h += 1  
                good_h = len(data_h)-bad_h       
                bad_rate =bad_h/bad_all
                good_rate = good_h/good_all
                if(bad_rate>0 and good_rate>0):
                    #print("1",flag_)
                    woe_ = woe_+ abs(math.log(good_rate/bad_rate))
                    iv_temp = iv_temp +(good_rate-bad_rate)*math.log(good_rate/bad_rate)
                    bin_ = bin_+1
                    flag_ = 0
                    count_ = 0
                else:
                    flag_ = 1
                    count_ = count_+1 
            print(bin_,good_h,bad_h,good_all,bad_all,good_rate,bad_rate,woe_,iv_temp)
    else:
          woe_ = 0.0;iv_temp = 0.0
    return (name_,bin_,woe_,iv_temp)
    
    
    
    

















#for k in range(N):
#        flag_ =  0 #分组是否成功
#        count_ = 0
#        step_ = int(len(rvs1_deal2)/N)
#    #    data_1 = rvs1_deal2[0:h*step_-1]
#    #    data_2_temp = rvs2_jxj[1:table_jxj.nrows]
#    #    data_2 = data_2_temp[0:h*step_-1]
#        data_all = comp_col
#        data_1 = [t[0] for t in data_all] #feature
#        data_2 = [t[1] for t in data_all] #label
#        data_h = data_2[k*step_:(k+1)*step_-1]  
#        if(k== (N-1)):
#            data_h = data_2[(N-1)*step_:len(data_2)-1] 
#        #标签为1的表示坏人
#        bad_all = sum(data_2);good_all = len(data_2)-bad_all;
#        bad_h = sum(data_h);good_h = len(data_h)-bad_h
#        bad_rate =bad_h/bad_all
#        good_rate = good_h/good_all
#        if(flag_ == 0):
#            if(bad_rate>0 and good_rate>0):
#                woe_ = woe_+ abs(math.log(good_rate/bad_rate))
#                iv_temp = iv_temp +(good_rate-bad_rate)*math.log(good_rate/bad_rate)
#            else:
#                flag_ = 1
#                count_ = count_+1
#        if(flag_ == 1):
#            if(k== (N-1)):
#                data_h = data_2[(N-1)*step_:len(data_2)-1] 
#            data_h = data_2[(k-count_)*step_:(k+1)*step_-1]
#            bad_h = sum(data_h);good_h = len(data_h)-bad_h
#            bad_rate =bad_h/bad_all
#            good_rate = good_h/good_all
#            if(bad_rate>0 and good_rate>0):
#                woe_ = woe_+ abs(math.log(good_rate/bad_rate))
#                iv_temp = iv_temp +(good_rate-bad_rate)*math.log(good_rate/bad_rate)
#                flag_ = 0
#                count_ = 0
#            else:
#                flag_ = 1
#                count_ = count_+1
#           
#            
#        # ks_rate = bad_rate-good_rate
##        if(ks_zhi_temp <= ks_rate):
##            ks_zhi_temp = ks_rate
##        temp_all = (name_,bad_h,good_h,bad_rate,good_rate,ks_rate) 
##        ks_plot.append(temp_all)        
#IV_TEMP =(name_,woe_,iv_temp)        
#    #计算每个因子的kS值
#IV.append(IV_TEMP)







'''
数据预处理模块：
unique = 1, 直接打上标签，不参与进行IV的计算,会包括header,所以
unique = 2 ,直接打上标签，不参与计算
top值很高，而且freq很大时，将top值替换成0 
pd.DataFrame(feature_).describe()
Out[464]: 
             0
count   5479.0
unique     8.0
top        0.0
freq    5418.0

 pd.Series(feature_).value_counts()
Out[465]: 
0.0                   5418
1.0                     21
                        21
2.0                      8
-9999.0                  7
3.0                      2
holmestype1passcnt       1
0.0                      1
dtype: int64

'''
##'''
#    pd.DataFrame(feature_).describe().index[1]
#    pd.DataFrame(feature_).describe().values[0]
#    pd.Series(feature_).value_counts().index[3]
#    pd.Series(feature_).value_counts().values[3]
#    unique_ = float(pd.DataFrame(feature_).describe().values[1]) 
#    top_ = 
#    
#    if(unique_ <=2):
#        j += 1
#        feature_ = table.col_values(j)
#    else:
#        
#    
#    
    
    
#'''











