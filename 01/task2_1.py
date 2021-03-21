ratings_file = open('ml-latest-small/ratings.csv')

ratings = list()

#skip header line
next(ratings_file)
for line in ratings_file:
    ratings.append(line.strip().split(",")[2])

ratings_file.close()

sum = 0

for rating in ratings:
    sum += float(rating)

average = sum/len(ratings)

print(average)  