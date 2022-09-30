#%% Revenue Estimation App


#imports
import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
from fpdf import FPDF
import matplotlib.pyplot as plt 

#testing
import random


# set the page icon and title
# may not be useful in the iframe
st.set_page_config(page_title='Revenue Model',  layout='wide', page_icon='https://noctrixhealth.com/wp-content/uploads/2021/05/cropped-SiteIcon-32x32.jpg')


# remove the orange/red line on top
# also hides the hamburger menu
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        footer {visibility: hidden;} 
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)




## Global variables for Model



Set_Initial_Number_Of_Clinics                       = 2
Set_Number_Of_New_Clinics_Monthly_Growth            = 10
Set_Patients_Per_Clinic_Per_Month                   = 4
Set_New_Patients_In_Existing_Clinic_Annual_Growth   = 10
Set_Patient_Attrition_Rate_Per_Month                = 20
Set_Percent_Patients_On_Medicare                    = 40
Set_Rental_Period_Refill_TOMA_CMS                   = 13
Set_Rental_Period_Refill_TOMA_PP                    = 6
Set_Rental_Period_Refill_CCG                        = 3
Set_Rental_Period_Refill_CDI                        = 1
Set_CMS_TOMA_CMS                                    = 450
Set_CMS_CCG                                         = 250
Set_CMS_CDI                                         = 14
Set_Private_Payer_Premium_Over_Medicare             = 40


def form_callback():
    print("==Pricing Assumptions==")
    
import streamlit as st



#testing







col1, col2, col3 = st.columns(3)

with col1:
    choice = st.radio(
     "Choose Preset",
     ('Optimistic', 'Conservative', 'Realistic'), index=2)

with col2:
    Quarterly = st.checkbox("Plot Quarterly")

if choice == "Conservative":
    Set_Initial_Number_Of_Clinics                       = 1
    Set_Number_Of_New_Clinics_Monthly_Growth            = 5
    Set_Patients_Per_Clinic_Per_Month                   = 2
    Set_New_Patients_In_Existing_Clinic_Annual_Growth   = 5
    Set_Patient_Attrition_Rate_Per_Month                = 15
    Set_Percent_Patients_On_Medicare                    = 60
    Set_Rental_Period_Refill_TOMA_CMS                   = 13
    Set_Rental_Period_Refill_TOMA_PP                    = 9
    Set_Rental_Period_Refill_CCG                        = 3
    Set_Rental_Period_Refill_CDI                        = 3
    Set_CMS_TOMA_CMS                                    = 300
    Set_CMS_CCG                                         = 150
    Set_CMS_CDI                                         = 21
    Set_Private_Payer_Premium_Over_Medicare             = 15


if choice == "Realistic":
    Set_Initial_Number_Of_Clinics                       = 2
    Set_Number_Of_New_Clinics_Monthly_Growth            = 10
    Set_Patients_Per_Clinic_Per_Month                   = 4
    Set_New_Patients_In_Existing_Clinic_Annual_Growth   = 10
    Set_Patient_Attrition_Rate_Per_Month                = 10
    Set_Percent_Patients_On_Medicare                    = 40
    Set_Rental_Period_Refill_TOMA_CMS                   = 13
    Set_Rental_Period_Refill_TOMA_PP                    = 6
    Set_Rental_Period_Refill_CCG                        = 3
    Set_Rental_Period_Refill_CDI                        = 3
    Set_CMS_TOMA_CMS                                    = 450
    Set_CMS_CCG                                         = 250
    Set_CMS_CDI                                         = 42
    Set_Private_Payer_Premium_Over_Medicare             = 40
    
    
if choice == "Optimistic":
    Set_Initial_Number_Of_Clinics                       = 4
    Set_Number_Of_New_Clinics_Monthly_Growth            = 20
    Set_Patients_Per_Clinic_Per_Month                   = 6
    Set_New_Patients_In_Existing_Clinic_Annual_Growth   = 15
    Set_Patient_Attrition_Rate_Per_Month                = 5
    Set_Percent_Patients_On_Medicare                    = 30
    Set_Rental_Period_Refill_TOMA_CMS                   = 13
    Set_Rental_Period_Refill_TOMA_PP                    = 4
    Set_Rental_Period_Refill_CCG                        = 3
    Set_Rental_Period_Refill_CDI                        = 3
    Set_CMS_TOMA_CMS                                    = 750
    Set_CMS_CCG                                         = 375
    Set_CMS_CDI                                         = 90
    Set_Private_Payer_Premium_Over_Medicare             = 50
    

    

    
