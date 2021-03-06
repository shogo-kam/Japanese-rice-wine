import pandas as pd
import numpy as np
import requests
import json
import streamlit as st
import plotly.express as px

st.markdown("""
# ð¶æ¥æ¬éæ¤ç´¢ã¢ããªð¶
##### å¥½ã¿ã®æ¥æ¬éãæ¤ç´¢ã
###### ããã®ããã¼ã¿ (https://sakenowa.com) ã®ãã¼ã¿ãå©ç¨ã
""")

# ã¨ã³ããã¤ã³ã
urls = {
    "å°åä¸è¦§": "https://muro.sakenowa.com/sakenowa-data/api/areas",
    "éæä¸è¦§": "https://muro.sakenowa.com/sakenowa-data/api/brands",
    "èµåä¸è¦§": "https://muro.sakenowa.com/sakenowa-data/api/breweries",
    "ã©ã³ã­ã³ã°": "https://muro.sakenowa.com/sakenowa-data/api/rankings",
    "ãã¬ã¼ãã¼ãã£ã¼ã": "https://muro.sakenowa.com/sakenowa-data/api/flavor-charts",
    "ãã¬ã¼ãã¼ã¿ã°": "https://muro.sakenowa.com/sakenowa-data/api/flavor-tags",
    "éæãã¨ãã¬ã¼ãã¼ã¿ã°": "https://muro.sakenowa.com/sakenowa-data/api/brand-flavor-tags",
    }

# å°ååãåå¾
areas_response = requests.get(urls.get("å°åä¸è¦§")).json()
areas = [area["name"] for area in areas_response["areas"]]
select_areas = st.sidebar.selectbox("é½éåºçãé¸ãã§ãã ãã", areas)

# å°åIDãåå¾
areaId = [area["id"] for area in areas_response["areas"] if area["name"]==select_areas][0]

# èµååãåå¾
breweries_response = requests.get(urls.get("èµåä¸è¦§")).json()
breweries = [breweries["name"] for breweries in breweries_response["breweries"] if breweries["areaId"]==areaId]
select_breweries = st.sidebar.selectbox("èµåãé¸ãã§ãã ãã", breweries)

# èµåIDãåå¾
breweryId = [breweries["id"] for breweries in breweries_response["breweries"] if breweries["name"]==select_breweries][0]

# éæåãåå¾
brands_response = requests.get(urls.get("éæä¸è¦§")).json()
brands = [brands["name"] for brands in brands_response["brands"] if brands["breweryId"]==breweryId]
select_brands = st.sidebar.selectbox("å¥½ããªéæãé¸ãã§ãã ãã", brands)

# éæIDãåå¾
brandId = [brands["id"] for brands in brands_response["brands"] if brands["name"]==select_brands][0]

# rankings
rankings_response = requests.get(urls.get("ã©ã³ã­ã³ã°")).json()


# ãã¬ã¼ãã¼ãã£ã¼ããåå¾
flavor_charts_response = requests.get(urls.get("ãã¬ã¼ãã¼ãã£ã¼ã")).json()
flavor_charts = [flavor_charts for flavor_charts in flavor_charts_response["flavorCharts"] if flavor_charts["brandId"]==brandId]

# plotlyã§ã¬ã¼ãã¼ãã£ã¼ããè¡¨ç¤º
st.write("----------------------------------------------")
st.markdown(f'## {select_brands}ã®ãã¬ã¼ãã¼ãã£ã¼ã')

# ä¾å¤å¦ç
try:
    df = pd.DataFrame(flavor_charts)
    df = df.drop('brandId', axis=1)
    # è¦ãããããããã«ã«ã©ã åãå¤æ´ããã®å¾plotlyã§èª­ã¿è¾¼ããããã«ãã¼ã¿ãè»¢ç½®
    df = df.rename(columns={'f1':'è¯ãã', 'f2':'è³é', 'f3':'éå', 'f4':'ç©ãã', 'f5':'ãã©ã¤', 'f6':'è»½å¿«'}).T
    fig = px.line_polar(df, r=df[0], theta=df.index, line_close=True, range_r=[0,1])
    st.plotly_chart(fig)

# ãã¬ã¼ãã¼ãã£ã¼ãã®ãã¼ã¿ããªããã®ãããã®ã§ä¾å¤å¦ç
except:
    st.markdown('### ãã®éæã¯æå ±ãå°ãªãããã¬ã¼ãã¼ãã£ã¼ãè¡¨ç¤ºãã§ãã¾ããã»ã»ã»')