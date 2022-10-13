#!/usr/bin/env python
# coding: utf-8

# In[5]:

#Packages

import pandas as pd
import geopandas as gpd
import numpy as np
import requests
import seaborn
#import json
import plotly.express as px
import plotly.figure_factory as ff
from shapely.geometry import Point
#!pip install missingno
import missingno as msno
import statsmodels.api as sm
#!pip install streamlit
import streamlit as st
from fuzzywuzzy import fuzz

#Dataframe Roy Locaties
locatie1 = requests.get('https://api.openchargemap.io/v3/poi?key=123?output=json&countrycode=NL&maxresults=20000')
locatie2 = locatie1.json()
df_locatie = pd.DataFrame(locatie2)

addressinfo = df_locatie['AddressInfo']
print(addressinfo.loc[0])
lijst = []

for x in addressinfo:
    inhoud = [x['ID'],x['StateOrProvince'], x['Title'], x['Longitude'], x['Latitude']]
    lijst.append(inhoud)
    
df_locatie = pd.DataFrame(lijst, columns = ['ID','Provincie','Straat','LNG','LAT'])

df_locatie['geometrie'] = df_locatie.apply(lambda x: Point(float(x.LNG), float(x.LAT)), axis = 1)
df_locatie_crs = {'init':'epsg:3857'}
df_locatie_geo = gpd.GeoDataFrame(df_locatie, crs = df_locatie_crs, geometry = df_locatie.geometrie)


df_locatie.isna().sum()

df_locatie = df_locatie.fillna('Nederland')

df_locatie.isna().sum()

df_locatie['Provincie'].unique()

provincies = ['Nederland', 'Noord Holland','Zuid Holland','Zeeland','Noord Brabant','Utrecht','Flevoland','Friesland','Groningen','Drenthe','Overijssel','Gelderland','Limburg']

#String similarity
for i in range(len(provincies)):
    # Elke Provincie in elke rij moet worden vergeleken met de lijst Provincies bovenstaand en daar een ratio aan geven:
    df_locatie[provincies[i]] = df_locatie.apply(lambda x: fuzz.ratio(x['Provincie'], provincies[i]), axis=1)
    
for i in range(len(provincies)):
    #Produceren van een kolom  waarbij de ID van de grootste waarde in de kolom wordt geplaatst
    df_locatie['Provincie'] = df_locatie[['Nederland','Noord Holland','Zuid Holland','Zeeland','Noord Brabant','Utrecht','Flevoland','Friesland','Groningen','Drenthe','Overijssel','Gelderland','Limburg']].idxmax(axis =1)
     
df_locatie1 = df_locatie['Provincie'].value_counts().sort_values(ascending = False)

fig11 = px.scatter_mapbox(df_locatie,
    lon = df_locatie_geo['LNG'], lat = df_locatie_geo['LAT'], color = df_locatie.Provincie,
                        mapbox_style = 'open-street-map', animation_group = 'Provincie', width = 1500, height = 1700, zoom = 7.5
    
                        
        
)
dropdown_buttons = [  {'label': "Alle Provincies", 'method': "update",
                       'args': [{"visible": [True, True, True, True, True, True,True, True, True, True, True, True, True, True]},
                                {'title': 'Alle Provincies'}]},
                    {'label': 'Noord Holland', 'method': 'update','args': [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False, False]}, {'title': 'Noord Holland'}]},
                   {'label': 'Utrecht', 'method': 'update','args': [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False, False]}, {'title': 'Utrecht'}]},  
                    {'label': 'Zuid Holland', 'method': 'update','args': [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False, False]}, {'title': 'Zuid Holland'}]},  
                    {'label': "Groningen", 'method': "update",'args': [{"visible": [False, False, False, True, False, False, False, False, False, False, False, False, False]}, {'title': 'Groningen'}]},
                   {'label': 'Nederland', 'method': 'update','args': [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False, False]}, {'title': 'Nederland'}]},
                   {'label': "Zeeland", 'method': "update",'args': [{"visible": [False, False, False, False, False, True, False, False, False, False, False, False, False]}, {'title': 'Zeeland'}]},
                    {'label': "Limburg", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, True, False, False, False, False, False, False]}, {'title': 'Limburg'}]},
                    {'label': "Noord Brabant", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, True, False, False, False, False, False]}, {'title': 'Noord Brabant'}]},
                    {'label': "Gelderland", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, False, True, False, False, False, False]}, {'title': 'Gelderland'}]},
                    {'label': "Flevoland", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, False, False, True, False, False, False]}, {'title': 'Flevoland'}]},
                    {'label': "Drenthe", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, False, False, False, True, False, False]}, {'title': 'Drenthe'}]},
                    {'label': "Overijssel", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, False, False, False, False, True, False]}, {'title': 'Overijssel'}]},
                    {'label': "Friesland", 'method': "update",'args': [{"visible": [False, False, False, False, False, False, False, False, False, False, False, False, True]}, {'title': 'Friesland'}]},
                   ]
