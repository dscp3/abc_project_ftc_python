### ================ Functions and Libraries ================ ###

# Converting Country_ID
def country_name(country_id):
    COUNTRIES = {
        1: "India",
        14: "Australia",
        30: "Brazil",
        37: "Canada",
        94: "Indonesia",
        148: "New Zeland",
        162: "Philippines",
        166: "Qatar",
        184: "Singapure",
        189: "South Africa",
        191: "Sri Lanka",
        208: "Turkey",
        214: "United Arab Emirates",
        215: "England",
        216: "United States of America"}
    return COUNTRIES[country_id]

# Setting price_type
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Converting Color_Code
def color_name(color_code):
    COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred"}
    return COLORS[color_code]

# Renaming the columns
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Libraries
import numpy as np
import pandas as pd
import inflection
import streamlit as st
from PIL import Image


### ================ Cleaning Data ================ ###

raw_df = pd.read_csv('zomato.csv')
raw_df = rename_columns(raw_df)
raw_df = raw_df.dropna()
raw_df['cuisines'] = raw_df.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
raw_df = raw_df.drop(['switch_to_order_menu'], axis=1)
raw_df = raw_df.drop_duplicates()
df = raw_df.copy()

### ================ Building Streamlit Page ================ ###

st.set_page_config(
    page_title='Home',
    page_icon='🏠')

image = Image.open('logo-projeto-ftc.png')

st.sidebar.image(image, width=120)
st.sidebar.markdown('# Company ABC | Restaurants App')
st.sidebar.markdown('''---''')

st.write('# General Dashboard')

st.markdown(
    '''
    
    This dashboard aims to provide meaningful insights of a ficticious company (ABC) that has a business model related to a marketplace that connects restaurants and customers.

    ### How to use it?

    - GEOGRAPHY
        - Insights about the geographic distribution of restaurants and main cities and countries 

    - CUISINES
        - Main types of 'cuisines' presented, alongside the average rating and best (and worst) restaurants
    
    ''')

with st.container():

    st.markdown('### Big Numbers of Company ABC')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        aux = df['restaurant_id'].nunique()
        col1.metric('Total Restaurants', aux)

    with col2:
        aux = df['country_code'].nunique()
        col2.metric('Total Countries', aux)

    with col3:
        aux = df['city'].nunique()
        col3.metric('Total Cities', aux)
        
    with col4:
        aux = df['votes'].sum()
        col4.metric('Total Votes', aux)

    with col5:
        aux = df['cuisines'].nunique()
        col5.metric('Cuisine Types', aux)
