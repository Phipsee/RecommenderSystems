import pandas as pd
import numpy as np
import math

def showTitlesAndGenresOfUser():
    movieRatings = ratings.merge(movies)
    print(movieRatings.loc[movieRatings['user_id'] == userId, ['movie', 'genres']].head(15))

def calcUserSimilarity():
    # Create a dataframe user-user to save the value of similarity
    userSimilarity = pd.DataFrame(index = [userId], columns = users['user_id'])
    # Calculate the mean rating of all users
    userAverages = userItems.mean(axis = 1)
    # Get all rated movies from the selected user (drop movies without rating)
    moviesOfUser = userItems.loc[userId].dropna().index

    #For each user calculate sim(a, b)
    for i in userSimilarity.columns:
        upperSum = 0
        lowerSum1 = 0
        lowerSum2 = 0
        # Calculate the three sums for each movie
        for movieId in moviesOfUser:
            if userItems.loc[i][movieId] >= 0:
                # Calculate according to formula
                upperSum += (userItems.loc[userId][movieId] - userAverages.loc[userId]) * (userItems.loc[i][movieId] - userAverages.loc[i])
                lowerSum1 += (userItems.loc[userId][movieId] - userAverages.loc[userId]) ** 2
                lowerSum2 += (userItems.loc[i][movieId] - userAverages.loc[i]) ** 2
        # Check for division by zero
        if lowerSum1 == 0 or lowerSum2 == 0:
            userSimilarity.loc[userId][i] = 0
        else:
            # Save to userSimilarity
            userSimilarity.loc[userId][i] = upperSum / (math.sqrt(lowerSum1) * math.sqrt(lowerSum2))

    return userSimilarity.sort_values(by = userId, ascending = False, axis = 1)   

def getPredictions(n):
    #
    neighbors = userSimilarity.iloc[:,:n]
    # Calculate the mean rating of all users
    userAverages = userItems.mean(axis = 1)
    # Get all rated movies from the selected user (drop movies without rating)
    moviesOfUser = userItems.loc[userId].dropna().index
    # Get all movie which have not been rated
    predictions = userItems.loc[userId].drop(moviesOfUser)
    for movieId in userItems.columns:
        if movieId not in moviesOfUser:
            upperSum = 0
            lowerSum = 0
            # Calculate prediction according to formula
            for n in neighbors.columns:
                if not math.isnan(userItems.loc[n][movieId]):
                    # similarity times (rating of the user subtracted by mean rating)
                    # similarity as a weight -> more similar more weight
                    upperSum += neighbors.loc[userId][n] * (userItems.loc[n][movieId] - userAverages.loc[n])
                    lowerSum += neighbors.loc[userId][n]
            # Calculate if the rating from the user is higher or lower than the mean rating of the selected user
            if lowerSum != 0 : predictions.loc[movieId] = userAverages.loc[userId] + upperSum / lowerSum
    return predictions.sort_values(ascending = False, axis = 0)
    
# Load datasets
users = pd.read_csv('./ml-1m/users.csv')
movies = pd.read_csv('./ml-1m/movies.csv', encoding = 'ISO-8859-1')
ratings = pd.read_csv('./ml-1m/ratings.csv')

# Get a user id
while True:
    userId = int(input('Enter a user id: '))
    if (users['user_id'] == userId).any():
        break
    print('There is no such user id.')

showTitlesAndGenresOfUser()

#create user item table
userItems = pd.pivot_table(ratings, index = 'user_id', columns = 'movie_id', values = 'rating')

# Get similarities
userSimilarity = calcUserSimilarity()

# Get n predictions
predictions = getPredictions(150)


for id in predictions.head(10).index:
    print(movies.loc[movies['movie_id'] == id])
