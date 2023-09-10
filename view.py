#streamlit run view.py

import streamlit as st
import pandas as pd
import datetime
import numpy as np
import pickle
from PIL import Image

st.set_page_config(page_title="得点表", layout="wide")
pd.options.display.float_format = '{:.1f}'.format
dt_now = datetime.datetime.now()
date = str(dt_now.strftime('%m/%d'))
month = int(dt_now.strftime('%m'))

st.title('SAKURA 得点表')

df_all = pd.read_csv('master.csv', encoding = 'UTF-8-sig')
df_all['参加点'] = 2
    
l_mm = []
l_dd = []
l_date = df_all['日付'].tolist()
for date in l_date:
    x = date.find('月')
    dd = date[x+1:]
    if len(dd) == 2:
        dd = '0' + dd
    l_dd.append(dd)
    mm = date[0:x+1]
    l_mm.append(mm)

l_vmm = ['9月', '8月', '7月', '6月', '5月', '4月', '3月', '2月', '1月'] 
#l_vmm = ['12月', '11月', '10月', '9月']

target = st.selectbox(label="＜表示月選択＞", options=l_vmm)

y = target.find('月')
mo = target[0:y]

pri = (int(mo)-1) %3 + 1
l_pri = [pri, pri + 3, pri + 6]
 
prize =   '入賞順位：' + str(pri) + '位，' + str(pri + 3) + '位，' + str(pri + 6) + '位'
st.write(prize)

df_all['月'] = l_mm
df_all['日付'] = l_dd

df2 = df_all[df_all['月'] == mo + '月']


df3 = pd.pivot_table(df2, index='なまえ', columns='日付', values='得点', margins=True, margins_name='得点合計', aggfunc=np.sum)
df3 = df3.fillna(0)
df3 = df3.reset_index()

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

df3 = df3[1:]
df3.iloc[:,1:] = df3.iloc[:,1:].astype('int')

l_namae = df3['なまえ'].tolist() 

l_win = []
r = 1
for namae in l_namae:
    if r in l_pri:
        l_win.append('★')
    else:
        l_win.append('')      
    r = r + 1

pd.options.display.float_format = '{:.2f}'.format
df3.insert(0, '入賞', l_win)
df3 = df3.drop('平均', axis=1)

st.dataframe(df3)

df_p.set_index('なまえ',inplace=True)
st.write('\n\n得点グラフ')
st.bar_chart(df_p)

l_kiku = ['聞かない', '聞く']
hitori = st.selectbox(label="＜ひとりごと＞", options=l_kiku)
if hitori == '聞く':
    st.write('Ｕ１８野球代表おめでとう！)
