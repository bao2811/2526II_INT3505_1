from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument

from db import get_products_collection


def _product_to_response(product_doc):
    return {
        "id": str(product_doc["_id"]),
        "name": product_doc["name"],
        "description": product_doc.get("description", ""),
        "price": product_doc["price"],
        "inStock": product_doc.get("inStock", True),
    }


def get_products():
    collection = get_products_collection()
    products = [_product_to_response(doc) for doc in collection.find()]
    return products, 200


def get_product_by_id(product_id):
    collection = get_products_collection()
    try:
        oid = ObjectId(product_id)
    except InvalidId:
        return {"message": "Invalid product id."}, 400

    product_doc = collection.find_one({"_id": oid})
    if not product_doc:
        return {"message": "Product not found."}, 404

    return _product_to_response(product_doc), 200


def create_product(body):
    collection = get_products_collection()
    product = body or {}

    payload = {
        "name": product["name"],
        "description": product.get("description", ""),
        "price": product["price"],
        "inStock": product.get("inStock", True),
    }

    result = collection.insert_one(payload)
    created = collection.find_one({"_id": result.inserted_id})
    return _product_to_response(created), 201


def update_product(product_id, body):
    collection = get_products_collection()

    product = body or {}

    try:
        oid = ObjectId(product_id)
    except InvalidId:
        return {"message": "Invalid product id."}, 400

    update_fields = {}
    for key in ["name", "description", "price", "inStock"]:
        if key in product:
            update_fields[key] = product[key]

    if not update_fields:
        return {"message": "No fields provided for update."}, 400

    updated = collection.find_one_and_update(
        {"_id": oid},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER,
    )

    if not updated:
        return {"message": "Product not found."}, 404

    return _product_to_response(updated), 200


def delete_product(product_id):
    collection = get_products_collection()

    try:
        oid = ObjectId(product_id)
    except InvalidId:
        return {"message": "Invalid product id."}, 400

    result = collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        return {"message": "Product not found."}, 404

    return "", 204
