import pandas as pd

userId = 1

df = pd.read_csv('./ratings_small.csv')

# Group dataframe by userId
df_grouped_user = df.groupby('userId')

# Create a set by the rated user movies, unique() for probable multiple ids
movies_rated_by_user = set(df_grouped_user.get_group(userId)['movieId'].unique())

print('Movies rated by User ' + str(userId) + ' : ' + str(movies_rated_by_user))

related_user = []

for userId, frame in df_grouped_user:
    # Apply intersection on the movie set from both users
    same_movies = movies_rated_by_user.intersection(set(frame['movieId']))
    # If there are at least 3 movie left, remember the user
    len(same_movies) >= 3 and related_user.append(userId)

print(*related_user, sep=', ')
