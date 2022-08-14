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

st.set_page_config(page_title='Revenue Model',  layout='wide', page_icon='https://noctrixhealth.com/wp-content/uploads/2021/05/cropped-SiteIcon-32x32.jpg')


st.markdown("""
            
            |   Revenue2    |         WebApp             |
| :------------------------------------------------------ | -----------: |
|  <img src="https://noctrixhealth.com/wp-content/uploads/2021/05/cropped-SiteIcon-270x270.jpg" alt="logo" width=150/>   | *Parameters set in side bar*    |
| *For internal use only*   | Jatin Tekchandani        |



""", unsafe_allow_html=True)

def form_callback():
    print("==Pricing Assumptions==")
    print(Total_TOMA_CMS,Private_TOMA, Blended_TOMA)
    print(Total_TOMA_PP )
    print(Total_CCG,Private_CCG,Blended_CCG)
    print(Total_CDI,Private_CDI,Blended_CDI)


    # Print to compare calculations in Excel
    print("==Pricing Assumptions==")
    print(Total_TOMA_CMS,Private_TOMA, Blended_TOMA)
    print(Total_TOMA_PP )
    print(Total_CCG,Private_CCG,Blended_CCG)
    print(Total_CDI,Private_CDI,Blended_CDI)

# https://noctrixhealth.com/wp-content/uploads/2020/08/noctrix_logo_white.png white logo
    