fig11.update_layout(
        title = 'Laadpalen in Nederland per Provincie',
        showlegend = True)

lat_foc = 52.09061
lng_foc = 5.12143
fig11.update_layout({'updatemenus':[{'type': "dropdown",'x': 1.1,'y': 0.75,'showactive': True,'active': 0,'buttons': dropdown_buttons}]},
    geo = dict(
    projection_scale = 11,
    center = dict(lat = lat_foc, lon=lng_foc)
    ))
#dataframe codes MAXIM Voertuigen######################################################################################################

URL3 = requests.get("https://opendata.rdw.nl/resource/m9d7-ebf2.json?$$app_token=j9OjMxvLi7CazM7CK2fssR5D5&$where=Datum_eerste_toelating>20180101&$select=Kenteken,Voertuigsoort,Merk,Handelsbenaming,Massa_rijklaar,Datum_eerste_toelating&$limit=1000000")
#z = URL3.json()
#df_kenteken = pd.DataFrame(z)
#URL4 = requests.get("https://opendata.rdw.nl/resource/8ys7-d773.json?$$app_token=VfcVY98pUi7UHzVmxqLl14OLS&$select=Kenteken,Brandstof_omschrijving&$limit=14200000")
#a = URL4.json()
#df_brandstof = pd.DataFrame(a)
#df_brandstof
#df_voertuigen = df_kenteken.merge(df_brandstof, on = "Kenteken", how = "inner")
#df_voertuigen
#df_voertuigen_na = df_voertuigen[df_voertuigen["Massa_rijklaar"].isna()]
#df_voertuigen_na
#df_voertuigen = df_voertuigen.dropna()
#df_voertuigen['Massa_rijklaar'] = df_voertuigen['Massa_rijklaar'].astype('int')
#duplicates = df_voertuigen["Kenteken"].duplicated()
#print(duplicates)
#df_voertuigen[duplicates]

#uitschieter = np.abs(stats.zscore(df_voertuigen['Massa_rijklaar']))
#print(uitschieter)

#df_voertuigen.drop(df_voertuigen[df_voertuigen.Massa_rijklaar > 20000].index, inplace=True)
#df_voertuigen.drop_duplicates(subset="Kenteken", keep = "first", inplace = True)

#geen spel fouten
#merk_handel = df_voertuigen['Merk'].value_counts().sort_values(ascending = False)
#merk_handel.head(70)

#
#df_voertuigen["Datum_eerste_toelating"] = pd.to_datetime(df_voertuigen['Datum_eerste_toelating'], format='%Y%m%d')
#df_voertuigen.head()

#df_voertuigen_aantal = df_voertuigen.groupby(["Datum_eerste_toelating", "Brandstof_omschrijving"])['Kenteken'].count().reset_index(name='aantal')
#df_voertuigen_aantal

#df_voertuigen_aantal['month_year'] = pd.to_datetime(df_voertuigen_aantal['Datum_eerste_toelating']).dt.to_period('M')
#df_voertuigen_aantal
####Code Laadpalen#### FLOOR Laadpalen #############################################################################################
df_laadpaal = pd.read_csv("laadpaaldata.csv", index_col = "Started")

df_laadpaal["TotalEnergy"] = df_laadpaal["TotalEnergy"] / 1000
df_laadpaal["MaxPower"] = df_laadpaal["MaxPower"] / 1000

df_laadpaal.drop(["2018-12-31 19:34:55", "2018-12-31 18:29:44", "2018-12-31 16:25:27", "2018-12-31 15:33:42", 
                  "2018-12-31 02:48:50", "2018-02-28 20:46:00", "2018-02-29 07:37:53"], inplace = True)

