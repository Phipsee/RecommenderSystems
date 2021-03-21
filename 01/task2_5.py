from utilityModule import Statistics as stats

def main():
    print('Mean rating: ', stats.computeMeanRating('ml-latest-small/ratings.csv'))

if __name__ == "__main__":
    main()