with st.sidebar.form(key='my_form'):
    st.markdown("""<div style="text-align: center;">
                <img src="https://noctrixhealth.com/wp-content/uploads/2020/10/NoctrixLogo@2x.png" alt="logo" width=200/></div>

    """, unsafe_allow_html=True)
    st.subheader('Model Parameters')


    Initial_Number_Of_Clinics                       =     st.slider("Initial Number Of Clinics [#]",
                                                            min_value = 0,
                                                            max_value = 10,
                                                            value = 2)

    Number_Of_New_Clinics_Monthly_Growth            =     st.slider("Number Of New Clinics Monthly Growth [%]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 10)*.01
           
    Patients_Per_Clinic_Per_Month                   =     st.slider("Patients Per Clinic Per Month [#]",
                                                            min_value = 0,
                                                            max_value = 20,
                                                            value = 4)
                              
    New_Patients_In_Existing_Clinic_Annual_Growth   =     st.slider("New Patients In Existing Clinic Annual Growth [%]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 10)*.01
    
    Patient_Attrition_Rate_Per_Month                =     st.slider("Patient Attrition Rate Per Month [%]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 20)*.01
    
    Percent_Patients_On_Medicare                    =     st.slider("Percent Patients On Medicare [%]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 40)*.01
    
    Private_Payer_Premium_Over_Medicare             =     st.slider("Private Payer Premium Over Medicare [%]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 40)*.01
    
    #Number per kit
    Number_Per_Kit_TOMA_CMS                         =     st.slider("Number Per Kit: TOMA when Medicare [#]",
                                                            min_value = 0,
                                                            max_value = 4,
                                                            value = 2)
    
    Number_Per_Kit_TOMA_PP                         =     st.slider("Number Per Kit: TOMA when Private Payer [#]",
                                                            min_value = 0,
                                                            max_value = 4,
                                                            value = 2)
    
    Number_Per_Kit_CCG                             =     st.slider("Number Per Kit: CCG [#]",
                                                            min_value = 0,
                                                            max_value = 4,
                                                            value = 2)
    
    Number_Per_Kit_CDI                             =     st.slider("Number Per Kit: CDI [#]",
                                                            min_value = 0,
                                                            max_value = 8,
                                                            value = 4)
    
    # Rental period / Refill frequency (months)
    Rental_Period_Refill_TOMA_CMS                 =     st.slider("Rental Period for TOMA when Medicare [months]",
                                                            min_value = 0,
                                                            max_value = 24,
                                                            value = 13)
    
    Rental_Period_Refill_TOMA_PP                  =     st.slider("Rental Period for TOMA when Private [months]",
                                                            min_value = 0,
                                                            max_value = 24,
                                                            value = 6)
    Rental_Period_Refill_CCG                      =     st.slider("Refill Period for CCG [months]",
                                                            min_value = 0,
                                                            max_value = 12,
                                                            value = 3)       
    Rental_Period_Refill_CDI                      =     st.slider("Refill Period for CCG [months]",
                                                            min_value = 0,
                                                            max_value = 12,
                                                            value = 1) 
    
    #Total CMS Reimbursement per unit
    CMS_TOMA_CMS                                 =     st.slider("Reimbursement per unit TOMA when Medicare [$]",
                                                            min_value = 0,
                                                            max_value = 5000,
                                                            value = 450)
    
    CMS_TOMA_PP                                  =     st.slider("Reimbursement per unit TOMA when Private Payer [$]",
                                                            min_value = 0,
                                                            max_value = 5000,
                                                            value = 630)
    CMS_CCG                                      =     st.slider("Reimbursement per unit CCG [$]",
                                                            min_value = 0,
                                                            max_value = 500,
                                                            value = 250)
    CMS_CDI                                       =     st.slider("Reimbursement per unit CDI [$]",
                                                            min_value = 0,
                                                            max_value = 100,
                                                            value = 14)

    submit_button = st.form_submit_button(label='Calculate!', on_click=form_callback)
    st.write("Please contact if ranges need to be adjusted")
    
#%% Calculations

# Calculated fields
#-------------------------------
#Total CMS Reimbursement
Total_TOMA_CMS            = CMS_TOMA_CMS * Number_Per_Kit_TOMA_CMS
Total_TOMA_PP             =  CMS_TOMA_PP * Number_Per_Kit_TOMA_PP
Total_CCG                 =      CMS_CCG * Number_Per_Kit_CCG
Total_CDI                 =      CMS_CDI * Number_Per_Kit_CDI

#-------------------------------
#Private Payer
Private_TOMA                = Total_TOMA_CMS * (1+ Private_Payer_Premium_Over_Medicare) 
# no Private and blended for CMS_TOMA_PP row.  This was included for rental periods
Private_CCG                 =      Total_CCG * (1+ Private_Payer_Premium_Over_Medicare)
Private_CDI                 =      Total_CDI * (1+ Private_Payer_Premium_Over_Medicare)

#-------------------------------
#Blended Reimbursement
Percent_Private = 1 - Percent_Patients_On_Medicare

Blended_TOMA                =  (Percent_Patients_On_Medicare * Total_TOMA_CMS) + (Percent_Private * Private_TOMA)
# no Private and blended for CMS_TOMA_PP row.  This was included for rental periods
Blended_CCG                 =  (Percent_Patients_On_Medicare * Total_CCG) + (Percent_Private * Private_CCG)
Blended_CDI                 =  (Percent_Patients_On_Medicare * Total_CDI) + (Percent_Private * Private_CDI)


Month = np.arange(37)
New_Clinics = np.zeros(37)
Total_prescribing_clinics = np.zeros(37)
New_patients_by_month = np.zeros(37)


# Month one inital condition
New_Clinics[1] = Initial_Number_Of_Clinics
Total_prescribing_clinics[1] = Initial_Number_Of_Clinics
New_patients_by_month[1] = Initial_Number_Of_Clinics * Patients_Per_Clinic_Per_Month

# one time calculation for monthly growth factor

Monthly_Growth = (1 + New_Patients_In_Existing_Clinic_Annual_Growth / 12)

# Loop for remaining months
for i in range(2,37):
  pre = i-1   # previous month
  New_Clinics[i]               = np.ceil(Total_prescribing_clinics[pre] * Number_Of_New_Clinics_Monthly_Growth)
  Total_prescribing_clinics[i] = Total_prescribing_clinics[pre] + New_Clinics[i] 
  New_patients_by_month[i]     = np.ceil(Total_prescribing_clinics[pre] * (Monthly_Growth ** Month[pre]) * Patients_Per_Clinic_Per_Month + New_Clinics[i] * Patients_Per_Clinic_Per_Month)
  

One_patient_amortization = np.zeros((37,37))
One_patient_amortization[1] =  New_patients_by_month
Attrition_Rate = 1 - Patient_Attrition_Rate_Per_Month

for row in range(2,37):
  for col in range(row,37):
    One_patient_amortization[row][col] = np.ceil(One_patient_amortization[row-1][col-1] * Attrition_Rate)



Total_patients = One_patient_amortization.sum(axis=0)

TOMA_CMS                   = np.zeros(37)
TOMA_PP                    = np.zeros(37)
CCG                        = np.zeros(37)  
CDI                        = np.zeros(37)

# For TOMA, check if within rental period before calculating
for month in Month:
  if month <= Rental_Period_Refill_TOMA_CMS:
    TOMA_CMS[month] = (Number_Per_Kit_TOMA_CMS * CMS_TOMA_CMS) / Rental_Period_Refill_TOMA_CMS

  if month <= Rental_Period_Refill_TOMA_PP:
    TOMA_PP[month] = (Number_Per_Kit_TOMA_PP * CMS_TOMA_PP)  / Rental_Period_Refill_TOMA_PP 

# cast to all values the same result for CCG and CDI
CCG[:] = Blended_CCG / Rental_Period_Refill_CCG
CDI[:] = Blended_CDI / Rental_Period_Refill_CDI

Total = (TOMA_CMS * Percent_Patients_On_Medicare) + (TOMA_PP * Percent_Private) + CCG + CDI

Devices = (TOMA_CMS * Percent_Patients_On_Medicare) + (TOMA_PP * Percent_Private)

Monthly_Revenue = np.dot(Total[1:], np.delete(One_patient_amortization, 0, 0))
Revenue_New_Patients = Total[1] * One_patient_amortization[1]
Revenue_Existing_Patients = Monthly_Revenue - Revenue_New_Patients
Revenue_Devices = np.dot(Devices, One_patient_amortization)
Revenue_Consumables = Monthly_Revenue - Revenue_Devices
Device_Percentage = Revenue_Devices / Monthly_Revenue
Consumables_Percentage = 1 - Device_Percentage

df = pd.DataFrame({
    'Month':Month,
    'New_Clinics':New_Clinics,
    'Total_prescribing_clinics':Total_prescribing_clinics,
    'New_patients_by_month':New_patients_by_month,
    'Total_patients':Total_patients,
    'Monthly_Revenue': Monthly_Revenue,
    'Revenue_New_Patients':Revenue_New_Patients,
    'Revenue_Existing_Patients':Revenue_Existing_Patients,
    'Revenue_Devices':Revenue_Devices,
    'Revenue_Consumables':Revenue_Consumables,
    'Device_Percentage':Device_Percentage,
    'Consumables_Percentage':Consumables_Percentage})

st.write("")
st.write("")



#%%

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

import numpy as np




fig = px.bar(
    data_frame = df,
    x = "Month",
    y = ["Monthly_Revenue"], #,"Revenue_Devices"],
    opacity = 0.5,
    color_discrete_sequence=['deepskyblue'],  #MediumSlateBlue
    orientation = "v",
    barmode = 'group',
    title='Monthly Revenue',
)


st.plotly_chart(fig, use_container_width=True)



fig = px.bar(
    data_frame = df,
    x = "Month",
    y = ["Revenue_New_Patients","Revenue_Existing_Patients"],
    opacity = 0.5,
    color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
    orientation = "v",
    barmode = 'group',
    title='Existing vs New Patient Revenue',
    labels={'x': 'Year', 'value':'Dollars USD'},
)


st.plotly_chart(fig, use_container_width=True)


fig = px.bar(
    data_frame = df,
    x = "Month",
    y = ["Revenue_Devices","Revenue_Consumables"],
    opacity = 0.5,
    color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
    orientation = "v",
    barmode = 'group',
    title='Devices vs Consumables Revenue',
    labels={'x': 'Year', 'value':'Dollars USD'},
)


st.plotly_chart(fig, use_container_width=True)
#%%

with st.expander("Calculations"):
    df.T
    
with st.expander("Amortization Matrix"):
    One_patient_amortization

#DataTable(pd.DataFrame(One_patient_amortization))



#st.bar_chart(chart_data)

'''

[theme]
base="light"
primaryColor="#8a76bd"
textColor="#584784"

[theme]
base="light"
primaryColor="#8a76bd"
secondaryBackgroundColor="#edf6fb"
textColor="#584784"

'''


