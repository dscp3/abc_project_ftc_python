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

# Cleaning data
def clean_data(raw_df):
    raw_df = rename_columns(raw_df)
    raw_df = raw_df.dropna()
    raw_df = raw_df.drop_duplicates()
    raw_df['cuisines'] = raw_df.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
    raw_df = raw_df.drop(['switch_to_order_menu'], axis=1)
    raw_df['country_name'] = raw_df['country_code'].apply(lambda x: country_name(x))
    raw_df['color_name'] = raw_df['rating_color'].apply(lambda x: color_name(x))
    return raw_df


# Building Graphs
def main_types_cuisines(df):
    cols = ['cuisines', 'restaurant_id']
    df_aux = df.loc[:, cols].groupby('cuisines').count().reset_index().sort_values(by='restaurant_id', ascending=False)
    df_aux = df_aux.iloc[0:10,:]
    
    fig = px.bar(df_aux, x='cuisines', y='restaurant_id', text='restaurant_id')
    fig.update_yaxes(title_text='number of restaurants')
    fig.update_xaxes(title_text='cuisines')
    return fig

def best_and_worst_cuisines(option, df):
    cols = ['cuisines', 'aggregate_rating']
    df_aux = df.loc[df['cuisines'] != 'Others', cols].groupby('cuisines').mean().reset_index()
    df_aux['aggregate_rating'] = np.round(df_aux['aggregate_rating'], 2)
    
    if option == 'best':
        df_aux = df_aux.sort_values(by='aggregate_rating', ascending=False)
        df_aux = df_aux.iloc[0:10,:]

    elif option == 'worst':
        df_aux = df_aux.sort_values(by='aggregate_rating')
        df_aux = df_aux.iloc[0:10,:]

    fig = px.bar(df_aux, x='cuisines', y='aggregate_rating', text='aggregate_rating')
    fig.update_yaxes(title_text='rating')
    fig.update_xaxes(title_text='cuisines')
    return fig
    
def best_and_worst_rest(option, df):
    cols = ['restaurant_name', 'country_name', 'city', 'cuisines', 'aggregate_rating', 'votes']
    
    if option == 'best':
        df_aux = df.loc[:, cols].sort_values(by=['aggregate_rating', 'votes'], ascending=[False, False])

    elif option == 'worst':
        df_aux = df.loc[df['votes'] > 3, cols]
        df_aux = df_aux.loc[:, cols].sort_values(by=['aggregate_rating', 'votes'], ascending=[True, False])

    df_aux = df_aux.iloc[0:10, :]
    return df_aux

# Libraries
import numpy as np
import pandas as pd
import inflection
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

### ================ Cleaning Data ================ ###

raw_df = pd.read_csv('zomato.csv')
df = clean_data(raw_df)

### ================ Building Streamlit Page ================ ###

st.set_page_config(
    page_title='Cuisines',
    page_icon='🌯', 
    layout='wide')

image = Image.open('../Projeto FTC/logo-projeto-ftc.png')

st.sidebar.image(image, width=120)
st.sidebar.markdown('# Company ABC | Restaurants App')
st.sidebar.markdown('''---''')
country = st.sidebar.multiselect(
    'Select a country:',
    ['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia',
    'India', 'Indonesia', 'New Zeland', 'Philippines', 'Singapure', 'Sri Lanka', 'Turkey',
    'United Arab Emirates', 'United States of America'],
    default=['Brazil', 'England', 'Qatar', 'South Africa', 'Canada', 'Australia'])

# Applying Filter
df = df.loc[df['country_name'].isin(country), :]

st.write('# 🥙 Cuisines Page')

with st.container():

    st.markdown('### Main types of cuisines in our database')
    
    fig = main_types_cuisines(df)
    st.plotly_chart(fig, use_container_width=True) 


with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Best Cuisines by Ratings')
        fig = best_and_worst_cuisines('best', df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Worst Cuisines by Ratings')
        fig = best_and_worst_cuisines('worst', df)
        st.plotly_chart(fig, use_container_width=True)

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Best Restaurants by Ratings and Votes')
        df_aux = best_and_worst_rest('best', df)
        st.dataframe(df_aux.reset_index(drop=True))

    with col2:
        st.markdown('#### Worst Restaurants by Ratings and Votes')
        df_aux = best_and_worst_rest('worst', df)
        st.dataframe(df_aux.reset_index(drop=True))

# with st.container():
#     st.markdown('#### Best Restaurants by Ratings and Votes')
#     df_aux = best_and_worst_rest('best', df)
#     st.dataframe(df_aux.reset_index(drop=True))

# with st.container():
#     st.markdown('#### Worst Restaurants by Ratings and Votes')
#     df_aux = best_and_worst_rest('worst', df)
#     st.dataframe(df_aux.reset_index(drop=True))
