import numpy as np


def win_fetch_medal_tally(win_df, year, country):
    win_medal_df = win_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = win_medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = win_medal_df[win_medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = win_medal_df[win_medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = win_medal_df[(win_medal_df['Year'] == int(year)) & (win_medal_df['region'] == country)]
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


def win_medal_tallly(win_df):
    win_medal_tally = win_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    win_medal_tally = win_medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                        ascending=False).reset_index()
    win_medal_tally['total'] = win_medal_tally['Gold'] + win_medal_tally['Silver'] + win_medal_tally['Bronze']

    win_medal_tally['Gold'] = win_medal_tally['Gold'].astype('int')
    win_medal_tally['Silver'] = win_medal_tally['Silver'].astype('int')
    win_medal_tally['Bronze'] = win_medal_tally['Bronze'].astype('int')
    win_medal_tally['total'] = win_medal_tally['total'].astype('int')

    return win_medal_tally


def win_country_year_wise(win_df):
    years = win_df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(win_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country


def win_data_over_time(win_df, col):
    win_nations_over_time = win_df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index().sort_values(
        'index')
    win_nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return win_nations_over_time


def win_event_over_time(win_df, col):
    win_event_over_time = win_df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index().sort_values(
        'index')
    win_event_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return win_event_over_time


def win_athlete_over_time(win_df, col):
    win_athlete_over_time = win_df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index().sort_values(
        'index')
    win_athlete_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return win_athlete_over_time


def win_most_successful(win_df, sport):
    temp_df = win_df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = \
        temp_df['Name'].value_counts().reset_index().head(15).merge(win_df, left_on='index', right_on='Name',
                                                                    how='left')[
            ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x


def win_yearwise_medal_tally(win_df, country):
    temp_df = win_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    win_new_df = temp_df[temp_df['region'] == country]
    win_final_df = win_new_df.groupby('Year').count()['Medal'].reset_index()

    return win_final_df


def win_country_event_heatmap(win_df, country):
    temp_df = win_df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def win_most_successful_countrywise(win_df, country):
    temp_df = win_df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = \
        temp_df['Name'].value_counts().reset_index().head(10).merge(win_df, left_on='index', right_on='Name',
                                                                    how='left')[
            ['index', 'Name_x', 'Sport']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x


def win_weight_vs_height(win_df, sport):
    win_athlete_df = win_df.drop_duplicates(subset=['Name', 'region'])
    win_athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = win_athlete_df[win_athlete_df['Sport'] == sport]
        return temp_df
    else:
        return win_athlete_df


def win_men_vs_women(win_df):
    win_athlete_df = win_df.drop_duplicates(subset=['Name', 'region'])

    win_men = win_athlete_df[win_athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    win_women = win_athlete_df[win_athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    win_final = win_men.merge(win_women, on='Year', how='left')
    win_final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    win_final.fillna(0, inplace=True)

    return win_final