duplicateRows = df_laadpaal[df_laadpaal.duplicated()]

#z = np.abs(stats.zscore(df_laadpaal['ConnectedTime']))

threshold = 3

for x in ['ConnectedTime']:
    q75,q25 = np.percentile(df_laadpaal.loc[:,x],[75,25])
    intr_qr = q75-q25
 
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)
 
    df_laadpaal.loc[df_laadpaal[x] < min,x] = np.nan
    df_laadpaal.loc[df_laadpaal[x] > max,x] = np.nan
    
df_laadpaal = df_laadpaal.dropna(axis = 0)
    
    
for x in ['TotalEnergy']:
    q75,q25 = np.percentile(df_laadpaal.loc[:,x],[75,25])
    intr_qr = q75-q25
 
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)
 
    df_laadpaal.loc[df_laadpaal[x] < min,x] = np.nan
    df_laadpaal.loc[df_laadpaal[x] > max,x] = np.nan
    
df_laadpaal = df_laadpaal.dropna(axis = 0)

for x in ['ChargeTime']:
    q75,q25 = np.percentile(df_laadpaal.loc[:,x],[75,25])
    intr_qr = q75-q25
 
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)
 
    df_laadpaal.loc[df_laadpaal[x] < min,x] = np.nan
    df_laadpaal.loc[df_laadpaal[x] > max,x] = np.nan
    
    
df_laadpaal = df_laadpaal.dropna(axis = 0)

for x in ['MaxPower']:
    q75,q25 = np.percentile(df_laadpaal.loc[:,x],[75,25])
    intr_qr = q75-q25
 
    max = q75+(1.5*intr_qr)
    min = q25-(1.5*intr_qr)
 
    df_laadpaal.loc[df_laadpaal[x] < min,x] = np.nan
    df_laadpaal.loc[df_laadpaal[x] > max,x] = np.nan
    
df_laadpaal = df_laadpaal.dropna(axis = 0)
df_laadpaal["Paalkleeftijd"] = df_laadpaal["ConnectedTime"] - df_laadpaal["ChargeTime"]

df_laadpaal.boxplot(column='MaxPower')
#mnso.matrix(df_laadpaal)

### totaal verbruikte energie
fig1 = px.histogram(df_laadpaal, x="TotalEnergy")
fig1.update_layout(title="Totaal verbruikte energie", xaxis_title="Totale energie (Wh)", yaxis_title="Aantal")
##ConnectedTime
fig2 = px.histogram(df_laadpaal, x="ConnectedTime")
fig2.update_layout(title="Tijd aangesloten aan laadpaal", xaxis_title="Uren", yaxis_title="Aantal")

fig3 = px.histogram(df_laadpaal, x="ChargeTime")
fig3.update_layout(title="Tijd echt aan het laden", xaxis_title="Uren", yaxis_title="Aantal")

fig4 = px.histogram(df_laadpaal, x="ChargeTime", marginal="box")
fig4.update_layout(title="Tjid werkelijk aan het laden aan laadpaal", xaxis_title="Uren", yaxis_title="Aantal")

fig5 = px.histogram(df_laadpaal, x="MaxPower")
fig5.update_layout(title="Maximaal gevraagd vermogen", xaxis_title="Vermogen (W)",
                  yaxis_title="Aantal")

hist_data = [df_laadpaal["ChargeTime"], df_laadpaal["ConnectedTime"], df_laadpaal["Paalkleeftijd"]]
group_labels = ['Oplaadtijd', 'Tijd aangesloten ', 'Paalkleeftijd']

fig6 = ff.create_distplot(hist_data, group_labels)
fig6.update_layout(title="Kansdichtheidfunctie oplaadtijd, tijd aangesloten en paalkleeftijd", 
                  xaxis_title="Uren", yaxis_title="Kans")
##
fig7 = px.histogram(df_laadpaal, x="ChargeTime", marginal="box")
fig7.update_layout(title="Tjid werkelijk aan het laden aan laadpaal", xaxis_title="Uren", yaxis_title="Aantal")
#MaxPower HISt
fig8 = px.histogram(df_laadpaal, x="MaxPower")
fig8.update_layout(title="Maximaal gevraagd vermogen", xaxis_title="Vermogen (W)",
                  yaxis_title="Aantal")
