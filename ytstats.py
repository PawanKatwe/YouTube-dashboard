from googleapiclient.discovery import build
import streamlit as st
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from wordcloud import WordCloud


api = 'API' #Use your own api here my API is hidden for privacy and security

yt = build('youtube','v3',developerKey=api)



### getting channels stats
def channelstats(id):
    rqst = yt.channels().list(
        part=['snippet','topicDetails','statistics'],
        id=id
    )

    response = rqst.execute()

    ### exrtracting the required data from response and saving it in varibale
    #snipet
    ch_title = response['items'][0]['snippet']['title']
    ch_publishat = response['items'][0]['snippet']['publishedAt'][:10]
    ch_thumbnail = response['items'][0]['snippet']['thumbnails']['medium']['url']

    #topicDetails
    ch_category = re.sub('https://en.wikipedia.org/wiki/','',response['items'][0]['topicDetails']['topicCategories'][0])

    #statistics
    ch_sub_count = response['items'][0]['statistics']['subscriberCount']
    ch_vid_count = response['items'][0]['statistics']['videoCount']
    ch_view_count = response['items'][0]['statistics']['viewCount']


    ############################################################################

    ##### streamlit code ######
    
    

    
    st.markdown("![thumbnail]({})".format(ch_thumbnail))
    
    st.title(ch_title)
    st.text("Published at: {}".format(ch_publishat))
    st.text('Top Category: {}'.format(ch_category))

    st.title(ch_sub_count)
    st.title(ch_view_count)
    st.title(ch_vid_count)



### getting comments of video by video id
def commentstats(vid_id):

    rqst_commentThreads = yt.commentThreads().list(
    part='snippet',
    videoId=vid_id,
    maxResults=100,
    textFormat='plainText'

    )

    response =  rqst_commentThreads.execute()

    comments = [response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'] for i in range(len(response['items']))]

    comments_df = pd.DataFrame(comments,columns=['Comments'])

    return comments_df

#W function to clean comments
def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9_:]+', '', text) #removin @mention
    text = re.sub(r'#', '', text) #removing '#' syboll
    text = re.sub(r'https?:\/\/\S+', '', text) #removing links
    
    return text

### cleaning the comments 
def clean(data):
  data['Comments'] = data['Comments'].apply(cleanText)
  return data

def getSubejectivity(text):
    return TextBlob(text).sentiment.subjectivity

#creating a function to get polarity 
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#creating a new column for subjectivity and polority 
def getSubjectivityAndPolarity(data):
  data['Polarity'] = data['Comments'].apply(getPolarity)
  data['Subjectivity'] = data['Comments'].apply(getSubejectivity)

  return data

def computePositivity(polarityvalue):
    if polarityvalue > 0:
        return "Positive"
    elif polarityvalue < 0:
        return "Negative"
    else:
        return "Nutral"

def analyzeComments(data):    
  data['Analysis'] = data['Polarity'].apply(computePositivity)
  return data

## fucntion to creat wordcloud
def PlotWordcloud(data):
    allwords = ''.join(twts for twts in data['Comments'])
    wrdcld = WordCloud(width = 500, height=300, random_state=21, max_font_size= 120).generate(allwords)
    plt.axis('off')
    fig= plt.figure(figsize=(20,7))
    plt.imshow(wrdcld, interpolation = 'bilinear')
    return fig

## fucntion to creat scatterplot
def scatterPlot(data):
    
    plt.title('Sentimental Analysis')
    plt.xlabel('Tweets')
    plt.ylabel('Polarity & Subjectivity')
    fig, ax = plt.subplots(figsize=(10,5))
    ax = sns.scatterplot(data=data,y='Polarity',x='Subjectivity',hue='Analysis')
    return fig





### getting stats of latest 30 videos 
def channels_videos_stats(channel_id):

  rqst_search = yt.search().list(
    part='snippet',
    channelId = channel_id,
    maxResults=30,
    type='video',
    order='date')
  
  vid_id_search = rqst_search.execute()
  vid_id_list = []
  vid_like_list = []
  vid_views_list = []
  vid_comments_count_list = []
  vid_title_list = []
  vid_publishedDate_list = []        
  
  for i in range(len(vid_id_search['items'])):
    vid_id = vid_id_search['items'][i]['id']['videoId']
    rqst_videos = yt.videos().list(
      part = ['statistics','snippet'],
      id=vid_id)
    vid_stats = rqst_videos.execute()
    vid_title = vid_stats['items'][0]['snippet']["localized"]['title']
    vid_publishedDate = vid_stats['items'][0]['snippet']["publishedAt"][:10]
    vid_views_count = float(vid_stats['items'][0]['statistics']['viewCount'])/1000
    vid_likes_count = vid_stats['items'][0]['statistics']['likeCount']
    vid_comments_count = vid_stats['items'][0]['statistics']['commentCount']

    vid_id_list.append(vid_id)
    vid_like_list.append(vid_likes_count)
    vid_views_list.append(vid_views_count)
    vid_comments_count_list.append(vid_comments_count)
    vid_title_list.append(vid_title)
    vid_publishedDate_list.append(vid_publishedDate)
    
    videos_dict = {
        "Title":vid_title_list,
        "Published Date":vid_publishedDate_list,
        'video_id':vid_id_list,
        'Views in thoudands':vid_views_list,
        'Likes':vid_like_list,
        'Comments_count':vid_comments_count_list
    }
  

  return videos_dict


#### converting stats to dataframe

def Convert_to_df(vid_stat_dict):
    df = pd.DataFrame.from_dict(vid_stat_dict)
    df['Published Date'] = pd.to_datetime(df['Published Date'])
    df['Views in thoudands'] = pd.to_numeric(df['Views in thoudands'])
    df['Likes'] = pd.to_numeric(df['Likes'])
    df['Comments_count'] = pd.to_numeric(df['Comments_count'])
    df = df.sort_values(by="Published Date",ascending=False)

    return df


### funtion to plot views vs likes
def plotviews_vs_likes(df):
    fig1 = plt.figure(figsize=(15,7))
    start = round(df['Views in thoudands'].min(),2)
    stop = round(df['Views in thoudands'].max(),2)
    step= (round(df['Views in thoudands'].max(),2))/5
    sns.scatterplot(data =df, y = 'Views in thoudands',x='Published Date',hue='Likes',size='Likes',sizes=(50,300))
    sns.lineplot(data =df, y = 'Views in thoudands',x='Published Date')
    plt.gcf().autofmt_xdate()
    plt.legend(title='Likes')
    st.pyplot(fig1)

### Function to plot comments vs likes
def plotComments_vs_likes(df):
    fig2 = plt.figure(figsize=(15,7))
    start = round(df['Likes'].min(),2)
    stop = round(df['Likes'].max(),2)
    step= (round(df['Likes'].max(),2))/5
    sns.scatterplot(data =df, y = 'Likes',x='Published Date',hue='Comments_count',size='Comments_count',sizes=(50,300))
    sns.lineplot(data =df, y = 'Likes',x='Published Date')
    plt.gcf().autofmt_xdate()
    plt.legend(title='Comments')
    st.pyplot(fig2)