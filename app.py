from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY, TIMESTAMP
from sqlalchemy import ForeignKeyConstraint
import os
import numpy as np
from scipy.spatial.distance import cosine
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY, TIMESTAMP
import os
import numpy as np
from scipy.spatial.distance import cosine
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class AspNetUsers(db.Model):
    __tablename__ = 'AspNetUsers'

    Id = db.Column(db.Text, primary_key=True)
    DisplayName = db.Column(db.String(50), nullable=False)

class Dishes(db.Model):
    __tablename__ = "Dishes"
    
    Id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Name = db.Column(db.String(32), nullable=False)

class DishReview(db.Model):
    __tablename__ = "DishReview"
    
    Id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    DishId = db.Column(PG_UUID(as_uuid=True), db.ForeignKey("Dishes.Id", ondelete="CASCADE"), nullable=False)
    Rating = db.Column(db.Integer, nullable=False, default=0)
    UserId = db.Column(db.String(128), db.ForeignKey("AspNetUsers.Id", ondelete="CASCADE"), nullable=False, default='')

class Restaurants(db.Model):
    __tablename__ = "Restaurants"
    
    Id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Name = db.Column(db.String(128), nullable=False)
    HeadId = db.Column(db.String(128), nullable=False)

class RestaurantReviews(db.Model):
    __tablename__ = "RestaurantReviews"
    
    Id = db.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    RestaurantId = db.Column(PG_UUID(as_uuid=True), db.ForeignKey("Restaurants.Id", ondelete="CASCADE"), nullable=False)
    UserId = db.Column(db.String(128), db.ForeignKey("AspNetUsers.Id", ondelete="CASCADE"), nullable=False)
    Rating = db.Column(db.Integer, nullable=False)

def prepare_rating_data(users, items, reviews,type='dish'):
    # Create user and item lists
    user_list = [user['id'] for user in users]
    item_list = [item['id'] for item in items]
    
    # Create ratings dictionary
    ratings_dict = {}
    for user in users:
        ratings_dict[user['id']] = {}
    
    # Populate ratings
    if type == 'dish':
        for review in reviews:
            user_id = review['userId']
            item_id = review['dishId']  # or restaurantId depending on context
            rating = review['rating']
            if user_id in ratings_dict:
                ratings_dict[user_id][item_id] = rating
    else:
        for review in reviews:
            user_id = review['userId']
            item_id = review['restaurantId']
            rating = review['rating']
            if user_id in ratings_dict:
                ratings_dict[user_id][item_id] = rating
            
    return user_list, item_list, ratings_dict

def get_user_item_matrix(user_list, item_list, item_ratings):
    matrix = np.zeros((len(user_list), len(item_list)))
    for user, user_ratings in item_ratings.items():
        user_idx = user_list.index(user)
        for item, rating in user_ratings.items():
            item_idx = item_list.index(item)
            matrix[user_idx, item_idx] = rating
    return matrix

def get_recommended_items(user_id, user_list, item_list, item_ratings, k=3):
    user_item_matrix = get_user_item_matrix(user_list, item_list, item_ratings)

    user_idx = user_list.index(user_id)

    if np.sum(user_item_matrix[user_idx]) == 0:
        average_ratings = np.mean(user_item_matrix, axis=0)
        recommended_items = [(item_list[item_idx], average_ratings[item_idx]) for item_idx in range(len(item_list))]
        recommended_items.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in recommended_items[:k]]

    user_similarities = [1 - cosine(user_item_matrix[user_idx], user_item_matrix[i]) for i in range(len(user_list))]

    similar_users = np.argsort(user_similarities)[::-1][1:k+1]

    recommended_items = []
    for item_idx in range(len(item_list)):
        if item_list[item_idx] not in item_ratings[user_id]:
            item_ratings_sum = sum(user_item_matrix[similar_user_idx][item_idx] for similar_user_idx in similar_users)
            recommended_items.append((item_list[item_idx], item_ratings_sum))

    recommended_items.sort(key=lambda x: x[1], reverse=True)

    return [item[0] for item in recommended_items[:k]]    


    
@app.route('/')
def hello():
	return {"hello": "world"}

@app.route('/models', methods=['GET'])
def test_models():
    users = AspNetUsers.query.all()
    dishes = Dishes.query.all()
    dish_reviews = DishReview.query.all()
    restaurants = Restaurants.query.all()
    restaurant_reviews = RestaurantReviews.query.all()
    return jsonify({
        "users": [{"id": user.Id, "displayName": user.DisplayName} for user in users],
        "dishes": [{"id": dish.Id, "name": dish.Name} for dish in dishes],
        "dishReviews": [{"id": review.Id, "dishId": review.DishId, "rating": review.Rating, "userId": review.UserId} for review in dish_reviews],
        "restaurants": [{"id": restaurant.Id, "name": restaurant.Name, "headId": restaurant.HeadId} for restaurant in restaurants],
        "restaurantReviews": [{"id": review.Id, "restaurantId": review.RestaurantId, "userId": review.UserId, "rating": review.Rating} for review in restaurant_reviews]
    })

@app.route('/recommended-dishes', methods=['GET'])
def recommend_dishes():
    user_id = request.args.get('userId', type=str)
    n = request.args.get('n', default=10, type=int) 
    users = AspNetUsers.query.all()
    dishes = Dishes.query.all()
    dish_reviews = DishReview.query.all()
    users_data = [{"id": user.Id, "displayName": user.DisplayName} for user in users]
    dishes_data = [{"id": str(dish.Id), "name": dish.Name} for dish in dishes]
    reviews_data = [{"id": str(review.Id), "dishId": str(review.DishId), 
                    "rating": review.Rating, "userId": review.UserId} 
                   for review in dish_reviews]
    
    # Prepare data for recommendation
    user_list, item_list, ratings_dict = prepare_rating_data(users_data, dishes_data, reviews_data)
    
    # Get recommendations
    recommended_dish_ids = get_recommended_items(user_id, user_list, item_list, ratings_dict, n)
    
    return jsonify(recommended_dish_ids)

@app.route('/recommended-restaurants', methods=['GET'])
def recommend_restaurants():
    user_id = request.args.get('userId', type=str)
    n = request.args.get('n', default=10, type=int) 
    users = AspNetUsers.query.all()
    restaurants = Restaurants.query.all()
    restaurant_reviews = RestaurantReviews.query.all()
    users_data = [{"id": user.Id, "displayName": user.DisplayName} for user in users]
    restaurants_data = [{"id": str(restaurant.Id), "name": restaurant.Name} 
                       for restaurant in restaurants]
    reviews_data = [{"id": str(review.Id), "dishId": str(review.RestaurantId), 
                    "rating": review.Rating, "userId": review.UserId} 
                   for review in restaurant_reviews]
    
    # Prepare data for recommendation
    user_list, item_list, ratings_dict = prepare_rating_data(users_data, restaurants_data, reviews_data)
    
    # Get recommendations
    recommended_restaurant_ids = get_recommended_items(user_id, user_list, item_list, ratings_dict, n)
    
    return jsonify(recommended_restaurant_ids)