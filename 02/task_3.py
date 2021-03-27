import pandas as pd
import numpy as np

# Read the csv file into a dataframe
df = pd.read_csv('./movies_metadata.csv')#

print('Type information of the dataframe')
print(type(df))
print('First movie in the dataset')
print(df.iloc[0])
print('Last movie in the dataset')
print(df.iloc[-1])
print('Information about the movie \'Jumanji\'')
print(df.loc[df['title'] == 'Jumanji'])

# Create dataframe with only selection of columns
small_df = df[['title', 'release_date', 'popularity', 'revenue', 'runtime', 'genres']]


def to_float(x):
    try:
        x = float(x)
    except:
        x = np.nan
    return x

small_df = df[['title', 'release_date', 'popularity', 'revenue', 'runtime', 'genres']].copy()
# convert release date to datetime
small_df.loc['release_date'] = pd.to_datetime(small_df['release_date'], errors='coerce')
# if the release date is valid convert it to string and split it to get the year and allocate it to the 'release_year' column
small_df['release_year'] = small_df['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
# convert the values of 'release_year' to float
small_df['release_year'] = small_df['release_year'].apply(to_float)
# change the type of the column 'release_year' to float
small_df['release_year'] = small_df['release_year'].astype('float')
# drop the 'release_date' column
small_df = small_df.drop(columns="release_date")

print('Movies with release year after 2010')
print(small_df.loc[small_df['release_year'] > 2010]['title'])
