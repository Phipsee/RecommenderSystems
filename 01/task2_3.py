def computeMeanMedianMode (fileName):
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

    stars = {};  
    sum = 0
    for rating in ratings:
        sum += float(rating)
        stars[float(rating)] = stars[float(rating)]+1 if float(rating) in stars else 1

    if len(ratings) % 2 == 1:
        median = ratings[len(ratings)/2]
    else:
        median = ratings[int((len(ratings)/2+len(ratings)/2+1)/2)]  

    mode = 0.5
    for key in stars:
        if stars[key] > stars[mode]:
            mode = key
        
    return (sum/len(ratings), median, mode)

def main():
    average, median, mode = computeMeanMedianMode('ml-latest-small/ratings.csv')
    if type(average) == float:
        print('Average: ', average)
        print('Median: ', median)
        print('Mode: ', mode)
    
if __name__ == "__main__":
    main()
