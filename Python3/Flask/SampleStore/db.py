from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

stores = {
    "1" : {
        "name": "My Store",
        "items": [
            {
                "name": 'Chair',
                "price": 16.99
            }
        ]
    }
}

items = {

}