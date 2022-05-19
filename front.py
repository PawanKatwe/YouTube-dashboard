from matplotlib.pyplot import yscale
import ytstats

## setting paglayout to wide as defualt layout in centered
ytstats.st.set_page_config(layout='wide')


#### getting channel info


def channel_view():

    
    ch_id1 = ytstats.st.text_input('Enter the channel ID')

    if ytstats.st.checkbox('Add channel to compare'):
        ch_id2 = ytstats.st.text_input('Enter the 2nd channel ID')

        if ch_id2:
            header, ch1, ch2,  = ytstats.st.columns((2,3,3))
            with header:
                for i in range(12):
                    ytstats.st.title('        ')

                ytstats.st.text('')
                ytstats.st.markdown( '<h2>subsribers</h2>',unsafe_allow_html=True)
                ytstats.st.text('')
                ytstats.st.markdown( '<h2>Views</h2>',unsafe_allow_html=True)
                ytstats.st.markdown( '<h2>Videos</h2>',unsafe_allow_html=True)
                ytstats.st.text('')
                ytstats.st.markdown( '<h3>Views vs Likes \n of last 30 videos</h3>',unsafe_allow_html=True)
                for i in range(6):
                    ytstats.st.title('        ')
                ytstats.st.markdown( '<h3>Comments vs Likes \n of last 30 videos</h3>',unsafe_allow_html=True)
                for i in range(6):
                    ytstats.st.title('        ')
                ytstats.st.markdown( '<h3>DataFrame</h3>',unsafe_allow_html=True)
            with ch1:
                ytstats.channelstats(ch_id1)
                df1 = ytstats.Convert_to_df(ytstats.channels_videos_stats(ch_id1))
                ytstats.plotviews_vs_likes(df1)
                ytstats.plotComments_vs_likes(df1)
                ytstats.st.write(df1)


            with ch2:
                ytstats.channelstats(ch_id2)
                df2 = ytstats.Convert_to_df(ytstats.channels_videos_stats(ch_id2))
                ytstats.plotviews_vs_likes(df2)
                ytstats.plotComments_vs_likes(df2)
                ytstats.st.write(df2)

    else:
        if ch_id1:
            header, col = ytstats.st.columns((1,3))
            with header:
                for i in range(12):
                    ytstats.st.title('        ')

                ytstats.st.text('')
                ytstats.st.markdown( '<h2>subsribers</h2>',unsafe_allow_html=True)
                ytstats.st.text('')
                ytstats.st.markdown( '<h2>Views</h2>',unsafe_allow_html=True)
                ytstats.st.markdown( '<h2>Videos</h2>',unsafe_allow_html=True)
                for i in range(6):
                    ytstats.st.title('        ')
                ytstats.st.markdown( '<h3>Views vs Likes \n of last 30 videos</h3>',unsafe_allow_html=True)
                for i in range(10):
                    ytstats.st.title('        ')
                ytstats.st.markdown( '<h3>Comments vs Likes \n of last 30 videos</h3>',unsafe_allow_html=True)
            with col:
                ytstats.channelstats(ch_id1)
                df = ytstats.Convert_to_df(ytstats.channels_videos_stats(ch_id1))
                ytstats.plotviews_vs_likes(df)
                ytstats.plotComments_vs_likes(df)
                ytstats.st.write(df)

def comment_view():

    vid_id = ytstats.st.text_input('Enter video id')
    if vid_id:
        ytstats.st.header('Analysis of comments')

        col1,col2 = ytstats.st.columns(2)
       
        df = ytstats.clean(ytstats.commentstats(vid_id))

        df = ytstats.getSubjectivityAndPolarity(df)
        df= ytstats.analyzeComments(df)

        
        with col1:
            ytstats.st.pyplot(ytstats.scatterPlot(df))
        with col2:
            ytstats.st.pyplot(ytstats.PlotWordcloud(df))

        


option = ytstats.st.radio('What you want to analyze?',('Channel','Video','Playlist'))

if option == 'Channel':
    channel_view()
elif option == 'Video':
    comment_view()
else:
    ytstats.st.title('This funcion is not available yet')