with st.sidebar.form(key='my_form'):
    # logo in sidebar
    #st.markdown("<div style="text-align: center;">
    #            <img src="https://noctrixhealth.com/wp-content/uploads/2020/10/NoctrixLogo@2x.png" alt="logo" width=200/></div>

    #""", unsafe_allow_html=True)
    

    
    st.subheader('Model Parameters')
    #top_submit_button = st.form_submit_button(label='🖩 Calculate', on_click=form_callback)

    

    

    with st.expander("🏥 Number of Clinic Parameters"):
        Initial_Number_Of_Clinics                       =     st.slider("Initial Number Of Clinics [#]",
                                                                min_value = 0,
                                                                max_value = 5,
                                                                value = Set_Initial_Number_Of_Clinics)
    
        Number_Of_New_Clinics_Monthly_Growth            =     st.slider("Number Of New Clinics Monthly Growth",
                                                                min_value = 0,
                                                                max_value = 40,
                                                                value = Set_Number_Of_New_Clinics_Monthly_Growth,
                                                                format="%i%%")*.01
               
        Patients_Per_Clinic_Per_Month                   =     st.slider("Patients Per Clinic Per Month [#]",
                                                                min_value = 0,
                                                                max_value = 10,
                                                                value = Set_Patients_Per_Clinic_Per_Month)
        
        
        
    with st.expander("👤Number of Patients Parameters"):                             
        New_Patients_In_Existing_Clinic_Annual_Growth   =     st.slider("New Patients In Existing Clinic Annual Growth",
                                                                min_value = 0,
                                                                max_value = 25,
                                                                value = Set_New_Patients_In_Existing_Clinic_Annual_Growth,
                                                                format="%i%%")*.01
        
        Patient_Attrition_Rate_Per_Month                =     st.slider("Patient Attrition Rate Per Month",
                                                                min_value = 0,
                                                                max_value = 25,
                                                                value = Set_Patient_Attrition_Rate_Per_Month,
                                                                format="%i%%")*.01
        
        
        Percent_Patients_On_Medicare                    =     st.slider("Percent Patients On Medicare",
                                                                min_value = 0,
                                                                max_value = 100,
                                                                value = Set_Percent_Patients_On_Medicare,
                                                                format="%i%%")*.01
    

    
    #Number per kit
    Number_Per_Kit_TOMA_CMS                        =     2
    
    
    Number_Per_Kit_TOMA_PP                         =     2
    
    Number_Per_Kit_CCG                             =     2
    
    Number_Per_Kit_CDI                             =     4
    
    
    
    # Rental period / Refill frequency (months)
    with st.expander("📅 Rental / Refill Period"):
        Rental_Period_Refill_TOMA_CMS                 =     st.slider("Rental Period for TOMA when Medicare [months]",
                                                                min_value = 0,
                                                                max_value = 24,
                                                                value = Set_Rental_Period_Refill_TOMA_CMS, disabled=True)
                                                          
        
        Rental_Period_Refill_TOMA_PP                  =     st.slider("Rental Period for TOMA when Private [months]",
                                                                min_value = 0,
                                                                max_value = 13,
                                                                value = Set_Rental_Period_Refill_TOMA_PP)
        
        Rental_Period_Refill_CCG                      =     st.slider("Refill Period for CCG [months]",
                                                                min_value = 0,
                                                                max_value = 12,
                                                                value = Set_Rental_Period_Refill_CCG, disabled=True)       
        
        Rental_Period_Refill_CDI                      =     st.slider("Refill Period for CDI [months]",
                                                                min_value = 0,
                                                                max_value = 12,
                                                                value = Set_Rental_Period_Refill_CDI, disabled=True) 
        
        
    with st.expander("💵 Reimbursement per unit"):    
    #Total CMS Reimbursement per unit
        CMS_TOMA_CMS                                 =     st.slider("Reimbursement per unit hf-TOMAC when Medicare",
                                                                min_value = 200,
                                                                max_value = 5000,
                                                                value = Set_CMS_TOMA_CMS,
                                                                format="$%i")
        
        CMS_CCG                                      =     st.slider("Reimbursement per unit CCG",
                                                                min_value = 0,
                                                                max_value = 500,
                                                                value = Set_CMS_CCG,
                                                                format="$%i")
        
        CMS_CDI                                       =     st.slider("Reimbursement per unit CDI",
                                                                min_value = 15,
                                                                max_value = 150,
                                                                value = Set_CMS_CDI,
                                                                format="$%i")
        
        Private_Payer_Premium_Over_Medicare             =     st.slider("Private Payer Premium Over Medicare",
                                                                min_value = 0,
                                                                max_value = 100,
                                                                value = Set_Private_Payer_Premium_Over_Medicare,
                                                                format="%i%%")*.01
    
    
    submit_button = st.form_submit_button(label='🖩 Calculate', on_click=form_callback)

    
