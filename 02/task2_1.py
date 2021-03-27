import pandas as pd

data = ['Toy Story', 'Jumanji', 'Grumpier Old Men']
# Standard Series
series = pd.Series(data)

print('First element: ', series[0])
print('First two elements: ', series[:2])
print('Last two elements: ', series[-2:])

# Series with custom indices
series = pd.Series(data, index = ['a', 'b', 'c'])

print('Element at position \'b\': ', series['b'])
