#streamlit run reg.py

import streamlit as st
import pandas as pd
import datetime
import numpy as np

pd.options.display.float_format = '{:.1f}'.format

dt_now = st.date_input(
    '開催日',
    datetime.date(2022, 1, 1))
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

l_bool = []  
for mem in l_mem:
    if st.sidebar.checkbox(mem):
        l_bool.append('出')
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
    po = st.number_input(part,0,100,0)
    l_po.append(po)

df_d['得点'] = l_po
df_d.drop(columns='参加', inplace=True)

st.write(df_d)

df_org = pd.read_csv('master.csv', encoding = 'UTF-8-sig')

df_add = pd.concat([df_org, df_d], axis=0)

if st.button('データベース更新'):
    df_add.to_csv('master.csv', encoding = 'UTF-8-sig',index=False)
