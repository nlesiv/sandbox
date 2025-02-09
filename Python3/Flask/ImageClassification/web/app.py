from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO;
app = Flask(__name__)

api = Api(app)

# load the pretrained model
pretrained_model = InceptionV3(weights="imagenet")

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


def generate_return_dictionary(status, msg):
    ret_json = {
        'status': status,
        'message': msg

    }
    return ret_json

class Classify(Resource):
    def post(self):
        # get posted data
        data = request.get_json()

        #get credentials and url
        url = data['url']


        #verify credentials

        #check if user has tokens

        # classify image _check url
        if not url:
            return jsonify(({'error': 'no URL provide'}), 400)
        
        # load image from URL
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # preprocess image
        img = img.resize((299, 299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # make prediction
        prediction = pretrained_model.predict(img_array)
        actual_prediction = imagenet_utils.decode_predictions(prediction, top=5)

        ret_json = {}
        for pred in actual_prediction[0]:
            print(pred)
            ret_json[pred[1]] = float(pred[2]*100)

        # users.update_one
        return ret_json



api.add_resource(Resource, '/register')
api.add_resource(Classify, '/classify')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8081")



