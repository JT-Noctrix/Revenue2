# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 17:55:57 2022

@author: JtekG
"""

import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title='Revenue Model',  layout='wide')


st.markdown("""
            
            |   Revenue Model    |         Adjust parameters for model              |
| :------------------------------------------------------ | -----------: |
|  <img src="https://noctrixhealth.com/wp-content/uploads/2020/10/NoctrixLogo@2x.png" alt="logo" width=300/>   | **Select from available patients and display analysis**    |
| *For internal use only*   | Jatin Tekchandani        |


* In your **MyDrive, create a GalenLogin.txt** file with your login email as the first line and your password as the second line
""", unsafe_allow_html=True)

def form_callback():
    sum = st.session_state.x1 + st.session_state.x2 + st.session_state.x3 + st.session_state.x4
    st.session_state.x1 = st.session_state.x1/sum*100.0
    st.session_state.x2 = st.session_state.x2/sum*100.0
    st.session_state.x3 = st.session_state.x3/sum*100.0
    st.session_state.x4 = st.session_state.x4/sum*100.0

with st.sidebar.form(key='my_form'):
    st.subheader('Glass composition')

    st.slider("SiO\u2082 concentration, mol%",
                    min_value = 50.0,
                    max_value = 100.0,
                    key='x1')

    st.slider("Al\u2082O\u2083 concentration, mol%",
                    min_value = 0.0,
                    max_value = 50.0,
                    key='x2')

    st.slider("Na\u2082O concentration, mol%",
                    min_value = 0.0,
                    max_value = 50.0,
                    key='x3')

    st.slider("K\u2082O concentration, mol%",
                    min_value = 0.0,
                    max_value = 50.0,
                    key='x4')

    submit_button = st.form_submit_button(label='Calculate!', on_click=form_callback)
    st.write("When you run the model, compositions will be rescaled to ensure they sum to 100%.")
composition =  np.array([st.session_state.x1/100, st.session_state.x2/100, st.session_state.x3/100, st.session_state.x4/100]).reshape(1,-1)

