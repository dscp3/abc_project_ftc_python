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
def ratings_and_votes_country(option, df):
    cols = ['restaurant_id', 'country_name']
    
    if option == 'votes':
        cols.append('votes')
        df_aux = df.loc[:, cols].groupby('country_name') \
                        .agg({'restaurant_id': 'count', 'votes': 'sum'}) \
                        .sort_values(by='country_name', ascending=False)
        df_aux.columns = ['restaurant_id', 'votes']
        df_aux.reset_index(inplace=True)
        df_aux['votes_per_restaurant'] = df_aux.apply(lambda x: x['votes']/x['restaurant_id'], axis=1)
        df_aux['votes_per_restaurant'] = np.round(df_aux['votes_per_restaurant']).astype(int)
        df_aux['votes_per_restaurant_avg'] = df_aux['votes_per_restaurant'].mean()
        df_aux['series_votes_per_restaurant'] = df_aux.apply(lambda x: \
                                                             1 if x['votes_per_restaurant'] > x['votes_per_restaurant_avg'] else 0, axis=1)
        df_aux.sort_values(by='votes_per_restaurant', inplace=True)
        
        fig = px.bar(df_aux, x='country_name', y='votes_per_restaurant', text='votes_per_restaurant', 
                     color='series_votes_per_restaurant')
        fig.add_hline(y=df_aux['votes_per_restaurant_avg'][0], line_width=1.5, line_dash="dot", line_color="red",
                     annotation_text="average", annotation_position="top left")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_yaxes(title_text='votes per restaurant')
        fig.update_xaxes(title_text='country')
        return fig
        
    elif option == 'ratings':
        cols.append('aggregate_rating')
        df_aux = df.loc[:, cols].groupby('country_name') \
                        .agg({'restaurant_id': 'count', 'aggregate_rating': 'mean'}) \
                        .sort_values(by='country_name', ascending=False)
        df_aux.columns = ['restaurant_id', 'aggregate_rating']
        df_aux.reset_index(inplace=True)
        df_aux['rating_agg'] = np.round(df_aux['aggregate_rating'],2)
        df_aux['rating_avg_general'] = df_aux['rating_agg'].mean()
        df_aux['series_rating'] = df_aux.apply(lambda x: \
                                                             1 if x['rating_agg'] > x['rating_avg_general'] else 0, axis=1)
        df_aux.sort_values(by='rating_agg', inplace=True)
        
        fig = px.bar(df_aux, x='country_name', y='rating_agg', text='rating_agg', 
                     color='series_rating')
        fig.add_hline(y=df_aux['rating_avg_general'][0], line_width=1.5, line_dash="dot", line_color="red",
                     annotation_text="average", annotation_position="top left")
        fig.update_layout(coloraxis_showscale=False)
        fig.update_yaxes(title_text='rating')
        fig.update_xaxes(title_text='country')
        return fig

def cities_restaurants_per_country(option, df):
    cols = ['country_name']
    if option == 'city':
        cols.append('city')
        df_aux = df.loc[:, cols].groupby('country_name').nunique().sort_values(by='city', ascending=False).reset_index()
        fig = px.bar(df_aux, x='country_name', y='city', text='city')
        fig.update_yaxes(title_text='number of cities')
        fig.update_xaxes(title_text='country')
        return fig
        
    elif option == 'rest':
        cols.append('restaurant_id')
        df_aux = df.loc[:, cols].groupby('country_name').count().sort_values(by='restaurant_id', ascending=False).reset_index()
        fig = px.bar(df_aux, x='country_name', y='restaurant_id', text='restaurant_id')
        fig.update_yaxes(title_text='number of restaurants')
        fig.update_xaxes(title_text='country ')
        return fig

def best_and_worst_cities(option, df):
    cols = ['city', 'aggregate_rating', 'country_name']
    df_aux = df.loc[:, cols].groupby(['city', 'country_name']) \
                        .mean() \
                        .sort_values(by='aggregate_rating')

    df_aux.columns = ['aggregate_rating']
    df_aux['aggregate_rating'] = np.round(df_aux['aggregate_rating'], 2)
    df_aux.reset_index(inplace=True)
    
    if option == 'best':
        df_aux.sort_values(by='aggregate_rating', ascending=False, inplace=True)
        df_aux=df_aux.iloc[0:10,:]
        fig = px.bar(df_aux, x='city', y='aggregate_rating', text='aggregate_rating',color='country_name')
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        fig.update_yaxes(title_text='rating')
        fig.update_xaxes(title_text='country')
        return fig
        
    elif option == 'worst':
        df_aux.sort_values(by='aggregate_rating', inplace=True)
        df_aux=df_aux.iloc[0:10,:]
        fig = px.bar(df_aux, x='city', y='aggregate_rating', text='aggregate_rating',color='country_name')
        fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total ascending'})
        fig.update_yaxes(title_text='rating')
        fig.update_xaxes(title_text='country')
        return fig
    
