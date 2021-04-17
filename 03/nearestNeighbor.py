import pandas as pd
import numpy as np
import math

def showTitlesAndGenresOfUser():
    movieRatings = ratings.merge(movies)
    print(movieRatings.loc[movieRatings['user_id'] == userId].head(15))

def calcUserSimilarity():
    userSimilarity = pd.DataFrame(index = [userId], columns = users['user_id'])
    userAverages = userItems.mean(axis = 1)
    moviesOfUser = userItems.loc[userId].dropna().index
    for i in userSimilarity.columns:
        upperSum = 0
        lowerSum1 = 0
        lowerSum2 = 0
        for movieId in moviesOfUser:
            if userItems.loc[i][movieId] >= 0:
                upperSum += (userItems.loc[userId][movieId] - userAverages.loc[userId]) * (userItems.loc[i][movieId] - userAverages.loc[i])
                lowerSum1 += (userItems.loc[userId][movieId] - userAverages.loc[userId]) ** 2
                lowerSum2 += (userItems.loc[i][movieId] - userAverages.loc[i]) ** 2
        if lowerSum1 == 0 or lowerSum2 == 0:
            userSimilarity.loc[userId][i] = 0
        else:    
            userSimilarity.loc[userId][i] = upperSum / (math.sqrt(lowerSum1) * math.sqrt(lowerSum2))

    return userSimilarity.sort_values(by = userId, ascending = False, axis = 1)   

def getPredictions(n):
    neighbors = userSimilarity.iloc[:,:n]
    userAverages = userItems.mean(axis = 1)
    moviesOfUser = userItems.loc[userId].dropna().index
    predictions = userItems.loc[userId].drop(moviesOfUser)
    for movieId in userItems.columns:
        if movieId not in moviesOfUser:
            upperSum = 0
            lowerSum = 0
            for n in neighbors.columns:
                if not math.isnan(userItems.loc[n][movieId]):
                    upperSum += neighbors.loc[userId][n] * (userItems.loc[n][movieId] - userAverages.loc[n])
                    lowerSum += neighbors.loc[userId][n]        
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

userSimilarity = calcUserSimilarity()

predictions = getPredictions(150)

for id in predictions.head(10).index:
    print(movies.loc[movies['movie_id'] == id])
