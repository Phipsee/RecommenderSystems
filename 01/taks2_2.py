def computeMeanRating (fileName):
    try:
        ratings_file = open(fileName)
    except OSError:
        print('Could not open/read file: ', fileName)
        return 
    except FileNotFoundError:
        print('Could not find file: ', fileName)
        return 
    
    ratings = list()

    #skip header line
    try:
        next(ratings_file)
        for line in ratings_file:
            ratings.append(line.strip().split(",")[2])
    except:
        print('Error while reading file: ', fileName)
            
    ratings_file.close()

    sum = 0

    for rating in ratings:
        sum += float(rating)

    return sum/len(ratings)

def main():
    average = computeMeanRating('ml-latest-small/ratings.csv')
    if type(average) == float:
        print(average)
    
if __name__ == "__main__":
    main()
