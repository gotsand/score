#streamlit run view.py

import streamlit as st
import pandas as pd
import datetime
import numpy as np
import pickle

pd.options.display.float_format = '{:.1f}'.format
dt_now = datetime.datetime.now()
date = str(dt_now.strftime('%m/%d'))
month = int(dt_now.strftime('%m'))

pri = (month-1)%3 + 1

l_pri = [pri, pri + 3, pri + 6]

head = str(month) + '月'
prize =   '入賞順位：' + str(pri) + '位，' + str(pri + 3) + '位，' + str(pri + 6) + '位'
st.title(head)
st.header(prize)

df_all = pd.read_csv('master.csv', encoding = 'UTF-8-sig')
    
l_mm = []
l_dd = []
l_date = df_all['日付'].tolist()
for date in l_date:
    x = date.find('月')
    dd = date[x+1:]
    if len(dd) == 2:
        dd = '0' + dd
    l_dd.append(dd)
    mm = date[0:x]
    l_mm.append(mm)

l_vmm = ['9月', '10月']

target = st.selectbox(label="表示月選択", options=l_vmm)

df_all['月'] = l_mm
df_all['日付'] = l_dd

df2 = df_all.query('月 == @target')

df3 = pd.pivot_table(df2, index='なまえ', columns='日付', values='得点', margins=True, margins_name='得点合計', aggfunc=np.sum)
df3 = df3.fillna(0)
df3 = df3.reset_index()

df_g = df3

df4 = pd.pivot_table(df2, index='なまえ', columns='日付', values='参加点', margins=True, margins_name='参加点', aggfunc=np.sum)
df4 = df4.fillna(0)
df4 = df4.reset_index()

df5 = pd.pivot_table(df2, index='なまえ', columns='日付', values='得点', margins=True, margins_name='平均', aggfunc=np.mean)
df5 = df5.fillna(0)
df5 = df5.reset_index()

df6 = pd.pivot_table(df_all, index='なまえ', values=['得点', '参加点'], margins=True, margins_name='得点合計', aggfunc=np.sum)
df6 = df6.fillna(0)
df6 = df6.reset_index()
df6['年間累積'] = df6['得点'] + df6['参加点']

df7 = pd.DataFrame()
df7['なまえ'] = df6['なまえ']
df7['年間累積'] = df6['年間累積']

df3['参加点'] = df4['参加点']
df3['平均'] = df5['平均']
df3['合計'] = df3['得点合計'] + df4['参加点']
df3 = df3.drop('得点合計', axis=1)

df_p = df3.iloc[0:-1,0:-2]

df3 = pd.merge(df3, df7, on='なまえ', how='left')
df3 = df3.sort_values(['合計', '平均'], ascending=False).reset_index(drop=True)

df3 = df3[1:].astype('str')
l_means = df3['平均'].tolist()

l_ave = []
for means in l_means:
    ave = means[0:4]
    l_ave.append(ave)
df3['平均'] = l_ave

l_namae = df3['なまえ'].tolist() 

l_win = []
r = 1
for namae in l_namae:
    if r in l_pri:
        l_win.append('★')
    else:
        l_win.append('')      
    r = r + 1

pd.options.display.float_format = '{:.1f}'.format
df3.insert(0, '入賞', l_win)

st.dataframe(df3, width=1000)  
df_p.set_index('なまえ',inplace=True)

st.write('\n\n')
st.bar_chart(df_p)
