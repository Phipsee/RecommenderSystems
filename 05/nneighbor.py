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

    # calculate the similarities for between ALL users
    def calcUserSimilarity(self):
        # Create a dataframe user-user to save the value of similarity
        self.userSimilarity = pd.DataFrame(
            index=self.users['user_id'], columns=self.users['user_id'])
        # Calculate the mean rating of all users
        self.userAverages = self.userItems.mean(axis=1)
        count = 0
        for selected_user in self.userSimilarity.index:
            print(str(count) + " of " + str(self.userSimilarity.index.size))
            count = count + 1
            # Get all rated movies from the selected user (drop movies without rating)
            if selected_user not in self.userItems.index:
                continue
            moviesOfUser = self.userItems.loc[selected_user].dropna().index

            # For each user calculate sim(a, b)
            for i in self.userSimilarity.columns:
                upperSum = 0
                lowerSum1 = 0
                lowerSum2 = 0
                # Calculate the three sums for each movie
                for movieId in moviesOfUser:
                    if movieId not in self.userItems.columns or i not in self.userItems.index:
                        continue
                    if self.userItems.loc[i][movieId] >= 0:
                        # Calculate according to formula
                        upperSum += (self.userItems.loc[selected_user][movieId] - self.userAverages.loc[selected_user]) * (
                            self.userItems.loc[i][movieId] - self.userAverages.loc[i])
                        lowerSum1 += (self.userItems.loc[selected_user]
                                      [movieId] - self.userAverages.loc[selected_user]) ** 2
                        lowerSum2 += (self.userItems.loc[i]
                                      [movieId] - self.userAverages.loc[i]) ** 2
                # Check for division by zero
                if lowerSum1 == 0 or lowerSum2 == 0:
                    self.userSimilarity.loc[selected_user][i] = 0
                else:
                    # Save to userSimilarity
                    self.userSimilarity.loc[self.userId][i] = upperSum / \
                        (math.sqrt(lowerSum1) * math.sqrt(lowerSum2))
        # return the userSimilarity sorted descending
        self.userSimilarity.to_csv()
        return self.userSimilarity

    # Get prediction for user from test set
    def getPredictionsTestset(self, n, test_set, user_id):
        # Get n neighbors according to the similarity
        neighbors = self.userSimilarity.iloc[:, :n]
        # Calculate the mean rating of all users
        userAverages = self.userItems.mean(axis=1)
        # Get all rated movies from the test set

        # Get all movie which have not been rated
        predictions = pd.DataFrame(index=test_set['movie_id'], columns=['rating_predicted'])

        if user_id not in self.userItems.index:
            print('This user does not have any movies in testset... '+str(user_id))
            return predictions
        moviesOfUser = self.userItems.loc[user_id].dropna().index

        for movieId in self.userItems.columns:
            if movieId not in moviesOfUser:
                upperSum = 0
                lowerSum = 0
                # Calculate prediction according to formula
                for n in neighbors.columns:
                    if user_id not in self.userItems.index or user_id not in neighbors.index or movieId not in self.userItems.columns or n not in self.userItems.index:
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

    # Predict ratings for a certain user for this test_set
    def task_1(self, test_set):

        # create user item table
        self.userItems = pd.pivot_table(
            self.ratings, index='user_id', columns='movie_id', values='rating')

        # Get similarities
        self.userSimilarity = self.calcUserSimilarity()

        # Get n predictions
        predictions = self.getPredictionsTestset(self.neighbor_size, test_set, self.userId)

        comparison_df = predictions.merge(test_set, on='movie_id')

        return comparison_df


    # Predict ratings for all users and select the ten movies and show recall and precision
    def task_2(self, test_set):

        predicted_rating = pd.DataFrame()
        count = 0
        for user_id in self.userItems.index:
            print(str(count)+" of "+ str(self.userItems.index.size))
            count = count +1
            self.user_id = user_id
            predictions = self.getPredictionsTestset(self.neighbor_size, test_set, user_id)
            #predicted_rating = predicted_rating.append(predictions)
            print(predicted_rating)
            if predicted_rating.size <= 0:
                continue
            ranked_list = predicted_rating.merge(test_set, on='movie_id').sort_values(by=['rating_predicted'], ascending=False).head(10)
            print("TASK 2 _________________________________________")
            tp = ranked_list[ranked_list['rating'] > 3].size
            fp = ranked_list.size()
            p = tp / (tp / fp)
            print('Precision: ' + str(p))

            tp = ranked_list[ranked_list['rating'] > 3].size
            fn = ranked_list[ranked_list['rating'] > 3].size
            r = tp / (tp / fn)
            print('Recall: ' + str(r))
            print(ranked_list.to_string)

        return predicted_rating.sort_values(by=['rating_predicted'], ascending=False).head(10)


    def nearestNeighborTestSet(self, test_set):
        comparison_df = self.task_1(test_set)
        ranked_list = self.task_2(test_set)

        return comparison_df, ranked_list


