from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np
from scipy.spatial.distance import cosine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class AspNetUsers(db.Model):
    __tablename__ = 'AspNetUsers'

    Id = db.Column(db.Text, primary_key=True)
    DisplayName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(256))



user_list = ['user1', 'user2', 'user3', 'user4','user5','user6','user7']
dish_list = ['dish1', 'dish2', 'dish3', 'dish4', 'dish5','dish6','dish7','dish8','dish9','dish10']
dish_ratings = {
    'user1': {'dish1': 4, 'dish2': 3, 'dish3': 5},
    'user2': {'dish1': 3, 'dish10': 4, 'dish5': 2},
    'user3': {'dish2': 4, 'dish9': 3, 'dish4': 5},
    'user4': {'dish1': 5, 'dish4': 3, 'dish5': 4}
}

def get_user_item_matrix(user_list, dish_list, dish_ratings):
    matrix = np.zeros((len(user_list), len(dish_list)))
    for user, user_ratings in dish_ratings.items():
        user_idx = user_list.index(user)
        for dish, rating in user_ratings.items():
            dish_idx = dish_list.index(dish)
            matrix[user_idx, dish_idx] = rating
    return matrix

def get_recommended_dishes(user_id, user_list, dish_list, dish_ratings, k=3):
    user_item_matrix = get_user_item_matrix(user_list, dish_list, dish_ratings)

    user_idx = user_list.index(user_id)

    if np.sum(user_item_matrix[user_idx]) == 0:
        average_ratings = np.mean(user_item_matrix, axis=0)
        recommended_dishes = [(dish_list[dish_idx], average_ratings[dish_idx]) for dish_idx in range(len(dish_list))]
        recommended_dishes.sort(key=lambda x: x[1], reverse=True)
        return [dish[0] for dish in recommended_dishes[:k]]  # Ensure only top k dishes are returned

    user_similarities = [1 - cosine(user_item_matrix[user_idx], user_item_matrix[i]) for i in range(len(user_list))]

    similar_users = np.argsort(user_similarities)[::-1][1:k+1]

    recommended_dishes = []
    for dish_idx in range(len(dish_list)):
        if dish_list[dish_idx] not in dish_ratings[user_id]:
            dish_ratings_sum = sum(user_item_matrix[similar_user_idx][dish_idx] for similar_user_idx in similar_users)
            recommended_dishes.append((dish_list[dish_idx], dish_ratings_sum))

    recommended_dishes.sort(key=lambda x: x[1], reverse=True)

    return [dish[0] for dish in recommended_dishes[:k]]    
    
@app.route('/')
def hello():
	return {"hello": "world"}

@app.route('/dish-recommended', methods=['GET'])
def recommend_dishes():
    user_id = request.args.get('userId', type=str)
    n = request.args.get('n', default=5, type=int) 

    recommended_dishes = get_recommended_dishes(user_id, user_list, dish_list, dish_ratings, n)

    return jsonify(recommended_dishes)