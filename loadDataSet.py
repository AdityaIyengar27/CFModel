import csv
from surprise import Dataset, Reader
from random import choice

bastPathForData = '/Users/adityaiyengar/Desktop/Desktop/Netflix task - Preteek/ml-latest-small/'

class dataReader:
    def __init__(self):
        self.users = []
        self.movieFileName = self.setMovieFileName()
        self.ratingFileName = self.setRatingFileName()
        self.movieId_to_name = {}
        self.name_to_movieId = {}
        self.loadMovies()
        self.returnAllUsers()

    def loadMovies(self):
        if self.movieFileName is None:
            self.movieFileName = self.setMovieFileName()
        with open(self.movieFileName) as csvFile:
            movieReader = csv.reader(csvFile)
            next(movieReader) # Skip header line
            for movies in movieReader:
                movieId = int(movies[0])
                movieName = movies[1]
                self.movieId_to_name[movieId] = movieName
                self.name_to_movieId[movieName] = movieId

    def returnAllUsers(self):
        if self.ratingFileName is None:
            self.ratingFileName = self.setRatingFileName()
        with open(self.ratingFileName) as csvFile:
            ratingReader = csv.reader(csvFile)
            next(ratingReader)
            for ratingRow in ratingReader:
                if not int(ratingRow[0]) in self.users:
                    self.users.append(int(ratingRow[0]))
        return self.users

    def setRatingFileName(self):
        self.ratingFileName = bastPathForData + 'ratings.csv'
        return self.ratingFileName

    def setMovieFileName(self):
        self.movieFileName = bastPathForData + 'movies.csv'
        return self.movieFileName

    # def userRating(self, user):
    #     for ratingRow in self.ratingReader:
    #         userId = int(ratingRow[0])
    #         movieId = int(ratingRow[1])
    #         rating = ratingRow[2]

    def loadRatingUsingSurprise(self):
        if self.ratingFileName is None:
            self.ratingFileName = self.setRatingFileName()
        reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)
        ratingsDataset = Dataset.load_from_file(self.ratingFileName, reader=reader)
        return ratingsDataset

    # def returnAllUsers(self):
    #     for ratingRow in self.ratingReader:
    #         if not int(ratingRow[0]) in self.users:
    #             self.users.append(int(ratingRow[0]))
    #     return self.users

    def returnRandomUser(self):
        if len(self.users) == 0:
            self.returnAllUsers()
        return choice(self.users)

    def getMovieName(self, movieId):
        if not self.movieId_to_name:
            self.loadMovies()
        if movieId in self.movieId_to_name:
            return self.movieId_to_name[movieId]