import heapq
from collections import defaultdict
from operator import itemgetter
from loadDataSet import dataReader
from surprise import KNNBasic
from prettytable import PrettyTable

def suggestSimilarMovies():
    MovieLens = dataReader()
    ratingData = MovieLens.loadRatingUsingSurprise()
    trainingData = ratingData.build_full_trainset()

    sim_options = {'name': 'cosine', 'user_based': True}

    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset=trainingData)
    simMatrix = model.compute_similarities()

    # testUserId = '464'
    # testUser = trainingData.to_inner_uid(testUserId)

    testUserId = None
    testUser = None
    while testUserId is None:
        try:
            testUserId = MovieLens.returnRandomUser()
            testUser = trainingData.to_inner_uid(str(testUserId))
        except:
            pass

    similarityRow = simMatrix[testUser]

    similarUsers = []
    for id, score in enumerate(similarityRow):
        if id != testUser:
            similarUsers.append((id,score) )

    kNeighbours = heapq.nlargest(10, similarUsers, key=lambda t: t[1])

    candidates = defaultdict(float)

    for similarUser in kNeighbours:
        id = similarUser[0]
        userSimilarityScore = similarUser[1]
        theirRatings = trainingData.ur[id]
        for rating in theirRatings:
            candidates[rating[0]] += (rating[1] / 5.0) * userSimilarityScore

    watched = {}
    for itemID, rating in trainingData.ur[testUser]:
        watched[itemID] = 1

    print()
    print("Based on similar users, computing top rated movies to user : {0}".format(testUserId))
    print()
    prettyTable = PrettyTable(['Movie', 'Average Rating'])
    pos = 0
    for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
        if not itemID in watched:
            movieID = trainingData.to_raw_iid(itemID)
            prettyTable.add_row([MovieLens.getMovieName(int(movieID)), ratingSum])
            pos += 1
            if pos > 10:
                break

    print(prettyTable)