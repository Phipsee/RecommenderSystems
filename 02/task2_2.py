import pandas as pd

data = [['Toy Story', 21.946943], ['Jumanji', 17.015539], ['Grumpier Old Men', 11.7129]]
# Create dataframe with column headings 'title' and 'popularity'
df = pd.DataFrame(data, columns = ['title', 'popularity'])
# Create new Dataframe with sorted entries
df = df.sort_values(by='popularity', ascending = True, ignore_index = True)
print(df['popularity'])
