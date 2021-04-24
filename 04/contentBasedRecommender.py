import pandas as pd
import numpy as np
import math

pd.set_option("display.max_rows", None, "display.max_columns", None)

MIN_RATING = 3


def createUserProfile(userId):
    movieRatings = ratings.merge(movies)
    ratedMovies = movieRatings.loc[movieRatings['user_id'] == userId, ['movie_id', 'movie', 'genres', 'rating']]

    profile = {}

    for genres in ratedMovies.loc[ratedMovies['rating'] >= MIN_RATING]['genres']:
        for genre in genres.split('|'):
            if genre in profile:
                profile[genre] = profile[genre] + 1
            else:
                profile[genre] = 1

    print(profile)

    return profile, ratedMovies


# Dice coefficient
def sim(a, b):
    up = 2 * len(a & b)
    under = len(a) + len(b)
    return up / under


def calculateSimilarity(userProfile, ratedMovies):
    unratedMovies = movies.merge(ratedMovies, on='movie_id', how='outer', indicator=True).query(
        '_merge != "both"').drop(columns='_merge')

    userGenres = set(userProfile.keys())
    userGenreSum = 0

    for val in userProfile.values():
        userGenreSum = userGenreSum + val

    similarities = {}

    for (index, data) in unratedMovies.iterrows():
        movieGenres = set(data['genres_x'].split('|'))

        genre_counter = 0
        for key in (userGenres & movieGenres):
            genre_counter = genre_counter + (userProfile[key] / userGenreSum)

        similarities[data['movie_id']] = [data['movie_id'], sim(userGenres, movieGenres), genre_counter]

    sim_df = pd.DataFrame.from_dict(similarities, orient='index', columns=['movie_id', 'sim', 'genre_counter'])

    recoms = unratedMovies.merge(sim_df, on=['movie_id'])

    recoms = recoms.loc[recoms['sim'] > 0]

    recomsGrouped = recoms.merge(ratings, on=['movie_id']).groupby(['movie_id','movie_x', 'genres_x', 'sim', 'genre_counter']).size().reset_index(name='counts')

    recomsGrouped = recomsGrouped.sort_values(by=['sim', 'genre_counter','counts', ], ascending=False)

    print(recomsGrouped.head(10).to_string())



# Load datasets
users = pd.read_csv('./ml-1m/users.csv')
movies = pd.read_csv('./ml-1m/movies.csv', encoding='ISO-8859-1')
ratings = pd.read_csv('./ml-1m/ratings.csv')

# Get a user id
while True:
    userId = int(input('Enter a user id: '))
    if (users['user_id'] == userId).any():
        break
    print('There is no such user id.')

userProfile, ratedMovies = createUserProfile(userId)

calculateSimilarity(userProfile, ratedMovies)
