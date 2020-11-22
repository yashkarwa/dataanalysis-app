import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as pl
#import time

st.title("Comprehension Twitter Airline Sentiment Analysis")
st.sidebar.title("Comprehension Twitter Airline Sentiment Analysis")
st.markdown("----------------------------------------------------------------------------------")
st.markdown("### **Business Problem**")
st.markdown("As a Marketing Researcher in the Airline Industry, I want to understand how the different US airline users experience and Sentiments from their tweeter feeds.")
st.markdown("As a researcher, you need to share the data insight with your stakeholder")
st.markdown("### **Final Product **")
st.markdown("You need to deliver an Analysis Web Application that showcases Users Sentiments & Insight to answer stakeholder below business questions.")
st.markdown("----------------------------------------------------------------------------------")
st.markdown("### **Technical Solution**")
st.markdown("For this exercise - let us say you have built a data pipeline to capture tweets for US Airlines or work with your Data Engineering partner to capture tweets. I am using Kaggle's data to build a web app for data analysis - In the future video, I will use Airflow to create a data pipeline.")
st.write ("Kaggle Link - https://www.kaggle.com/crowdflower/twitter-airline-sentiment")

###################

st.sidebar.markdown("Application to understand US Airline Users Sentiments")
@st.cache(persist=True)
def load_data():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()


### Question1: Show an example of tweets

st.sidebar.markdown("--------")
st.sidebar.subheader("Show Random Tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Hide", True, key=4):
    st.markdown("----------------------------------------------------------------------------------")
    st.markdown("### _Q1: Show Example of a %s Sentiment_" %random_tweet)
    st.write(data.query('airline_sentiment ==@random_tweet')[["text"]].sample(n=3).iat[0,0])
    st.markdown("----------------------------------------------------------------------------------")

### Question2: Show the number of tweets by Sentiment?

st.sidebar.markdown("--------")
st.sidebar.markdown("## Number of Tweets by Sentiment")
select = st.sidebar.selectbox("Visualization", ['Histogram', 'Pie Chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide", True):
    st.markdown("### _Q2: Show number of Tweets by Sentiment_")
    if select == "Histogram":
        fig = plt.bar(sentiment_count, x='Sentiment', y = 'Tweets', height = 500)
        st.plotly_chart(fig)
    else:
        fig = plt.pie(sentiment_count, values ='Tweets', names = 'Sentiment')
        st.plotly_chart(fig)
    st.markdown("----------------------------------------------------------------------------------")

## Question 3: Show Users' Tweet Location based on time

st.sidebar.markdown("--------")
st.sidebar.subheader("When & where users are tweeting from?")
hour = st.sidebar.slider("Hour day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Close", True, key='1'):
    st.markdown('### Q3: _Show Users'' Tweet location based on time_')
    st.markdown("%i tweets between %i:00 and %i:00" %(len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.markdown('### _Raw Data_')
        st.write(modified_data)
    st.markdown("----------------------------------------------------------------------------------")

## Question 4: Breakdown Airline Tweets by Sentiment
st.sidebar.markdown("--------")
st.sidebar.subheader("Breakdown airline tweets by sentiment")
choice = st.sidebar.multiselect('Pick airline', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='0')

if len(choice)> 0:
    st.markdown('### Q4: _Show tweet sentiment counts by Airline _')
    choice_data = data[data.airline.isin(choice)]
    fig_choice = plt.histogram(choice_data,title='Tweet Sentiment Count by Airline', x= 'airline', y='airline_sentiment', histfunc= 'count', color = 'airline_sentiment', facet_col = 'airline_sentiment', labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)
    st.markdown("----------------------------------------------------------------------------------")

## Question 5: Word Cloud by Sentiment
st.sidebar.markdown("--------")
st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for sentiment', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Close", True, key='3'):
    st.markdown('### Q5: _Word Cloud for %s sentiment_' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words = ' '.join(df['text'])
    process_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords= STOPWORDS, background_color='black', height=640, width=800).generate(process_words)
    pl.imshow(wordcloud)
    pl.xticks([])
    pl.yticks([])
    st.pyplot()
    st.markdown("----------------------------------------------------------------------------------")

## Question 6: Show Negative Sentiment Reasons
st.sidebar.markdown("--------")
st.sidebar.markdown("## Negative Sentiment Reason")
select_reason = st.sidebar.selectbox("Visualization", ['Histogram', 'Pie Chart'], key = '6')
negativereason_count = data['negativereason'].value_counts()
sentiment_count = pd.DataFrame({'Negative Reason': negativereason_count.index, 'Tweets Count': negativereason_count.values})

if not st.sidebar.checkbox("Hide", True, key = '6'):
    st.markdown("### _Q6: Show Negative Sentiment Reasons_")
    if select_reason == "Histogram":
        fig = plt.bar(sentiment_count, x='Negative Reason', y = 'Tweets Count', color = 'Negative Reason', height = 500)
        st.plotly_chart(fig)
    else:
        fig = plt.pie(sentiment_count, values ='Tweets Count', names = 'Negative Reason')
        st.plotly_chart(fig)
    st.markdown("----------------------------------------------------------------------------------")

## Question 6: Show Negative Sentiment Reasons by Airline
st.sidebar.markdown("--------")
st.sidebar.subheader("Negative Sentiment Reason by Airline")
choice = st.sidebar.multiselect('Pick airline', ('US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'), key='7')


if len(choice)> 0:
    st.markdown('### Q7: _Show Negative Sentiment Reasons by Airline _')
    choice_data = data[data.airline.isin(choice)]
    fig_choice = plt.histogram(choice_data,title='Negative Tweet Reason by Airline', x= 'negativereason', y = 'airline_sentiment', color = 'airline', histfunc= 'count', labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)
    st.markdown("----------------------------------------------------------------------------------")


##  Reference

if  st.sidebar.checkbox("Reference Link", True, key=9):
    st.write ("Kaggle Link - https://www.kaggle.com/parthsharma5795/comprehensive-twitter-airline-sentiment-analysis")