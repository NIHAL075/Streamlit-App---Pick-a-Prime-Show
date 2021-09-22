import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import streamlit as st
import plotly.express as px
from collections import Counter
import seaborn as sns
from load_css import local_css

local_css("style.css")

msg = "<div><span class='highlight blue bold','bold'>Pick the next Prime show to Watch </span></div> "
st.markdown(msg, unsafe_allow_html=True)

#Loading the database
tv_shows=pd.read_csv("Prime TV Shows Data set.csv",encoding="iso-8859-1")

#Replacing Data heading
tv_shows.rename(columns={'Year of release': 'year', "No of seasons available" : "seasons", "IMDb rating" : "rating", "Age of viewers" : "age" }, inplace=True)

# Replace using median 
median = tv_shows['rating'].median()
tv_shows['rating'].fillna(median, inplace=True)
tv_shows.drop(['S.no.'],axis=1,inplace=True)


#Raw data display
st.sidebar.markdown("### Show the dataset")
if st.sidebar.checkbox('Show raw data'):
    st.sidebar.subheader('Raw data')
    st.write(tv_shows)

#Genre display
st.sidebar.markdown("### Number of Shows")
st.sidebar.markdown("Genre wise")
select =st.sidebar.selectbox("Visualization Type", ['Histogram', 'Pie chart'], key='1')

#Plotting Genre display
genre_count=tv_shows['Genre'].value_counts()
genre_count=pd.DataFrame({'Genre':genre_count.index,'Number of Shows':genre_count.values})
if st.sidebar.checkbox("Raw ", False, key='0'):
    st.markdown("### Number of Shows per genre")
    st.write(genre_count)

if not st.sidebar.checkbox("Hide", True, key='1'):
    st.markdown("### Number of Shows per Genre")
    if select == 'Histogram':
        fig1=px.bar(genre_count,x='Genre', y='Number of Shows',color='Number of Shows', height=700)
        st.plotly_chart(fig1)
    else:
        fig1=px.pie(genre_count, values='Number of Shows', names='Genre')
        st.plotly_chart(fig1)

st.sidebar.markdown("### Filter by Genre and Language")

#Genre and Language Filter
st.sidebar.subheader("Select Genre and Language")
random_Genre = st.sidebar.radio('A few options from the data set', ('Kids', 'Comedy', 'Drama', 'Action','Sci-fi'))
random_Lang = st.sidebar.radio('A few options from the data set', ('English', 'Hindi'))
msg1="<div><span class='red bold'>Top 5 Recommended shows by Genre and language</span></div>"
st.markdown(msg1,unsafe_allow_html=True)
st.write(tv_shows.query("Genre==@random_Genre" or "Language==@random_Lang")[["Name of the show","Genre", "year", "seasons","Language","rating"]].sample(n=5).sort_values(by = "rating", ascending = False))


st.sidebar.markdown("### Filter by Number of Seasons")
#Season Filter
st.sidebar.subheader("Select Number of Seasons")
random_Season = st.sidebar.radio('A few options from the data set', ('1', '2', '3', '4','5'))
msg2="<div><span class='red bold'>Top 5 Recommended shows by  Number of Seasons</span></div>"
st.markdown(msg2,unsafe_allow_html=True)
st.write(tv_shows.query("seasons ==@random_Season")[["Name of the show","Genre", "year", "seasons","Language","rating"]].sample(n=5).sort_values(by = "rating", ascending = False))

st.sidebar.markdown("### Filter by Viewer age")
#Age Filter
st.sidebar.subheader("Select viewer age")
random_age = st.sidebar.radio('A few options from the data set', ('7+','16+', '18+', '13+', 'All'))
msg3="<div><span class='red bold'>Top 5 Recommended shows by Age</span></div>"
st.markdown(msg3,unsafe_allow_html=True)
st.write(tv_shows.query("age ==@random_age")[["Name of the show","Genre", "year", "seasons","Language","rating"]].sample(n=5).sort_values(by = "rating", ascending = False))
