# -*- coding: utf-8 -*-
"""Home Credit Default Risk_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qR_o7n3Kvrhbx1ydOmjNX82MKleowjHu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

! gdown 17O-10vq80ufw9S6qCyAC2Tqvf134-iPV

! gdown 1E9saoE5S637izLNz-oONPKpUEolD--iB

! gdown 1xqc9H6S1v8MvnZSp_Q9AJ-eMCigKOdW7

! gdown 1CnwpyDtYOPfkAb6p6THXTOx8U9VrJit2

! gdown 1Gqze15BQlp-hxvX6wYK5J7Yjaepv503S

! gdown 1Gs76Oi6DjWgTvCQ92Yv_IlqrVsEJMLJh

! gdown 1Xgu9bqigQYOvROPl2Fku6iPvG-zNxQgP

! gdown 1fkF1-1KDoVcQcbJzzRvYZb9AjyHqqgrJ

! gdown 1FiSbRKMwXnYzpV4LnJ-XKxdknAU1Y9j7

def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage(deep=True).sum() / 1024 ** 2 # just added 
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    percent = 100 * (start_mem - end_mem) / start_mem
    print('Mem. usage decreased from {:5.2f} Mb to {:5.2f} Mb ({:.1f}% reduction)'.format(start_mem, end_mem, percent))
    return df

train=pd.read_csv('application_train.csv')
test=pd.read_csv('application_test.csv')
POS_CASH_balance=pd.read_csv('POS_CASH_balance.csv')
bureau=pd.read_csv('bureau.csv')
bureau_balance=pd.read_csv('bureau_balance.csv')
credit_card_balance=pd.read_csv('credit_card_balance.csv')
installments_payments=pd.read_csv('installments_payments.csv')
previous_application=pd.read_csv('previous_application.csv')

train=reduce_mem_usage(train)
test=reduce_mem_usage(test)
POS_CASH_balance=reduce_mem_usage(POS_CASH_balance)
bureau=reduce_mem_usage(bureau)
bureau_balance=reduce_mem_usage(bureau_balance)
credit_card_balance=reduce_mem_usage(credit_card_balance)
installments_payments=reduce_mem_usage(installments_payments)
previous_application=reduce_mem_usage(previous_application)

print('dataset length:',len(train),'\n')
L=[col for col in train.columns if (train[col].isna().sum()/len(train))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')

print('dataset length:',len(test),'\n')
L=[col for col in test.columns if (test[col].isna().sum()/len(test))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')

print('dataset length:',len(POS_CASH_balance),'\n')
L=[col for col in POS_CASH_balance.columns if (POS_CASH_balance[col].isna().sum()/len(POS_CASH_balance))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
POS_CASH_balance.isna().sum()

print('dataset length:',len(bureau),'\n')
L=[col for col in bureau.columns if (bureau[col].isna().sum()/len(bureau))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
bureau.isna().sum()

print('dataset length:',len(bureau_balance),'\n')
L=[col for col in bureau_balance.columns if (bureau_balance[col].isna().sum()/len(bureau_balance))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
bureau_balance.isna().sum()

print('dataset length:',len(credit_card_balance),'\n')
L=[col for col in credit_card_balance.columns if (credit_card_balance[col].isna().sum()/len(credit_card_balance))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
credit_card_balance.isna().sum()

print('dataset length:',len(installments_payments),'\n')
L=[col for col in installments_payments.columns if (installments_payments[col].isna().sum()/len(installments_payments))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
installments_payments.isna().sum()

print('dataset length:',len(previous_application),'\n')
L=[col for col in previous_application.columns if (previous_application[col].isna().sum()/len(previous_application))>0.7]
print('No. of columns with more than 70% NaN:', len(L),L,'\n')
previous_application.isna().sum()

def feature_prec_risk(feature):
  temp1=train.groupby([feature], as_index=False)['TARGET'].count()
  temp2=train.groupby([feature], as_index=False)['TARGET'].sum().rename({'TARGET':'total_risk'}, axis=1)
  temp1=pd.concat([temp1, temp2['total_risk']], axis=1)
  temp1['percent_risk']=temp1['total_risk']/temp1['TARGET']*100
  temp1=temp1.sort_values(by='percent_risk', ascending=False)

  sns.set_theme(style="darkgrid")
  sns.barplot(x=feature, y='percent_risk', data=temp1)
  plt.xticks(rotation=90)

  del temp1, temp2

sns.set_theme(style="darkgrid")
sns.countplot(x='TARGET', data=train)

sns.set_theme(style="darkgrid")
sns.countplot(x='CODE_GENDER', data=train)

feature_prec_risk('CODE_GENDER')

sns.set_theme(style="darkgrid")
sns.countplot(x='NAME_CONTRACT_TYPE', data=train)

feature_prec_risk('NAME_CONTRACT_TYPE')

sns.set_theme(style="darkgrid")
sns.countplot(x='NAME_INCOME_TYPE', data=train)
plt.xticks(rotation=90)

feature_prec_risk('NAME_INCOME_TYPE')

"""Income is right skewed"""

sns.set_theme(style="darkgrid")
sns.countplot(x='NAME_EDUCATION_TYPE', data=train)
plt.xticks(rotation=90)

feature_prec_risk('NAME_EDUCATION_TYPE')

sns.set_theme(style="darkgrid")
sns.countplot(x='NAME_HOUSING_TYPE', data=train)
plt.xticks(rotation=90)

feature_prec_risk('NAME_HOUSING_TYPE')

feature_prec_risk('CNT_CHILDREN')

feature_prec_risk('OCCUPATION_TYPE')

feature_prec_risk('WEEKDAY_APPR_PROCESS_START')

"""==> Weekdays of process start almost have same share of payment difficaulties"""

sns.distplot(train['AMT_INCOME_TOTAL'])

"""==> Income amount is highly right skewed"""

train['TARGET'].corr(train['AMT_INCOME_TOTAL'])

map={'Lower secondary':0,'Secondary / secondary special':1,'Incomplete higher':2,'Higher education':3,'Academic degree':4 }
train['NAME_EDUCATION_TYPE']=train['NAME_EDUCATION_TYPE'].map(map)
train['TARGET'].corr(train['NAME_EDUCATION_TYPE'])

"""==> The higher customer education level the lower risk"""

train['TARGET'].corr(train['REGION_POPULATION_RELATIVE'])

""" ==> Higher population area lower risk of default"""

train['TARGET'].corr(-train['DAYS_BIRTH'])

"""==> The Older Client the Lower risk of Default"""

train['TARGET'].corr(-train['DAYS_EMPLOYED'])

"""==> More days employed higher risk of default"""

train['TARGET'].corr(-train['DAYS_ID_PUBLISH'])

train['TARGET'].corr(train['REGION_RATING_CLIENT'])

train['TARGET'].corr(train['REGION_RATING_CLIENT_W_CITY'])

L=[col for col in train.columns if col.endswith('_AVG')]
sns.set_style('whitegrid')
plt.figure()
fig, ax = plt.subplots(5,3,figsize=(14,14))
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    
for i in range(13):
      plt.subplot(5,3,i+1)
      sns.distplot(train[L[i]])

L=[col for col in train.columns if col.endswith('_MODE')]
sns.set_style('whitegrid')
plt.figure()
fig, ax = plt.subplots(5,3,figsize=(14,14))
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    
for i in range(13):
      plt.subplot(5,3,i+1)
      sns.distplot(train[L[i]])

L=[col for col in train.columns if col.endswith('_MEDI')]
sns.set_style('whitegrid')
plt.figure()
fig, ax = plt.subplots(5,3,figsize=(14,14))
plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
    
for i in range(13):
      plt.subplot(5,3,i+1)
      sns.distplot(train[L[i]])

train_bureau=train.merge(bureau, on='SK_ID_CURR', how='left')

def feature_prec_risk_bureau(feature):
  temp1=train_bureau.groupby([feature], as_index=False)['TARGET'].count()
  temp2=train_bureau.groupby([feature], as_index=False)['TARGET'].sum().rename({'TARGET':'total_risk'}, axis=1)
  temp1=pd.concat([temp1, temp2['total_risk']], axis=1)
  temp1['percent_risk']=temp1['total_risk']/temp1['TARGET']*100
  temp1=temp1.sort_values(by='percent_risk', ascending=False)

  sns.set_theme(style="darkgrid")
  sns.barplot(x=feature, y='percent_risk', data=temp1)
  plt.xticks(rotation=90)

  del temp1, temp2

feature_prec_risk_bureau('CREDIT_ACTIVE')

feature_prec_risk_bureau('CNT_CREDIT_PROLONG')

feature_prec_risk_bureau('CREDIT_TYPE')

sns.distplot(bureau['AMT_CREDIT_SUM'])

sns.distplot(bureau['AMT_CREDIT_SUM_DEBT'])

train_previous_app=train.merge(previous_application, on='SK_ID_CURR', how='left')

def feature_prec_risk_prev_app(feature):
  temp1=train_previous_app.groupby([feature], as_index=False)['TARGET'].count()
  temp2=train_previous_app.groupby([feature], as_index=False)['TARGET'].sum().rename({'TARGET':'total_risk'}, axis=1)
  temp1=pd.concat([temp1, temp2['total_risk']], axis=1)
  temp1['percent_risk']=temp1['total_risk']/temp1['TARGET']*100
  temp1=temp1.sort_values(by='percent_risk', ascending=False)

  sns.set_theme(style="darkgrid")
  sns.barplot(x=feature, y='percent_risk', data=temp1)
  plt.xticks(rotation=90)

  del temp1, temp2

feature_prec_risk_prev_app('NAME_CONTRACT_TYPE_y')

feature_prec_risk_prev_app('NAME_CASH_LOAN_PURPOSE')

feature_prec_risk_prev_app('NAME_CONTRACT_STATUS')

"""==> Clients with refused previous applications, have payment difficaulties for current credits"""