#%% Calculations



# Calculated fields
#-------------------------------

CMS_TOMA_PP               = CMS_TOMA_CMS * (1+ Private_Payer_Premium_Over_Medicare) 

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



numMonths = 61 # add one to the actual number you want


Month = np.arange(numMonths)
New_Clinics = np.zeros(numMonths)
Total_prescribing_clinics = np.zeros(numMonths)
New_patients_by_month = np.zeros(numMonths)


# Month one inital condition
New_Clinics[1] = Initial_Number_Of_Clinics
Total_prescribing_clinics[1] = Initial_Number_Of_Clinics
New_patients_by_month[1] = Initial_Number_Of_Clinics * Patients_Per_Clinic_Per_Month

# one time calculation for monthly growth factor

Monthly_Growth = (1 + New_Patients_In_Existing_Clinic_Annual_Growth / 12)

# Loop for remaining months
for i in range(2,numMonths):
  pre = i-1   # previous month
  New_Clinics[i]               = np.ceil(Total_prescribing_clinics[pre] * Number_Of_New_Clinics_Monthly_Growth)
  Total_prescribing_clinics[i] = Total_prescribing_clinics[pre] + New_Clinics[i] 
  New_patients_by_month[i]     = np.ceil(Total_prescribing_clinics[pre] * (Monthly_Growth ** Month[pre]) * Patients_Per_Clinic_Per_Month + New_Clinics[i] * Patients_Per_Clinic_Per_Month)
  

One_patient_amortization = np.zeros((numMonths,numMonths))
One_patient_amortization[1] =  New_patients_by_month
Attrition_Rate = 1 - Patient_Attrition_Rate_Per_Month

for row in range(2,numMonths):
  for col in range(row,numMonths):
    One_patient_amortization[row][col] = np.ceil(One_patient_amortization[row-1][col-1] * Attrition_Rate)



Total_patients = One_patient_amortization.sum(axis=0)

TOMA_CMS                   = np.zeros(numMonths)
TOMA_PP                    = np.zeros(numMonths)
CCG                        = np.zeros(numMonths)  
CDI                        = np.zeros(numMonths)

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

Quarter = np.ceil(Month /3)

