#!/usr/bin/env python
# coding: utf-8

# In[5]:

####################################################################################################################################################################################################################
##################################################################################################################################################################################
#######################################################################################################################################################################################
####                                PACKAGES                #######

import pandas as pd
import numpy as np
import requests
import json
#import plotly.express as px
#from shapely.geometry import Point
#!pip install missingno
#import missingno as msno
#!pip install streamlit
import streamlit as st


# In[ ]:



st.title('Laadpaal data')
st.sidebar.title('Menu')

st.sidebar.backgroundColor = '#A9A9A9'
st.backgroundColor = '#D3D3D3'


if st.sidebar.button('Home',key = "1"):
    st.header('Home')
    #st.markdown('**Welcome to the Covid19 dashboard**') 
    st.markdown('**Dashboard Chargemaps Netherlands**')
   # st.markdown('This dashboard is made to visualize every subject around the covid pandemic. On the left side of the screen are buttons to select a specific subject. Every subject has his own graphs and description.')
    st.markdown('A Dashboard made to visualize different datasets; The openchargemap was used to visualize the the different EV and their corresponding chargingtime, these visualization are grouped into different categories, where the following topics are analyzed; amount of Chargestations with their corresponding municipality or province visualized on the OpenChargeMap ')
    st.sidebar.button('Voertuigen',key = "2")
    st.sidebar.button('Locations',key = "3")
    st.sidebar.button('Charging stations ',key = "4")
    st.sidebar.button('Statistic explanations',key = "5")
#elif st.sidebar.button('Cases', key = "6"):
elif st.sidebar.button('Voertuigen', key = "6"):
        st.header('Voertuigen')
        st.markdown('**Dashboard Elektrische Voertuigen**') 
        st.markdown('Hier worden visualisaties gemaakt over desbetreffend autos, die dan tegenover de verkoop permaand worden gezet.') 
        st.markdown('Pie chart in percentages. waarbij de auto per brandstof in het totaal worden gevisualiseerd.')
        st.markdown('Aantal autos die verkocht worden per maand gesorteerd op type auto. Aantal voertuigen tegenover het gewicht.')
        st.markdown('Hier Data en visuele data voor de EVs in Nederland.')
    #st.plotly_chart(fig3)
    #st.plotly_chart(fig4)
        st.sidebar.button('Return',key = "7")
#elif st.sidebar.button('Deaths', key = "8"):
elif st.sidebar.button('Locaties', key = "8"):
        st.header('Gemeentes & provincies')
    #st.header('Total Deaths')
    #st.markdown('**Welcome to the Covid19 dashboard of total deaths**') 
    #st.markdown('**Dashboard for the different provinces**') 
    #st.markdown('Here you can find some visualizations of total deaths around the world, per region, per country and per 100.000 inhabitants')
        st.markdown('visualizaties voor de locaties per gemeente en provincie, hierbij wordt weer gekeken naar de laadpaal data en de OpenChargemap, om relevant informatie te tonen.')
    #st.plotly_chart(fig5)
    #st.plotly_chart(fig6)
        st.sidebar.button('Return',key = "9")
#elif st.sidebar.button('Vaccinations', key = "10"):
elif st.sidebar.button('Laadpaal', key = "10"):
        st.header('Charging stations')
        st.markdown('**Dashboard for the Charging stations**') 
    #st.markdown('Here you can find some visualizations of total vaccinations around the world, per region, per country and per 100.000 inhabitants')
    #st.markdown('In this charter there is going thoroughly research on the Charging station spread in the Netherlands, This will include but not limit itself to statistics explanations and visualizing this data in conprehensive charts.
        st.markdown('Hier gaan we diepgaand analyseren hoe de laadpaal data eruit ziet en hoe munipulaties worden uitgevoerd om conclusies te maken. Ook word er visueel aangetond hoe statistische variabelen relatie hebben met elkaar.')
    #st.plotly_chart(fig1)
    #st.plotly_chart(fig2)
        st.sidebar.button('Return',key = "11")
elif st.sidebar.button('Statistic explanations',key = "12"):
    #st.header('Total Recovered')
    #st.markdown('**Welcome to the Covid19 dashboard of total recovered people from covid19**') 
    #st.markdown('Here you can find some visualizations of recovering form covid19 around the world, per region, per country and per 100.000 inhabitants')
    #st.plotly_chart(fig7)
        st.sidebar.button('Return', key = "13")
#elif st.sidebar.button('Manufactures',key = "14"):
    #st.header('Total Manufacturers')
    #st.markdown('**Welcome to the Covid19 dashboard of manufacturers**') 
    #st.markdown('Here you can find some visualizations of manufacturers around the world, per region, per country and per 100.000 inhabitants')
    #st.plotly_chart(fig8)
    #st.sidebar.button('Home', key = "15")
else :
    st.header('Home')
    #st.markdown('**Welcome to the Covid19 dashboard**')
st.markdown('**Dashboard Chargemaps Netherlands**') 
        #st.markdown('Here you can find some visualizations of total cases around the world, per region, per country and per 100.000 inhabitants')

    #st.markdown('This dashboard is made to visualize every subject around the covid pandemic. On the left side of the screen are buttons to select a specific subject. Every subject has his own graphs and description.')




