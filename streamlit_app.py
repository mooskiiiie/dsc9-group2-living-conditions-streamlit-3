import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import warnings
import json
warnings.filterwarnings('ignore')

#!pip install

df = pd.read_csv("data/PH-HRIR-merged-sampled.csv")

with open('data/PHHR71FL-data-dictionary.json', 'r') as file:
    hr_col_dict = json.load(file)
    
with open('data/PHIR71FL-data-dictionary.json', 'r') as file:
    ir_col_dict = json.load(file)

df['HV204'].replace(to_replace=['On premises', "Don't know"], value=[0, 0], inplace = True)
df['SH202'] = df['SH202'].fillna(0)
df['SH207'] = df['SH207'].fillna(0)

my_page = st.sidebar.radio('Page Navigation', ['Introduction', 'Water Source', 'Healthcare Access', 'Electricity', 'Sanitation'])

if my_page == 'Introduction':
    st.title("Pamumuhay:")
    st.header("An Analysis on the Living Conditions of the Filipino People")
    st.subheader("Problem Statement")
    st.markdown("How might we mitigate possible issues in the living conditions of the Filipino people?")
    st.markdown(" ")
    st.subheader("Objective")
    st.markdown("To build a profile of Filipino households on how their physical living conditions affect their health")    

elif my_page == 'Water Source':
    st.header("Water Source")
    
    df['HV204'] = df['HV204'].astype(float)
    
    interest1 = df[['HV025','HV204', 'HV201','HV202','SH202','SH207']]
   
    drink = interest1.groupby('HV201').size().nlargest().sort_values(ascending = False)
    
    # indicates if plotting on the figues or on subplots
    plt.figure(figsize=(8,6)) 

    # the main code to create the graph
    plt.barh(drink.index, drink.values) 

    # additional elements that can be customzed
    plt.title("Source of Drinking Water", fontsize=16)
    plt.ylabel("Frequency", fontsize=12)
    plt.xlabel("Source", fontsize=12)
    plt.xticks(rotation=60)

    # display graph
    st.pyplot(plt)
    
    #second graph
    non_drink = interest1.groupby('HV202').size().sort_values(ascending = True).nlargest()

    plt.figure(figsize=(8,6)) 

    # the main code to create the graph
    plt.barh(non_drink.index, non_drink.values) 

    # additional elements that can be customzed
    plt.title("Source of Non-Drinking Water", fontsize=16)
    plt.ylabel("Frequency", fontsize=12)
    plt.xlabel("Source", fontsize=12)
    plt.xticks(rotation=60)

    # display graph
    st.pyplot(plt)
    
elif my_page == 'Healthcare Access':
    st.header("Healthcare Access")
    
    sickp = (df.groupby("HV024")['SH207'].sum()/df.groupby("HV024")['SH202'].sum()).sort_values(ascending = True)

    # indicates if plotting on the figues or on subplots
    plt.figure(figsize=(8,6)) 

    # the main code to create the graph
    plt.barh(sickp.index, sickp.values) 

    # additional elements that can be customzed
    plt.title("Percent of Sick / Injured People Who Visited Medical Facility", fontsize=16)
    plt.ylabel("Region", fontsize=12)
    plt.xlabel("Percentage", fontsize=12)
    plt.xticks(rotation=0)

    # display graph
    st.pyplot(plt)
    
elif my_page == 'Electricity':
    st.header("Electricity")
    
    elec = df.groupby('HV206').size()
    
    plt.figure(figsize=(6,6))

    plt.pie(elec, labels = elec.index, autopct='%1.1f%%', startangle=90)
    plt.title("Respondents Access to Electricity", fontsize=14)

    st.pyplot(plt)
    
elif my_page == 'Sanitation':
    st.header("Sanitation")
    toilet = df.groupby('HV205').size().sort_values()
    plt.xlabel('Number of Respondents')
    plt.barh(toilet.index, toilet.values)
    st.pyplot(plt)