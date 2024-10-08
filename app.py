import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)



    #fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # stats area

        num_messages, words, num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)


     # monthly timeline

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        plt.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # dailytimeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # finding busisest user in group(group level)

        if selected_user == 'Overall':
            st.title('Most Busy User')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='brown')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)


        #wordcloud

        st.title('Wordcloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words

        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most common words')

        st.pyplot(fig)


        # pickle file








