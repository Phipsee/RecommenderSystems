import pandas as pd
import numpy as np

def showTitlesAndGenresOfUser(userid):
    movieRatings = ratings.merge(movies)
    print(movieRatings.loc[movieRatings['user_id'] == 1].head(15))
    
    
# Load datasets
users = pd.read_csv('./ml-1m/users.csv')
movies = pd.read_csv('./ml-1m/movies.csv', encoding = 'ISO-8859-1')
ratings = pd.read_csv('./ml-1m/ratings.csv')

# Get a user id
while True:
    userid = input('Enter a user id: ')
    if (users['user_id'] == int(userid)).any():
        break
    print('There is no such user id.')

showTitlesAndGenresOfUser(userid)
