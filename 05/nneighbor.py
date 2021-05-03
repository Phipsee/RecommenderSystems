import pandas as pd
import numpy as np
import math


class NearestNeighbor(object):

    def __init__(self, users, movies, ratings, userId, neighbor_size):
        self.users = users
        self.movies = movies
        self.ratings = ratings
        self.userId = userId
        self.neighbor_size = neighbor_size

    def showTitlesAndGenresOfUser(self):
        movieRatings = self.ratings.merge(self.movies)
        print(movieRatings.loc[movieRatings['user_id'] ==
                               self.userId, ['movie', 'genres']].head(15))

    def calcUserSimilarity(self):
        # Create a dataframe user-user to save the value of similarity
        self.userSimilarity = pd.DataFrame(
            index=[self.userId], columns=self.users['user_id'])
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
                if movieId not in self.userItems.columns:
                    continue
                if self.userItems.loc[i][movieId] >= 0:
                    # Calculate according to formula
                    upperSum += (self.userItems.loc[self.userId][movieId] - self.userAverages.loc[self.userId]) * (
                        self.userItems.loc[i][movieId] - self.userAverages.loc[i])
                    lowerSum1 += (self.userItems.loc[self.userId]
                                  [movieId] - self.userAverages.loc[self.userId]) ** 2
                    lowerSum2 += (self.userItems.loc[i]
                                  [movieId] - self.userAverages.loc[i]) ** 2
            # Check for division by zero
            if lowerSum1 == 0 or lowerSum2 == 0:
                self.userSimilarity.loc[self.userId][i] = 0
            else:
                # Save to userSimilarity
                self.userSimilarity.loc[self.userId][i] = upperSum / \
                    (math.sqrt(lowerSum1) * math.sqrt(lowerSum2))
        # return the userSimilarity sorted descending
        return self.userSimilarity.sort_values(by=self.userId, ascending=False, axis=1)

    def getPredictionsTestset(self, n, test_set, user_id):
        # Get n neighbors according to the similarity
        neighbors = self.userSimilarity.iloc[:, :n]
        # Calculate the mean rating of all users
        userAverages = self.userItems.mean(axis=1)
        # Get all rated movies from the test set
        moviesOfUser = self.userItems.loc[user_id].dropna().index


        # Get all movie which have not been rated
        predictions = pd.DataFrame(index=test_set['movie_id'], columns=['rating_predicted'])

        for movieId in self.userItems.columns:
            if movieId not in moviesOfUser:
                upperSum = 0
                lowerSum = 0
                # Calculate prediction according to formula
                for n in neighbors.columns:
                    if user_id not in self.userItems.index or user_id not in neighbors.index:
                        continue
                    if not math.isnan(self.userItems.loc[n][movieId]):
                        # similarity times (rating of the user subtracted by mean rating)
                        # similarity as a weight -> more similar more weight
                        upperSum += neighbors.loc[user_id][n] * (
                            self.userItems.loc[n][movieId] - userAverages.loc[n])
                        lowerSum += neighbors.loc[user_id][n]
                # Calculate if the rating from the user is higher or lower than the mean rating of the selected user
                if lowerSum != 0:
                    predictions.loc[movieId] = userAverages.loc[user_id] + \
                        upperSum / lowerSum
        return predictions

    def task_1(self, test_set):
        self.showTitlesAndGenresOfUser()

        # create user item table
        self.userItems = pd.pivot_table(
            self.ratings, index='user_id', columns='movie_id', values='rating')

        # Get similarities
        self.userSimilarity = self.calcUserSimilarity()

        # Get n predictions
        predictions = self.getPredictionsTestset(self.neighbor_size, test_set, self.userId)

        # for id in predictions.head(10).index:
        #   print(self.movies.loc[self.movies['movie_id'] == id])
        comparison_df = predictions.merge(test_set, on='movie_id')

        return comparison_df

    def task_2(self, test_set):

        predicted_rating = pd.DataFrame()

        count = 0
        for user_id in self.userItems.index:
            print(str(count)+" of "+ str(self.userItems.index.size))
            count = count +1
            self.user_id = user_id
            self.userSimilarity = self.calcUserSimilarity()
            predictions = self.getPredictionsTestset(self.neighbor_size, test_set, user_id)
            predicted_rating = predicted_rating.append(predictions)

        return predicted_rating.sort_values(by=['rating_predicted'], ascending=False).head(10)


    def nearestNeighborTestSet(self, test_set):
        comparison_df = self.task_1(test_set)
        ranked_list = self.task_2(test_set)

        print(ranked_list)

        return comparison_df


