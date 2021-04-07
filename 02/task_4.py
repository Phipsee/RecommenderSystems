import pandas as pd

df = pd.read_csv('./ratings_small.csv')

resultList = []

# Group the dataframe by the movieId column
df_grouped = df.groupby('movieId')

# Each tuple in the new dataframe consist of the value by which the frame is grouped and the grouped data
for movieId, frame in df_grouped:
    mean = frame['rating'].mean()
    median = frame['rating'].median()
    # Appending new dict to list
    resultList.append({'id': movieId, 'mean': mean, 'median': median})

# Print list with newline character as separator between dicts
# Asteriks create tuples from list
print(*resultList, sep='\n')
