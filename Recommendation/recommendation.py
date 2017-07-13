"""
    This uses ratings data and trust data to make a recommendation
    Memory Based Colloborative Filtering
    User Item Colloborative Filtering
    rating data is in the format
    userid, productid, categoryid, rating, helpfulness, timestamp    
"""

from scipy.spatial.distance import hamming
import numpy as np
import pandas as pan

def distance(user1, user2):
    user1Ratings = userProductRatingMatrix.transpose()[user1]
    user2Ratings = userProductRatingMatrix.transpose()[user2]
    return hamming(user1Ratings, user2Ratings)

def nearestNeighbours(user,K=10):
    allUsers = pan.DataFrame(userProductRatingMatrix.index)
    allUsers = allUsers[allUsers.user!=user]
    allUsers["distance"] = allUsers["user"].apply(lambda user2: distance(user, user2))
    kNearestUsers = allUsers.sort_values(["distance"], ascending=True)["user"][:K]
    return kNearestUsers

RATING_MATRIX_FILE = "./data/rating-sample.txt"
ratings_df = pan.read_csv(RATING_MATRIX_FILE, sep=' ', names=['user', 'productids', 'category', 'rating', 'helpfulness', 'timestamp'])
#ratings_df["catprod"] = ratings_df["category"].map(str) + "-" + ratings_df["product"].map(str)

users = ratings_df.user.value_counts()
products = ratings_df.productids.value_counts()
print('Number of users = ' + str(users.shape) + ' | Number of products = ' + str(products.shape))

userProductRatingMatrix = pan.pivot_table(ratings_df, values='rating', index=['user'], columns=['productids'])

user = 2
KNearestNeighbours = nearestNeighbours(user)
NearestNeighbourRatings = userProductRatingMatrix[userProductRatingMatrix.index[KNearestNeighbours]]
avgRating = NearestNeighbourRatings.apply(np.nanmean).dropna()

productsAlreadyRated = userProductRatingMatrix.transpose()[user].dropna().index

#remove average rating for products already rated by user
#avgRating = avgRating[-avgRating.index[productsAlreadyRated]]

TopNProducts = 10
topNCatProds = avgRating.sort_values(ascending=False).index[:TopNProducts]
print(topNCatProds.values)
