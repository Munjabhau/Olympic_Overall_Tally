# Import Requried libarary
import streamlit as st
import pandas as pd
import preprocessor, helper, winterPreprocessor, winterhelper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df, region_df)

win_df = pd.read_csv('athlete_events.csv')
win_region_df = pd.read_csv('noc_regions.csv')
win_df = winterPreprocessor.preprocess(win_df, win_region_df)

st.sidebar.title("OLYMPIC OVERALL TALLY")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Summer Medal Tally', 'Summer Overall Analysis', 'Summer Country-wise Analysis', 'Summer Athlete wise Analysis',
     'Winter Medal Tally', 'Winter Overall Analysis', 'Winter Country-wise Analysis', 'Winter Athlete wise Analysis')
)

if user_menu == 'Summer Medal Tally':
    st.sidebar.header("Summer Olympic Medal Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Summer Olympic Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Summer Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Event over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("Number of Events over time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)

    st.pyplot(fig)

    st.title("Most Successfull Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a Sport", sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Summer Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally  over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Summer Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Distribution of Age wrt Sports (Gold Medalist)
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    st.plotly_chart(fig)

    # Distribution of Age wrt Sports (Silver Medalist)
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Silver Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Height VS Weight")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)

    st.pyplot(fig)

    st.title("Men VS Women Participation Over the year")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

# -------------------------------------------------Winter Olympic Overall Analysis---------------------------------------------------------------------------------------
if user_menu == 'Winter Medal Tally':
    st.sidebar.header("Winter Olympic Tally")
    years, country = winterhelper.win_country_year_wise(win_df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    win_medal_tally = winterhelper.win_fetch_medal_tally(win_df, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Winter Olympic Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Winter Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Winter Olympic Performance ")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Winter Olympics")
    st.table(win_medal_tally)

if user_menu == 'Winter Overall Analysis':
    editions = win_df['Year'].unique().shape[0]
    cities = win_df['City'].unique().shape[0]
    sports = win_df['Sport'].unique().shape[0]
    events = win_df['Event'].unique().shape[0]
    athletes = win_df['Name'].unique().shape[0]
    nations = win_df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    win_nations_over_time = winterhelper.win_data_over_time(win_df, 'region')
    fig = px.line(win_nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    win_event_over_time = winterhelper.win_event_over_time(win_df, 'Event')
    fig = px.line(win_event_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    win_athlete_over_time = winterhelper.win_athlete_over_time(win_df, 'Name')
    fig = px.line(win_athlete_over_time, x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("Number of Events over time")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = win_df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most Successfull Athletes")
    win_sport_list = win_df['Sport'].unique().tolist()
    win_sport_list.sort()
    win_sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox("Select a Sport", win_sport_list)
    x = winterhelper.win_most_successful(win_df, selected_sport)
    st.table(x)

if user_menu == 'Winter Country-wise Analysis':
    st.sidebar.title("Winter Country Wise Analysis")

    win_Country_list = win_df['region'].dropna().unique().tolist()
    win_Country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', win_Country_list)

    win_country_df = winterhelper.win_yearwise_medal_tally(win_df, selected_country)
    fig = px.line(win_country_df, x='Year', y="Medal")
    st.title(selected_country + " Medal Tally  over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = winterhelper.win_country_event_heatmap(win_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    win_top10_df = winterhelper.win_most_successful_countrywise(win_df, selected_country)
    st.table(win_top10_df)

if user_menu == 'Winter Athlete wise Analysis':
    win_athlete_df = win_df.drop_duplicates(subset=['Name', 'region'])

    x1 = win_athlete_df['Age'].dropna()
    x2 = win_athlete_df[win_athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = win_athlete_df[win_athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = win_athlete_df[win_athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Distribution of Age wrt Sports (Gold Medalist)
    x = []
    name = []
    win_famous_sports = ['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
                         'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
                         'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
                         'Snowboarding', 'Short Track Speed Skating', 'Skeleton',
                         'Military Ski Patrol', 'Alpinism']

    for win_sport in win_famous_sports:
        temp_df = win_athlete_df[win_athlete_df['Sport'] == win_sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(win_sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports (Gold Medalist)")
    st.plotly_chart(fig)

    win_sport_list = win_df['Sport'].unique().tolist()
    win_sport_list.sort()
    win_sport_list.insert(0, 'Overall')

    st.title("Height VS Weight")
    win_selected_sport = st.selectbox("Select a Sport", win_sport_list)
    temp_df = winterhelper.win_weight_vs_height(win_df, win_selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'], temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)
    st.pyplot(fig)

    st.title("Men VS Women Participation Over the year")
    win_final = winterhelper.win_men_vs_women(win_df)

    fig = px.line(win_final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
