#streamlit run reg.py

import streamlit as st
import pandas as pd
import datetime
import numpy as np

pd.options.display.float_format = '{:.1f}'.format
tod = datetime.datetime.now()

dt_now = st.date_input('開催日', tod)
date = str(dt_now.strftime('%m/%d'))
month = int(dt_now.strftime('%m'))

df = pd.read_csv('member.csv', encoding = 'UTF-8-sig')

l_mem = df['なまえ'].tolist()

new = st.text_input('新規参加者（なまえ）', '')
l_new = [new]

if st.button('追加'):
    df_n = pd.DataFrame()
    df_n['なまえ'] = l_new
    df_c = pd.concat([df, df_n], axis=0)
    df_c.to_csv('member.csv', encoding = 'UTF-8-sig',index=False)

st.sidebar.write('参加者')

num = 0
l_bool = []  
for mem in l_mem:
    if st.sidebar.checkbox(mem):
        l_bool.append('出')
        num = num + 1
    else:
        l_bool.append('欠')
        
df_d = pd.DataFrame()
df_d['参加'] = l_bool
df_d['なまえ'] = l_mem
df_d['日付'] = date
df_d['参加点'] = 2

df_d = df_d.query('参加 == "出"')
l_part = df_d['なまえ'].tolist() 


l_po = []
for part in l_part:
    po = st.select_box(part, (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20))
    l_po.append(po)

df_d['得点'] = l_po
df_d.drop(columns='参加', inplace=True)

st.write(str(num) +'人参加')
st.write(df_d)

df_org = pd.read_csv('master.csv', encoding = 'UTF-8-sig')

df_add = pd.concat([df_org, df_d], axis=0)

if st.button('データベース更新'):
    df_add.to_csv('master.csv', encoding = 'UTF-8-sig',index=False)
