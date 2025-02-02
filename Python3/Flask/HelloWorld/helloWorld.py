from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://sandbox:Fuckthisplace$01@mongo.statninja.net:27017")
db = client.sandbox
UserNum = db['UserNum']
UserNum.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num+1;
        UserNum.update_one({}, {"$set": {"num_of_users": new_num}})
        return str("hello user" + str(new_num));


# Rest Model with the basic Crud Operations
class Add(Resource):
    def post(self):
        # fim ih ere, thene the resour add was requested using post
        # Get posted data
        postedData = request.get_json()
        x = int(postedData['x'])
        y =  int(postedData['y'])

        respMap = {
            'sum': x +y,
            'status': 200
        }
        return jsonify(respMap)

    def get(self):
        return ""

    def put(self):
        return ""

    def delete(self):
        return ""


class Subtract(Resource):
    pass

class Divide(Resource):
    pass


api.add_resource(Add, '/add')
api.add_resource(Visit, '/visit')


@app.route('/')
def hello_world():
    return "hello World"

if __name__ == '__main__':
    app.run()