df = pd.DataFrame({
    'Month':Month,
    'Quarter':Quarter,
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

qdf    = df.groupby('Quarter').sum()
qdfMax = df.groupby('Quarter').max()  # for patient count

qdf['Quarter'] = qdf.index
qdfMax['Quarter'] = qdfMax.index
        

qdf['Revenue'] = qdf['Monthly_Revenue']

if not Quarterly:
    fig = px.bar(
        data_frame = df,
        x = "Month",
        y = ["Monthly_Revenue"], #,"Revenue_Devices"],
        opacity = 0.5,
        color_discrete_sequence=['MediumSlateBlue'],  
        orientation = "v",
        barmode = 'group',
        title='Monthly Revenue',
        labels={'x': 'Month', 'value':'Dollars USD'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

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
        labels={'x': 'Month', 'value':'Dollars USD'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

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
        labels={'x': 'Month', 'value':'Dollars USD'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        data_frame = df,
        x = "Month",
        y = ["Device_Percentage","Consumables_Percentage"],
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        title='Devices vs Consumables Revenue',
        labels={'x': 'Month', 'value':'% of revenue'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        data_frame = df,
        x = "Month",
        y = ["New_Clinics","Total_prescribing_clinics"],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Number of Clinics',
        labels={'x': 'Month', 'value':'Number of Clinics'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        data_frame = df,
        x = "Month",
        y = ['New_patients_by_month','Total_patients'],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Number of Patients',
        labels={'x': 'Month', 'value':'Number of Patients'},
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))

    st.plotly_chart(fig, use_container_width=True)
    
# display Quaterly plots

if Quarterly:
    fig = px.bar(
        data_frame = qdf,
        x = "Quarter",
        y = ["Revenue"], #,"Revenue_Devices"],
        opacity = 0.5,
        color_discrete_sequence=['MediumSlateBlue'],  
        orientation = "v",
        barmode = 'group',
        title='Quarterly Revenue',
        labels={'x': 'Quarter', 'value':'Dollars USD'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    fig = px.bar(
        data_frame = qdf,
        x = "Quarter",
        y = ["Revenue_New_Patients","Revenue_Existing_Patients"],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Existing vs New Patient Revenue',
        labels={'x': 'Quarter', 'value':'Dollars USD'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    
    fig = px.bar(
        data_frame = qdf,
        x = "Quarter",
        y = ["Revenue_Devices","Revenue_Consumables"],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Devices vs Consumables Revenue',
        labels={'x': 'Quarter', 'value':'Dollars USD'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.line(
        data_frame = qdf,
        x = "Quarter",
        y = ["Device_Percentage","Consumables_Percentage"],
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        title='Devices vs Consumables Revenue',
        labels={'x': 'Quarter', 'value':'% of revenue'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(
        data_frame = qdf,
        x = "Quarter",
        y = ["New_Clinics","Total_prescribing_clinics"],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Number of Clinics',
        labels={'x': 'Quarter', 'value':'Number of Clinics'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    st.plotly_chart(fig, use_container_width=True)
    
    fig = px.bar(
        data_frame = qdfMax,
        x = "Quarter",
        y = ['New_patients_by_month','Total_patients'],
        opacity = 0.5,
        color_discrete_sequence=['deepskyblue','MediumSlateBlue'],
        orientation = "v",
        barmode = 'group',
        title='Number of Patients',
        labels={'x': 'Quarter', 'value':'Number of Patients'},
    )
    
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ))
    
    
    st.plotly_chart(fig, use_container_width=True)

#%%

with st.expander("Calculations"):
    st.write('Monthly')
    #df2 = df.T.style.format("{:.2}")
    df.T
    st.write('Quarterly')
    #qdf2 = qdf.T.style.format("{:.2}")
    qdf.T
    
with st.expander("Amortization Matrix"):
    One_patient_amortization
    

with col3:
     PDFgen = st.button(f"⚙️ Generate PDF")
     if PDFgen:
        with st.spinner('Generating PDF...'):
            pdf = FPDF(orientation="P", unit="mm", format="Letter")
            pdf.add_page()
            pdf.set_font("helvetica", "B", 16)
            pdf.image("Logo.png",x=10,y=10,w=40)

            pdf.cell(190, 40, "Revenue Estimation Report", ln=1, align='C')

            pdf.cell(40,5,"Input Parameters to Model",ln=1)

            pdf.set_font("helvetica", "", 14)

            pdf.ln(1)

            rh = 7 # row height

            pdf.cell(150,rh,"Initial Number Of Clinics",border=1)
            pdf.cell(40,rh,str(Initial_Number_Of_Clinics),border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Number Of New Clinics Monthly Growth",border=1)
            pdf.cell(40,rh,str(Number_Of_New_Clinics_Monthly_Growth*100)+'%',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Patients Per Clinic Per Month",border=1)
            pdf.cell(40,rh,str(Patients_Per_Clinic_Per_Month),border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"New Patients In Existing Clinic Annual Growth",border=1)
            pdf.cell(40,rh,str(New_Patients_In_Existing_Clinic_Annual_Growth*100)+'%',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Patient Attrition Rate Per Month",border=1)
            pdf.cell(40,rh,str(Patient_Attrition_Rate_Per_Month*100)+'%',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Percent Patients On Medicare",border=1)
            pdf.cell(40,rh,str(Percent_Patients_On_Medicare*100)+'%',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Rental Period Refill TOMA CMS",border=1)
            pdf.cell(40,rh,str(Rental_Period_Refill_TOMA_CMS)+' months',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Rental Period Refill TOMA PP",border=1)
            pdf.cell(40,rh,str(Rental_Period_Refill_TOMA_PP)+' months',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Rental Period Refill CCG",border=1)
            pdf.cell(40,rh,str(Rental_Period_Refill_CCG)+' months',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Rental Period Refill CDI ",border=1)
            pdf.cell(40,rh,str(Rental_Period_Refill_CDI)+' months',border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"CMS TOMA CMS ",border=1)
            pdf.cell(40,rh,'$'+str(CMS_TOMA_CMS),border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"CMS CCG",border=1)
            pdf.cell(40,rh,'$'+str(CMS_CCG),border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"CMS CDI",border=1)
            pdf.cell(40,rh,'$'+str(CMS_CDI),border=1)
            pdf.ln(rh)
            pdf.cell(150,rh,"Private Payer Premium Over Medicare",border=1)
            pdf.cell(40,rh,str(Private_Payer_Premium_Over_Medicare*100)+'%',border=1)
            pdf.ln(rh)


            #  next page begins plots

            pdf.add_page()


            X = qdf['Quarter'].astype(int)
            Y = qdf['Monthly_Revenue']

            X_axis = np.arange(len(X))

            plt.figure(dpi=250)  
            plt.bar(X_axis - 0.2, Y, 0.4, label = 'Revenue',color='MediumSlateBlue', alpha=0.7)

              
            plt.xticks(X_axis, X)
            plt.xlabel("Quarter")
            plt.ylabel("Dollars USD")
            plt.title("Revenue")
            plt.legend()
            plt.savefig('plot.png')
            pdf.image("plot.png",x=10,y=10,w=180)



            Y = qdf['Revenue_New_Patients']
            Z = qdf['Revenue_Existing_Patients']



            plt.figure(dpi=250)    
            plt.bar(X_axis - 0.2, Y, 0.4, label = 'Revenue New Patients',color='deepskyblue', alpha=0.7)
            plt.bar(X_axis + 0.2, Z, 0.4, label = 'Revenue Existing Patients',color='MediumSlateBlue', alpha=0.7)
              
            plt.xticks(X_axis, X)
            plt.xlabel("Quarter")
            plt.ylabel("Dollars USD")
            plt.title("Revenue From New vs Existing Patients")
            plt.legend()
            plt.savefig('plot2.png')
            pdf.image("plot2.png",x=10,y=140,w=180)



            # next page   =============

            pdf.add_page()

            Y = qdf['New_Clinics']
            Z = qdf['Total_prescribing_clinics']

            plt.figure(dpi=250)    
            plt.bar(X_axis - 0.2, Y, 0.4, label = 'New Clinics',color='deepskyblue', alpha=0.7)
            plt.bar(X_axis + 0.2, Z, 0.4, label = 'Total prescribing clinics',color='MediumSlateBlue', alpha=0.7)
              
            plt.xticks(X_axis, X)
            plt.xlabel("Quarter")
            plt.ylabel("Clinics")
            plt.title("New vs Total Prescibing Clinics")
            plt.legend()
            plt.savefig('plot3.png')
            pdf.image("plot3.png",x=10,y=10,w=180)



            Y = qdfMax['New_patients_by_month']
            Z = qdfMax['Total_patients']



            plt.figure(dpi=250)    
            plt.bar(X_axis - 0.2, Y, 0.4, label = 'New patients by month',color='deepskyblue', alpha=0.7)
            plt.bar(X_axis + 0.2, Z, 0.4, label = 'Total patients',color='MediumSlateBlue', alpha=0.7)
              
            plt.xticks(X_axis, X)
            plt.xlabel("Quarter")
            plt.ylabel("Patients")
            plt.title("New Patient vs Total Patients")
            plt.legend()
            plt.savefig('plot4.png')
            pdf.image("plot4.png",x=10,y=140,w=180)
            pdf.output("Report1.pdf")

            with open("Report1.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
                
        st.success('📃 PDF Created!') 
        
        st.download_button(
            "⬇️ Download PDF",
            data=PDFbyte,
            file_name="Revenue Estimation.pdf",
            mime="application/octet-stream",
        )