# Drawing the map
def draw_map(df):
    
    cols = ['restaurant_name', 'average_cost_for_two', 'currency', 'latitude',
            'longitude', 'aggregate_rating', 'cuisines', 'color_name']
    
    df_map = df.copy()
    df_map = df_map.loc[:, cols]
    
    map_x = folium.Map(zoom_start=80)
    marker_cluster = MarkerCluster().add_to(map_x)
    
    for i in range(0,len(df_map)):
        html = f'''
                <div style='font-family: arial; font-size: 11.5'>
                    <p><b>{df_map.iloc[i]['restaurant_name']}</b></p>
                    <p>Avg Price for Two: {df_map.iloc[i]['average_cost_for_two']} ({df_map.iloc[i]['currency']})</p>
                    <p>Type: {df_map.iloc[i]['cuisines']}</p>
                    <p>Rating: {df_map.iloc[i]['aggregate_rating']}/5.0</p>
                </div>
                '''
        iframe = folium.IFrame(html=html, width=140, height=140)
        popup = folium.Popup(iframe, max_width=2000)
        folium.Marker([df_map.iloc[i]['latitude'],
                     df_map.iloc[i]['longitude']],
                    popup=popup,
                   icon=folium.Icon(color=df_map.iloc[i]['color_name'], icon='info-sign')).add_to(marker_cluster)
    
    return map_x

# Libraries
import numpy as np
import pandas as pd
import inflection
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

### ================ Cleaning Data ================ ###

raw_df = pd.read_csv('zomato.csv')
df = clean_data(raw_df)

### ================ Building Streamlit Page ================ ###

st.set_page_config(
    page_title='Geography',
    page_icon='🌎', 
    layout='wide')

image = Image.open('../logo-projeto-ftc.png')

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

st.write('# 🗺 Geography Page')

with st.container():

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        aux = df['country_code'].nunique()
        col1.metric('Total Countries', aux)

    with col2:
        aux = df['city'].nunique()
        col2.metric('Total Cities', aux)

    with col3:
        cols = ['aggregate_rating', 'country_name']
        df_aux = df.loc[:, cols].groupby('country_name').mean().reset_index()
        aux = np.round(df_aux['aggregate_rating'].mean(), 1)
        aux = aux.astype(str) + '/5.0'
        col3.metric('Agg. Rating', aux)
        
    with col4:
        cols = ['cuisines', 'country_name']
        df_aux = df.loc[:, cols].groupby('country_name').nunique().reset_index()
        aux = np.round(df_aux['cuisines'].mean()).astype(int)
        col4.metric('Cuisines per Country', aux)

with st.container():

    st.markdown('---')
    st.markdown('## 🌎 Our Map!')
    st.markdown('##### Global distribution of our restaurants, alongside detailed information. Feel free to check on each area and icon!')
    map_x = draw_map(df)
    folium_static(map_x, width=1200, height=600)

with st.container():

    st.markdown('### Ratings per restaurant per country')
    st.markdown('###### Countries with lower (or higher) rating score than the average')
    
    fig = ratings_and_votes_country('ratings', df)
    st.plotly_chart(fig, use_container_width=True) 

with st.container():

    st.markdown('### Votes per restaurant per country')
    st.markdown('###### Countries with less (or more) votes per restaurant than the average')
    
    fig = ratings_and_votes_country('votes', df)
    st.plotly_chart(fig, use_container_width=True)

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Cities per country')
        fig = cities_restaurants_per_country('city', df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Restaurants per country')
        fig = cities_restaurants_per_country('rest', df)
        st.plotly_chart(fig, use_container_width=True)

with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Best Cities by Ratings')
        fig = best_and_worst_cities('best', df)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('#### Worst Cities by Ratings')
        fig = best_and_worst_cities('worst', df)
        st.plotly_chart(fig, use_container_width=True)

