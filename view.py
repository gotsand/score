#streamlit run view.py

import streamlit as st
import pandas as pd
import datetime
import numpy as np
import pickle

st.set_page_config(page_title="得点表", layout="wide")
pd.options.display.float_format = '{:.1f}'.format
dt_now = datetime.datetime.now()
date = str(dt_now.strftime('%m/%d'))
month = int(dt_now.strftime('%m'))

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
    mm = date[0:x+1]
    l_mm.append(mm)

l_vmm = ['3月', '2月', '1月']
#l_vmm = ['12月', '11月', '10月', '9月']

target = st.selectbox(label="表示月選択", options=l_vmm)

y = target.find('月')
mo = target[0:y]

pri = (int(mo)-1) %3 + 1
l_pri = [pri, pri + 3, pri + 6]
 
prize =   '入賞順位：' + str(pri) + '位，' + str(pri + 3) + '位，' + str(pri + 6) + '位'
st.write(prize)

df_all['月'] = l_mm
df_all['日付'] = l_dd

st.write('0' + mo)

if len(mo) ==1:
    df2 = df_all[df_all['月'] == '0' + mo]
else:
    df2 = df_all[df_all['月'] == mo]

st.dataframe(df_all.dtypes)    
st.dataframe(df2)
