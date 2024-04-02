import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total']= medal_tally['Gold']+ medal_tally['Silver']+ medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=df['region'].unique().tolist()
    country=np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

def data_over_time(df,col):
    nations_over_time=df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index()

    nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)

    return nations_over_time

def most_successful(df,sport):
    temp_df=df.dropna(subset=['Medal'])

    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')

    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    
    return x

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df=temp_df[temp_df['region']==country]
    final_df=new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df=temp_df[temp_df['region']==country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df=df.dropna(subset=['Medal'])

    
    temp_df=temp_df[temp_df['region']==country]
    
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name',how='left')[['index','Name_x','Sport']].drop_duplicates('index')

    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    
    return x

def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)  
    if sport!='Overall':  
        temp_df=athlete_df[athlete_df['Sport']==sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df=df.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)

    return final

def sports_wise_analysis(df):
    new_df=df.drop('Event',axis=1)
    sport_regions_df = new_df.groupby('Sport')['region'].nunique().reset_index()
    sport_regions_df.columns = ['Sport', 'Number of Regions']

    return sport_regions_df

def sports_atheltes_analysis(df):
    new_df=df.drop('Event',axis=1)
    athletes_per_sport_df = new_df.drop_duplicates(subset=['Name', 'Sport']).groupby('Sport').size().reset_index(name='Number of Athletes')

    # Sort the DataFrame by 'Number of Athletes'
    athletes_per_sport_df = athletes_per_sport_df.sort_values('Number of Athletes', ascending=False)
    top_10_sports = athletes_per_sport_df.nlargest(10, 'Number of Athletes')

    return top_10_sports

def sports_age_analysis(df):
    new_df=df.drop('Event',axis=1)
    avg_age_per_sport_df = new_df.groupby('Sport')['Age'].mean().nlargest(10).reset_index(name='Average Age')
    return avg_age_per_sport_df
