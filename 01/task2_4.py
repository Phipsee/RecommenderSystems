import csv

def getFileContentInfo (fileName):
    try:
        enc = 'utf-8'
        plainFile = open(fileName, encoding=enc)
    except OSError:
        print('Could not open/read file: ', fileName)
        return 
    except FileNotFoundError:
        print('Could not find file: ', fileName)
        return 
    
    file = csv.reader(plainFile)
    
    genres = {}

    try:
        #skip header line
        next(file)
        for line in file:
            for genre in line[2].split('|'):
                genres[genre] = genres[genre] + 1 if genre in genres else 1
    except OSError:
        print('Error while reading file: ', fileName)
            
    plainFile.close()

    print('Genres and Movies per Genre')
    print('---------------------------')
    for key in genres:
        print(key, ' ',  genres[key])
        
    print('---------------------------')  
    print('Most popular Genre: ', max(genres, key=genres.get))
   
    
def main():
    getFileContentInfo('ml-latest-small/movies.csv')
    
if __name__ == "__main__":
    main()
