from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests
from tensorflow.keras.applications import InceptionV3
import tensorflow as tf
# from tf.keras.applications import InceptionV3

app = Flask(__name__)

api = Api(app)

# Init Mongo Client
client = MongoClient("mongodb://sandbox:Fuckthisplace$01@mongo.statninja.net:27017")
db = client.sandbox
users = db['users']

def user_exists(username):
    if users.count_documents({"username": username}) == 0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        # Get the post data
        data = request.get_json()

        # Get username and password
        username = data['username']
        password = data['password']

        # check if user already exists
        if user_exists(username):
            return jsonify({
                "status": 301,
                'message': "Invalid username, user already exists"
            })
        # if user is new has passwword
        hashed = bcrypt.hashpw(password.encone('utf8'), bcrypt.gensalt())
        # store user in database
        users.insert_one({
            'username': username,
            'password':hashed,
            'token': 4
        })
        # return success
        return jsonify({
            "status":200,
            "message": "Succesfully Registered"
        })


api.add_resource(Resource, '/register')