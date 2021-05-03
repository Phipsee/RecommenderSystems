import pandas as pd
from nneighbor import NearestNeighbor
import numpy as np
import math


# Load datasets and return them
def loadDatasets(sample):
    if sample:
        ratings = pd.read_csv('./ml-1m/ratings.csv').sample(frac=0.001)

        users = pd.read_csv('./ml-1m/users.csv')
        users = users[users['user_id'].isin(ratings['user_id'])]

        movies = pd.read_csv('./ml-1m/movies.csv', encoding='ISO-8859-1')
        movies = movies[movies['movie_id'].isin(ratings['movie_id'])]

    else:
        users = pd.read_csv('./ml-1m/users.csv')
        movies = pd.read_csv('./ml-1m/movies.csv', encoding='ISO-8859-1')
        ratings = pd.read_csv('./ml-1m/ratings.csv')

    return users, movies, ratings

# Create trainingsset with the ration of the training- to testset


def createTrainingsAndTestset(ratio, set):
    trainings_set = set.sample(frac=ratio, random_state=100)
    test_set = set.drop(trainings_set.index)

    return trainings_set, test_set


def inputUserId():
    # Get a user id
    userId = ratings['user_id'].iloc[0]
    print('Values for user: '+str(userId))
    return userId


def nearestNeighbour(user_id, users, movies, ratings, test_set, neighborSize):
   result, ranked_list = NearestNeighbor(users, movies, ratings,user_id, neighborSize).nearestNeighborTestSet(test_set)
   result = result.dropna()

   print("TASK 1 _________________________________________")
   print(result[['rating_predicted', 'rating']])

   result_sum = result['rating_predicted'] - result['rating']

   sum_mae = 0
   sum_rmse = 0
   amount = result_sum.size

   for s in result_sum:
        sum_mae = sum_mae + abs(s)
        sum_rmse = sum_rmse + s*s


   sum_mae = sum_mae / amount
   sum_rmse = math.sqrt(sum_rmse / amount)

   print('MAE: '+str(sum_mae))
   print('RMSE: '+str(sum_rmse))

   print("TASK 2 _________________________________________")
   tp = ranked_list[ranked_list['rating'] > 3].size
   fp = ranked_list.size()
   p = tp / (tp/fp)
   print('Precision: '+str(p))

   tp = ranked_list[ranked_list['rating'] > 3].size
   fn = ranked_list[ranked_list['rating'] > 3].size
   r = tp / (tp/fn)
   print('Recall: '+str(r))

users, movies, ratings = loadDatasets(True)
userId = inputUserId()

if(math.isnan(userId)):
    exit()

ratings_training, ratings_test = createTrainingsAndTestset(0.8, ratings)

ratings_test = ratings_test[ratings_test['user_id'] == userId]

nearestNeighbour(userId, users, movies, ratings_training, ratings_test, 100)

