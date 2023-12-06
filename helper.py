import numpy as np

# Function to filter country and year as per selection
def get_medal_tally_regionwise(df,yrs,country):
    flag=0
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    if yrs == 'Overall' and country == 'Overall':
        tmp_df = medal_df
    if yrs == 'Overall' and country != 'Overall':
        flag=1
        tmp_df = medal_df[medal_df['region']==country]
        
    if yrs != 'Overall' and country == 'Overall':
        tmp_df = medal_df[medal_df['Year']== int(yrs)]
        
    if yrs != 'Overall' and country != 'Overall':
        tmp_df = medal_df[(medal_df['region']==country) & (medal_df['Year']== int(yrs))]
        
    if flag==1:
        z = tmp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=False).reset_index()
    else:
        z = tmp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    
    z['total'] = z['Gold'] + z['Silver'] + z['Bronze'] 
    z['Gold'] = z['Gold'].astype('int')
    z['Silver'] = z['Silver'].astype('int')
    z['Bronze'] = z['Bronze'].astype('int')
    z['total'] = z['total'].astype('int')
    
   
    return z



def medal_tallyRegionWise(df):
    medal_tally_regionwise = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally_regionwise = medal_tally_regionwise.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally_regionwise['total'] = medal_tally_regionwise['Gold'] + medal_tally_regionwise['Silver'] + medal_tally_regionwise['Bronze']

    medal_tally_regionwise['Gold'] = medal_tally_regionwise['Gold'].astype('int')
    medal_tally_regionwise['Silver'] = medal_tally_regionwise['Silver'].astype('int')
    medal_tally_regionwise['Bronze'] = medal_tally_regionwise['Bronze'].astype('int')
    medal_tally_regionwise['total'] = medal_tally_regionwise['total'].astype('int')

    return medal_tally_regionwise


def country_yrs_list(df):
    yrs = df['Year'].unique().tolist()
    yrs.sort(reverse=True)
    yrs.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return yrs,country


def participating_nations(df):
    nations_overTime = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('index')
    nations_overTime.rename(columns={'index':'Edition','Year':'No. of countries'},inplace=True)

    return nations_overTime


def mostSuccessful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df = temp_df[temp_df['Sport']==sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')   
    x.rename(columns={'count':'Medals','region':'Region'},inplace=True)
    return x


def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region']==country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def mostSuccessful_countryWise(df,country):
    temp_df = df.dropna(subset=['region'])
    temp_df = temp_df[temp_df['region']==country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')   
    x.rename(columns={'count':'Medals','region':'Region'},inplace=True)
    return x


def weight_vs_height(df,sport):
    # remove duplicate names and regions
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport!='Overall':
        temp_df= athlete_df[athlete_df['Sport']==sport]
        return temp_df
    else:
        return athlete_df
    

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    men=athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index() 
    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final