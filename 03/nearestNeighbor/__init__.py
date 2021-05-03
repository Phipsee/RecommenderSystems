import pandas as pd
import numpy as np
import math


class NearestNeighbor(object):

    def __init__(self, users, movies, ratings, userId):
        self.users = users
        self.movies = movies
        self.ratings = ratings
        self.userId = userId

    def showTitlesAndGenresOfUser(self):
        movieRatings = self.ratings.merge(self.movies)
        print(movieRatings.loc[movieRatings['user_id'] == self.userId, ['movie', 'genres']].head(15))

    def calcUserSimilarity(self):
        # Create a dataframe user-user to save the value of similarity
        self.userSimilarity = pd.DataFrame(index=[self.userId], columns=self.users['user_id'])
        # Calculate the mean rating of all users
        self.userAverages = self.userItems.mean(axis=1)
        # Get all rated movies from the selected user (drop movies without rating)
        moviesOfUser = self.userItems.loc[self.userId].dropna().index

        # For each user calculate sim(a, b)
        for i in self.userSimilarity.columns:
            upperSum = 0
            lowerSum1 = 0
            lowerSum2 = 0
            # Calculate the three sums for each movie
            for movieId in moviesOfUser:
                if self.userItems.loc[i][movieId] >= 0:
                    # Calculate according to formula
                    upperSum += (self.userItems.loc[self.userId][movieId] - self.userAverages.loc[self.userId]) * (
                                self.userItems.loc[i][movieId] - self.userAverages.loc[i])
                    lowerSum1 += (self.userItems.loc[self.userId][movieId] - self.userAverages.loc[self.userId]) ** 2
                    lowerSum2 += (self.userItems.loc[i][movieId] - self.userAverages.loc[i]) ** 2
            # Check for division by zero
            if lowerSum1 == 0 or lowerSum2 == 0:
                self.userSimilarity.loc[self.userId][i] = 0
            else:
                # Save to userSimilarity
                self.userSimilarity.loc[self.userId][i] = upperSum / (math.sqrt(lowerSum1) * math.sqrt(lowerSum2))
        # return the userSimilarity sorted descending
        return self.userSimilarity.sort_values(by=self.userId, ascending=False, axis=1)

    def getPredictions(self, n):
        # Get n neighbors according to the similarity
        neighbors = self.userSimilarity.iloc[:, :n]
        # Calculate the mean rating of all users
        userAverages = self.userItems.mean(axis=1)
        # Get all rated movies from the selected user (drop movies without rating)
        moviesOfUser = self.userItems.loc[self.userId].dropna().index
        # Get all movie which have not been rated
        predictions = self.userItems.loc[self.userId].drop(moviesOfUser)
        for movieId in self.userItems.columns:
            if movieId not in moviesOfUser:
                upperSum = 0
                lowerSum = 0
                # Calculate prediction according to formula
                for n in neighbors.columns:
                    if not math.isnan(self.userItems.loc[n][movieId]):
                        # similarity times (rating of the user subtracted by mean rating)
                        # similarity as a weight -> more similar more weight
                        upperSum += neighbors.loc[self.userId][n] * (
                                    self.userItems.loc[n][movieId] - userAverages.loc[n])
                        lowerSum += neighbors.loc[self.userId][n]
                # Calculate if the rating from the user is higher or lower than the mean rating of the selected user
                if lowerSum != 0: predictions.loc[movieId] = userAverages.loc[self.userId] + upperSum / lowerSum
        return predictions.sort_values(ascending=False, axis=0)

    def getPredictionsTestset(self, n, test_set):
        # Get n neighbors according to the similarity
        neighbors = self.userSimilarity.iloc[:, :n]
        # Calculate the mean rating of all users
        userAverages = self.userItems.mean(axis=1)
        # Get all rated movies from the test set
        moviesOfUser = self.userItems.loc[self.userId].dropna().index
        # Get all movie which have not been rated
        predictions = test_set('movie_id').drop(moviesOfUser)
        for movieId in predictions:
            if movieId not in moviesOfUser:
                upperSum = 0
                lowerSum = 0
                # Calculate prediction according to formula
                for n in neighbors.columns:
                    if not math.isnan(self.userItems.loc[n][movieId]):
                        # similarity times (rating of the user subtracted by mean rating)
                        # similarity as a weight -> more similar more weight
                        upperSum += neighbors.loc[self.userId][n] * (
                                    self.userItems.loc[n][movieId] - userAverages.loc[n])
                        lowerSum += neighbors.loc[self.userId][n]
                # Calculate if the rating from the user is higher or lower than the mean rating of the selected user
                if lowerSum != 0: predictions.loc[movieId] = userAverages.loc[self.userId] + upperSum / lowerSum
        return predictions.sort_values(ascending=False, axis=0)

    def nearestNeighbor(self):

        self.showTitlesAndGenresOfUser()

        # create user item table
        self.userItems = pd.pivot_table(self.ratings, index='user_id', columns='movie_id', values='rating')

        # Get similarities
        self.userSimilarity = self.calcUserSimilarity()

        # Get n predictions
        predictions = self.getPredictions(50)

        for id in predictions.head(10).index:
            print(self.movies.loc[self.movies['movie_id'] == id])


    def nearestNeighborTestSet(self, test_set):

        self.showTitlesAndGenresOfUser()

        # create user item table
        self.userItems = pd.pivot_table(self.ratings, index='user_id', columns='movie_id', values='rating')

        # Get similarities
        self.userSimilarity = self.calcUserSimilarity()

        # Get n predictions
        predictions = self.getPredictionsTestset(50, test_set)
        print('aaa')
        #for id in predictions.head(10).index:
         #   print(self.movies.loc[self.movies['movie_id'] == id])
        comparison_df = predictions.merge(test_set, on='movie_id')

        print(comparison_df)