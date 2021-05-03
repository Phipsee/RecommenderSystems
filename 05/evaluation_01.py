import pandas as pd
from nneighbor import NearestNeighbor
import numpy as np
import math


# Load datasets and return them
def loadDatasets(sample):
    if sample:
        users = pd.read_csv('./ml-1m/users.csv').sample(frac=0.2)
        movies = pd.read_csv('./ml-1m/movies.csv', encoding='ISO-8859-1').sample(frac=0.2)
        ratings = pd.read_csv('./ml-1m/ratings.csv').sample(frac=0.2)
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
    while True:
        userId = int(input('Enter a user id: '))
        if (users['user_id'] == userId).any():
            break
        print('There is no such user id.')

    return userId


def nearestNeighbour(user_id, users, movies, ratings, test_set, neighborSize):
   result = NearestNeighbor(users, movies, ratings,user_id, neighborSize).nearestNeighborTestSet(test_set)
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


users, movies, ratings = loadDatasets(False)
userId = inputUserId()

if(math.isnan(userId)):
    exit()

ratings_training, ratings_test = createTrainingsAndTestset(0.8, ratings)

ratings_test = ratings_test[ratings_test['user_id'] == userId]

nearestNeighbour(userId, users, movies, ratings_training, ratings_test, 100)

