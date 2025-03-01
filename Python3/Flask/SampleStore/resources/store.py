import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

from schemas import ItemSchema, ItemUpdateSchema, StoreSchema

blp = Blueprint("stores", __name__, description="OPeration on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return ({"stores": list(stores.values())}, 200)

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store deleted"}
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return list(stores.values())

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, request_data):
        # request_data = request.get_json()

        # if "name" not in request_data:
        #     abort(
        #         400,
        #         message="Bad Request, Ensure 'name' is included"
        #     )

        for store in stores.values():
            if request_data["name"] == store["name"]:
                abort(400, message=f"Store Already exists.")

        store_id = uuid.uuid4().hex

        new_store = {**request_data, "id": store_id}
        stores[store_id] = new_store
        return (new_store, 200)

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message="item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()

        # if "price" not in item_data or "name" not in item_data:
        #     abort(400, message="Bad Request, Price and Name required")

        try:
            item = items[item_id]
            # Replace any fields coming in from the request.
            item |= item_data
            return item
        except KeyError:
            abort(400, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, request_data):
        # request_data = request.get_json()

        # if (
        #         "price" not in request_data
        #         or "store_id" not in request_data
        #         or "name" not in request_data
        # ):
        #     abort(400,
        #           message="Bad request, ensure all fields are included")

        for item in items.values():
            if (
                    request_data["name"] == item["name"]
                    and request_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists")

        if request_data["store_id"] not in stores:
            abort(404, message="Store not found")

        item_id = uuid.uuid4().hex
        item = {**request_data, "id": item_id}
        items[item_id] = item

        return (item, 201)