##Scatter
fig9 = px.scatter(df_laadpaal, x="ChargeTime", y="ConnectedTime", trendline = "ols")
fig9.update_layout(title="Tijd verbonden aan laadpaal in verband met werkelijk aan het laden",
                   xaxis_title="Tijd aan het laden (uren)",
                   yaxis_title="Tijd verbonden (uren)")


X = df_laadpaal[['ChargeTime', 'TotalEnergy']]
Y = df_laadpaal['ConnectedTime']

X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()

predictions = model.predict(X) 
print_model = model.summary()

#explanotory_data = pd.DataFrame({"ChargeTime": np.arange(0, 10)})

#mdl_con_vs_char = OLS("ConnectedTime ~ ChargeTime", data=df_laadpaal).fit()

#explanotory_data = pd.DataFrame({"ChargeTime": np.arange(0, 10)})

#prediction_data = explanotory_data.assign(ConnectedTime=mdl_con_vs_char.predict(explanotory_data))

#fig10 = plt.figure()
#sns.regplot(x="ChargeTime", y="ConnectedTime", ci=None, data=df_laadpaal)
#sns.scatterplot(x="ChargeTime", y="ConnectedTime", data=prediction_data, color="red", marker="s")
#plt.xlabel("Tijd aan het laden (uren)")
#plt.ylabel("Tijd aan laadpaal (uren)")
#plt.title("Voorspelling tijd verbonden aan laadpaal in verband met werkelijk aan het laden")


#little_laadpaal = pd.DataFrame({"ChargeTime": [8]})

#pred_little_laadpaal = little_laadpaal.assign(ConnectedTime=mdl_con_vs_char.predict(little_laadpaal))


##Dashboard Codes



###############tekst voor charts
#st.markdown('
############### 
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
    
    
    st.header('Provincies')
    st.markdown('Laadpalen in totaal gelegen in Nederland en bijbehorende provincie.')
    

    st.markdown('visualizaties voor de locaties per gemeente en provincie, hierbij wordt weer gekeken naar de laadpaal data en de OpenChargemap, om relevant informatie te tonen.')
    st.plotly_chart(fig11)
    st.markdown('Wat opvalt aan de plot is dat er een grote dichtheid aan laadpalen in Nederland aanwezig is.')
    st.sidebar.button('Return',key = "9")

elif st.sidebar.button('Laadpaal', key = "10"):
        st.header('Charging stations')
        st.markdown('**Dashboard for the Charging stations**')      
        st.markdown('Hier gaan we diepgaand analyseren hoe de laadpaal data eruit ziet en hoe munipulaties worden uitgevoerd om conclusies te maken. Ook word er visueel aangetond hoe statistische variabelen relatie hebben met elkaar.')
       

                    
        st.plotly_chart(fig1)
        st.plotly_chart(fig3)
        
        st.markdown('De tijd van aansluiten met betrekkeing tot de oplaadtijd en de paalkleeftijd.')
        st.plotly_chart(fig6)
 

        st.markdown('De Scatterplot met bijbehorende plotlijn.')
        st.plotly_chart(fig9)
        
        st.markdown('Lineair regression Model, aangetoont de bijbehorende data voor de correlerende variablen van de laadpaal data.')
        st.write(print_model)
        
       

  
   
        st.sidebar.button('Return',key = "11")
elif st.sidebar.button('Statistic explanations',key = "12"):
    #st.header('Total Recovered')
    #st.markdown('**Welcome to the Covid19 dashboard of total recovered people from covid19**') 
    #st.markdown('Here you can find some visualizations of recovering form covid19 around the world, per region, per country and per 100.000 inhabitants')
    #st.plotly_chart(fig7)
        st.sidebar.button('Return', key = "13")

else :
    st.header('Home')
    #st.markdown('**Welcome to the Covid19 dashboard**')
st.markdown('**Dashboard Chargemaps Netherlands**') 
        #st.markdown('Here you can find some visualizations of total cases around the world, per region, per country and per 100.000 inhabitants')

    #st.markdown('This dashboard is made to visualize every subject around the covid pandemic. On the left side of the screen are buttons to select a specific subject. Every subject has his own graphs and description.')




