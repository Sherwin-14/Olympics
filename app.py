import streamlit as st
import pandas as pd
import numpy as np
import preprocessor, helper
import plotly.express as px
import plotly.io as py
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import matplotlib.animation as animation    

st.set_page_config(layout="wide")

df=pd.read_csv('dataset/athlete_events.csv')
region_df=pd.read_csv('dataset/noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympic Analysis')

st.sidebar.image('images/Untitled.png')

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Home','Medal Tally','Overall Analysis','Country Wise Analysis','Athlete Wise Analysis','Sport Wise Analysis','About Me')
)



if user_menu=='Home':
    st.title('Olympic Analysis Tool')
    st.image('images/16284178410156.jpg',caption="Olympics Uptill Now",width=900)
    st.write("""
    Welcome to the Olympic Analysis Tool! This application provides a comprehensive analysis of the Olympic Games data up to 2016. Whether you're a sports enthusiast, a data analyst, or just curious about the Olympics, this tool offers a wealth of information at your fingertips. Dive in and explore the rich history of this global event.
    The Olympic Games, a quadrennial international multi-sport event, is considered the world's foremost sports competition. With more than 200 nations participating, the Olympics symbolize unity in diversity and foster a spirit of camaraderie and international cooperation. The Games are characterized by their unique blend of sporting prowess, cultural exchange, and a commitment to promoting peace and understanding across the globe.

    The modern Olympics were inspired by the ancient Olympic Games held in Olympia, Greece, from the 8th century BC to the 4th century AD. Baron Pierre de Coubertin founded the International Olympic Committee (IOC) in 1894, leading to the first modern Games in Athens in 1896. The IOC is the governing body of the Olympic Movement, with the Olympic Charter defining its structure and authority.

    The evolution of the Olympic Movement during the 20th and 21st centuries has resulted in several changes to the Olympic Games. Some of these adjustments include the creation of the Winter Olympic Games for snow and ice sports, the Paralympic Games for athletes with disabilities, the Youth Olympic Games for athletes aged 14 to 18, the five Continental games (Pan American, African, Asian, European, and Pacific), and the World Games for sports that are not contested in the Olympic Games.

    The Deaflympics and the Special Olympics are also endorsed by the IOC. The IOC has had to adapt to a variety of economic, political, and technological advancements. The abuse of amateur rules by the Eastern Bloc nations prompted the IOC to shift away from pure amateurism, as envisioned by Coubertin, to allowing participation of professional athletes. The growing importance of mass media created the issue of corporate sponsorship and commercialization of the Games.

    World Wars led to the cancellation of the 1916, 1940, and 1944 Games. Large boycotts during the Cold War limited participation in the 1980 and 1984 Games. The Olympic Movement consists of international sports federations (IFs), NOCs, and organizing committees for each specific Olympic Games. As the decision-making body, the IOC is responsible for choosing the host city for each Games. The host city is responsible for organizing and funding a celebration of the Games consistent with the Olympic Charter.

    The Olympic program, consisting of the sports to be contested at the Games, is also determined by the IOC. The celebration of the Games encompasses many rituals and symbols, such as the Olympic flag and torch, as well as the opening and closing ceremonies. Over 13,000 athletes compete at the Summer and Winter Olympic Games in 33 different sports and nearly 400 events.

    The first, second, and third-place finishers in each event receive Olympic medals: gold, silver, and bronze, respectively. The Games have grown in scale to the point that nearly every nation is represented. Such growth has created numerous challenges, including boycotts, doping, bribery, and a terrorist attack in 1972. Every two years, the Olympics and its media exposure provide unknown athletes with the chance to attain national, and sometimes international, fame. The Games also constitute a major opportunity for the host city and country to showcase themselves to the world.         
    """)

