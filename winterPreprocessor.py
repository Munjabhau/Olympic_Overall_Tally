import pandas as pd


def preprocess(win_df, win_region_df):
    # Filtering for winter olympics
    win_df = win_df[win_df['Season'] == 'Winter']
    # merge with region_df
    win_df = win_df.merge(win_region_df, on='NOC', how='left')
    # dropping duplicates
    win_df.drop_duplicates(inplace=True)
    # one hot encoding medals
    df = pd.concat([win_df, pd.get_dummies(win_df['Medal'])], axis=1)
    return df
