import streamlit as st
import pandas as pd
import preprocessing
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

st.sidebar.title('Olympics Analysis')
df = preprocessing.preprocess(df,region_df)

user_menu = st.sidebar.radio('Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis'))



if(user_menu=='Medal Tally'):
    st.sidebar.header('Medal Tally')
    yrs,country = helper.country_yrs_list(df)
    selected_year = st.sidebar.selectbox('Select Year',yrs)
    selected_country = st.sidebar.selectbox('Select Country',country) 
    regionwise_medal_tally = helper.get_medal_tally_regionwise(df,selected_year,selected_country)
    if(selected_year=='Overall' and selected_country=='Overall'):
        st.title('Overall Tally')
    if(selected_year!='Overall' and selected_country=='Overall'):
        st.title('Medal Tally in '+str(selected_year)+' Olympics')
    if(selected_year=='Overall' and selected_country!='Overall'):
        st.title(selected_country + ' overall performance')
    if(selected_year!='Overall' and selected_country!='Overall'):
        st.title(selected_country + ' performance in '+ str(selected_year) + ' Olympics')
    st.table(regionwise_medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Stats')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    # nations_overTime = helper.participating_nations(df)
    # fig=px.line(nations_overTime,x="Edition",y="No. of countries")
    # st.plotly_chart(fig)

    st.title('No. of events over time (Each sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)

    st.title('Most successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select sport',sport_list)
    x = helper.mostSuccessful(df,selected_sport)
    st.write(x)


if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country_name = st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.year_wise_medal_tally(df,selected_country_name)
    fig=px.line(country_df,x='Year',y='Medal')
    st.title(selected_country_name + ' Medal tally over the years')
    st.plotly_chart(fig)

    st.title(selected_country_name+' excels in follwoing sports')
    pt = helper.country_heatmap(df,selected_country_name)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Top 10 athletes of '+selected_country_name)
    top10_df = helper.mostSuccessful_countryWise(df,selected_country_name)
    st.table(top10_df)

        
    
    
if user_menu == 'Athlete wise Analysis':
    athlete_df= df.drop_duplicates(subset=['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.title('Distribution of Age')
    fig.update_layout(autosize=False,width=800,height=600)
    st.plotly_chart(fig)

    st.title('Height vs Weight')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select sport',sport_list)
    temp_df = helper.weight_vs_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'])
    st.pyplot(fig)

    final=helper.men_vs_women(df)
    fig=px.line(final,x="Year",y=['Male','Female'])
    st.title('Men vs Women Participation over the years')
    fig.update_layout(autosize=False,width=800,height=600)
    st.plotly_chart(fig)
