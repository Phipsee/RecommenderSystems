import pandas as pd
import numpy as np
import math

pd.set_option("display.max_rows", None, "display.max_columns", None)

MIN_RATING = 3

# Create and print a user profile according to genres of watched movies
def createUserProfile(userId):
    movieRatings = ratings.merge(movies)
    # Filter out movies without rating
    ratedMovies = movieRatings.loc[movieRatings['user_id'] == userId, ['movie_id', 'movie', 'genres', 'rating']]

    profile = {}

    # Iterate over all movies with a rating >= MIN_RATING
    for genres in ratedMovies.loc[ratedMovies['rating'] >= MIN_RATING]['genres']:
        for genre in genres.split('|'):
            # Everytime a genre occurs add 1
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

# Calculate the similiarity 
def calculateSimilarity(userProfile, ratedMovies):
    # Get all movies that have not yet been rated
    unratedMovies = movies.merge(ratedMovies, on='movie_id', how='outer', indicator=True).query(
        '_merge != "both"').drop(columns='_merge')

    # Get all genres from the user profile
    userGenres = set(userProfile.keys())
    userGenreSum = 0

    # Calculate the sum of all genres in the user profile
    for val in userProfile.values():
        userGenreSum = userGenreSum + val

    similarities = {}

    # Iterate over all unrated movies
    for (index, data) in unratedMovies.iterrows():
        movieGenres = set(data['genres_x'].split('|'))

        genre_counter = 0
        
        # Iterate over genres that are in the user profile and in the current movie
        for key in (userGenres & movieGenres):
            # Weigh the user profile values by the sum of all values
            genre_counter = genre_counter + (userProfile[key] / userGenreSum)

        # Add similarity to the dictionary including the Dice similarity
        similarities[data['movie_id']] = [data['movie_id'], sim(userGenres, movieGenres), genre_counter]

    # Create a dataframe out of the dictionary
    sim_df = pd.DataFrame.from_dict(similarities, orient='index', columns=['movie_id', 'sim', 'genre_counter'])

    # Merge movies and similarity
    recoms = unratedMovies.merge(sim_df, on=['movie_id'])

    # Filter out movies with similarity <= 0
    recoms = recoms.loc[recoms['sim'] > 0]

    # Merge recommendations with ratings and group by movie_id (other columns only there for visualization)
    recomsGrouped = recoms.merge(ratings, on=['movie_id']).groupby(['movie_id','movie_x', 'genres_x', 'sim', 'genre_counter']).size().reset_index(name='counts')

    # Sort by sim - genre_counter - counts descending
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