if user_menu=='About Me':
    st.title('About Me')
    st.markdown(""" 
     <div style="text-align:center">           
    <a href="https://github.com/Sherwin-14">
    <img src="https://avatars.githubusercontent.com/u/141290943?v=4" alt="GitHub" style="width:200px;height:200px;border-radius:50%;">
    </a>   
    </div>            
""", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("""
    Hello! I am Sherwin Varghese the developer of this Olympic Analysis Tool. As a data scientist, I have a deep passion for machine learning, sports analytics, and computer vision. I've always been fascinated by the power of data and the insights it can provide.

    My interest in sports and machine learning led me to create this comprehensive tool for analyzing Olympic Games data. I believe that the combination of sports and data science can provide unique and valuable insights, and I wanted to create a platform where anyone can explore these insights in an interactive and user-friendly way.

    This Olympic Analysis Tool is not just a product of my technical skills, but also a reflection of my interests and passions. Whether you're a fellow data enthusiast or a casual user, I hope this tool provides you with a deeper understanding of the Olympics through data. Enjoy exploring!
    """)
    


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)
    selected_country=st.sidebar.selectbox("Select Year",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overally Tally')
    if selected_year!='Overall' and selected_country=='Overall':
        st.title('Medal Tally in' +" " +str(selected_year) + " " + "Olympics")
    if selected_year=='Overall' and selected_country!='Overall':
         st.title('All Time Medal Tally for ' + " "+ str(selected_country) + " " + " in Olympics")
    if selected_year!='Overall' and selected_country!='Overall':
        st.title(selected_country +" "+"peformance in" + " "+ str(selected_year))            
    st.table(medal_tally)

if user_menu =='Overall Analysis' :
    editions=df['Year'].unique().shape[0]
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    
    st.title("Top Statistics")
    col1,col2,col3= st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3= st.columns(3)    
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes) 
    with col3:
        st.header("Nations")
        st.title(nations)   

    nations_over_time=helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y='region')
    fig.update_layout(autosize=False, width=900, height=400)
    st.title("Participating Nations over the Years")
    st.plotly_chart(fig)

    events_over_time=helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    fig.update_layout(autosize=False, width=900, height=400)
    st.title("Events over the Years")
    st.plotly_chart(fig)

    athletes_over_time=helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name")
    fig.update_layout(autosize=False, width=900, height=400)
    st.title("Athletes over the Years")
    st.plotly_chart(fig)

    st.title("No of Events over time(Every Sport)")
    x = df.drop_duplicates(['Year', 'Event', 'Sport'])
    fig, ax = plt.subplots(figsize=(18, 18))
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True, ax=ax)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')

    selected_sport=st.selectbox('Select a Sport',sports_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)


if user_menu =='Country Wise Analysis' :

    st.sidebar.title("Country Wise Analysis")
    
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country=st.sidebar.selectbox('Select a Country',country_list)

    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    fig.update_layout(autosize=False, width=900, height=400)
    st.title("Medal Tally for"+" " +str(selected_country)+" " +"over the Years")
    st.plotly_chart(fig)

    pt=helper.country_event_heatmap(df,selected_country)
    
    st.title(selected_country +" "+"excels in the following sports")
    fig, ax = plt.subplots(figsize=(18, 18))
    sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes of '+" "+str(selected_country))
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)
    

if user_menu=="Athlete Wise Analysis":
    athlete_df=df.drop_duplicates(subset=['Name','region'])

    x1=athlete_df['Age'].dropna()
    x2=athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3=athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4=athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()    

    fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=500)

    st.title("Distribution of Age")
    st.plotly_chart(fig)

  

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



    for sports in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sports]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sports)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=500)
    st.title("Distribution of Age wrt to Sports (Gold Medal)") 
    st.plotly_chart(fig)

    sports_list=df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0,'Overall')
 
    st.title('Height Vs Weight')
    selected_sport=st.selectbox('Select a Sport',sports_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=40)
    st.pyplot(fig)

    st.title("Men vs Women Participation Over The Years")
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    fig.update_layout(autosize=False, width=1000, height=500)
    st.plotly_chart(fig)  


if user_menu=='Sport Wise Analysis':

    sports_regions_df=helper.sports_wise_analysis(df)

    sports = sports_regions_df['Sport'].unique().tolist()
    sports.insert(0, 'Overall')

    st.title("Countries Participation All Time wrt to Sports")

    # Create a dropdown for the sports
    sport = st.selectbox('Select a Sport', sports)

# Filter the DataFrame for the selected sport
    df_sport = sports_regions_df[sports_regions_df['Sport'] == sport]


    # Display the number of regions in a card-like format
    if sport == 'Overall':
    # Display the entire DataFrame, sorted by 'Number of Regions' in descending order
        st.table(sports_regions_df.sort_values('Number of Regions', ascending=False))
    
    else:
    # Filter the DataFrame for the selected sport
        df_sport = sports_regions_df[sports_regions_df['Sport'] == sport]
        st.table(df_sport)
    
    st.title("Top 10 Sports in terms of Particpation (All Time)")
    top_10=helper.sports_atheltes_analysis(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(top_10['Sport'], top_10['Number of Athletes'], color=plt.cm.magma(np.linspace(0, 1, len(top_10))))
    ax.set_xlabel('Number of Athletes')
    ax.set_ylabel('Sport')
    ax.set_xlim(left=0) 
    ax.set_title('Number of Athletes per Sport')
    ax.invert_yaxis()  # Invert the y-axis to display the sport with the most athletes at the top
    st.pyplot(fig)

    st.title("Sports With Highest Average Age")
    avg_age=helper.sports_age_analysis(df)
    fig = px.scatter(avg_age, x='Sport', y='Average Age')
    fig.update_layout(autosize=False, width=1000, height=500)
    st.plotly_chart(fig)
