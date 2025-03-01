import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blp = Blueprint("stores", __name__, description="OPeration on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
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
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        request_data = request.get_json()

        if "name" not in request_data:
            abort(
                400,
                message="Bad Request, Ensure 'name' is included"
            )

        for store in stores.values():
            if request_data["name"] == store["name"]:
                abort(400, message=f"Store Already exists.")

        store_id = uuid.uuid4().hex

        new_store = {**request_data, "id": store_id}
        stores[store_id] = new_store
        return (new_store, 200)

@blp.route("/item/<string:item_id>")
class Item(MethodView):
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

    def put(self, item_id):
        item_data = request.get_json()

        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad Request, Price and Name required")

        try:
            item = items[item_id]
            # Replace any fields coming in from the request.
            item |= item_data
            return item
        except KeyError:
            abort(400, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        request_data = request.get_json()

        if (
                "price" not in request_data
                or "store_id" not in request_data
                or "name" not in request_data
        ):
            abort(400,
                  message="Bad request, ensure all fields are included")

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

