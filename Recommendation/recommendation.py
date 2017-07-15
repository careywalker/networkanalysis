"""
    This uses ratings data and trust data to make a recommendation
    Memory Based Colloborative Filtering
    User Item Colloborative Filtering
    rating data is in the format
    userid, productid, categoryid, rating, helpfulness, timestamp
"""

import warnings
from scipy.spatial.distance import hamming
import numpy as np
import pandas as pan
import networkx as nx
import threading as th

#for trust data, give all trusted people a distance of 2 to put them in front
#read in the trust data as a graph which will allow checking if two nodes have an edge
import networkx as nx

trustdata=pan.read_csv('data/trust.txt',sep=" ",header=0,names=['node1', 'node2', 'timestamp'])
G = nx.from_pandas_dataframe(trustdata, 'node1', 'node2')
nx.info(G)

#a simple check to see if there is an edge between two nodes
def distance(user1, user2, usetrust=False):
    if usetrust:
        if G.has_edge(user1, user2):
            return 2
        else:
            user1Ratings = userProductRatingMatrix.transpose()[user1]
            user2Ratings = userProductRatingMatrix.transpose()[user2]
            return hamming(user1Ratings, user2Ratings)
    else:
        user1Ratings = userProductRatingMatrix.transpose()[user1]
        user2Ratings = userProductRatingMatrix.transpose()[user2]
        return hamming(user1Ratings, user2Ratings)

def nearestNeighbours(user,K=10,usetrust=False):
    allUsers = pan.DataFrame(userProductRatingMatrix.index)
    allUsers = allUsers[allUsers.user!=user]
    allUsers["distance"] = allUsers["user"].apply(lambda user2: distance(user, user2, usetrust))
    kNearestUsers = allUsers.sort_values(["distance"], ascending=True)["user"][:K]
    return kNearestUsers

def getTopNProductsPerUser(user, K=10, usetrust=False):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        KNearestNeighbours = nearestNeighbours(user, K, usetrust)
        NearestNeighbourRatings = userProductRatingMatrix[userProductRatingMatrix.index.isin(KNearestNeighbours)]
        avgRating = NearestNeighbourRatings.apply(np.nanmean).dropna()
        productsAlreadyRated = userProductRatingMatrix.transpose()[user].dropna().index
        #remove average rating for products already rated by user
        avgRating = avgRating[-avgRating.index.isin(productsAlreadyRated)]
        cummulative_rating = avgRating.sort_values(ascending=False)[:(K*K*K)].sum()
        topNCatProds = avgRating.sort_values(ascending=False).index[:K]
    return topNCatProds, cummulative_rating

def dowork(userid, topn, usetrust):
    #print(user)
    products, cummulative_rating = getTopNProductsPerUser(userid, topn, usetrust)
    print('User Id: ' + repr(userid) + " || Recommended Products : " + ', '.join([str(product) for product in products.values]) + " || Rating : " + str(cummulative_rating))

RATING_MATRIX_FILE = "./data/rating.txt"
ratings_df = pan.read_csv(RATING_MATRIX_FILE, sep=' ', names=['user', 'productids', 'category', 'rating', 'helpfulness', 'timestamp'])
#ratings_df["catprod"] = ratings_df["category"].map(str) + "-" + ratings_df["product"].map(str)

users = ratings_df.user.value_counts()
products = ratings_df.productids.value_counts()
print('Number of users = ' + str(users.shape) + ' | Number of products = ' + str(products.shape))

usersPerProduct = ratings_df.productids.value_counts()
productsPerUser = ratings_df.user.value_counts()
ratings_df = ratings_df[ratings_df["productids"].isin(usersPerProduct[usersPerProduct>10].index)]
userProductRatingMatrix = pan.pivot_table(ratings_df, values='rating', index=['user'], columns=['productids'])

#userid = 144
topn = 10
usetrust = True

threads = []
print("With Trust = ", usetrust)
for row in userProductRatingMatrix.head(10).itertuples():
    #t = th.Thread(target=dowork, args=(row[0], topn, usetrust))
    #threads.append(t)
    #t.start()
    #th._start_new_thread(dowork, (row[0], topn, usetrust))
    dowork(row[0], topn, usetrust)
    #print(row[0])

usetrust = False
print("With Trust = ", usetrust)
for row in userProductRatingMatrix.head(10).itertuples():
    dowork(row[0], topn, usetrust)