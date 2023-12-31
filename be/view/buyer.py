from flask import Blueprint
from flask import request
from flask import jsonify
from be.model.buyer import Buyer

bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")


@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    data = request.get_json(silent=True) or {}
    user_id: str = data.get("user_id")
    store_id: str = data.get("store_id")
    books: [] = data.get("books")
    id_and_count = []
    for book in books:
        book_id = book.get("id")
        count = book.get("count")
        id_and_count.append((book_id, count))

    b = Buyer()
    code, message, order_id = b.new_order(user_id, store_id, id_and_count)
    return jsonify({"message": message, "order_id": order_id}), code


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    data = request.get_json(silent=True) or {}
    user_id: str = data.get("user_id")
    order_id: str = data.get("order_id")
    password: str = data.get("password")
    b = Buyer()
    b.delete_order_time()
    code, message = b.payment(user_id, password, order_id)
    return jsonify({"message": message}), code


@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    password = data.get("password")
    add_value = data.get("add_value")
    b = Buyer()
    code, message = b.add_funds(user_id, password, add_value)
    return jsonify({"message": message}), code

@bp_buyer.route("/search_global", methods=['POST'])
def search():
    data = request.get_json(silent=True) or {}
    key = data.get('key')
    pageIndex = data.get('pageIndex', 1)
    pageSize = data.get('pageSize', 5)
    b = Buyer()
    code, message, result = b.search_global(key, pageIndex, pageSize)
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/search_store", methods=['POST'])
def search_store():
    data = request.get_json(silent=True) or {}
    key = data.get('key')
    store_id = data.get('store_id')
    pageIndex = data.get('pageIndex', 1)
    pageSize = data.get('pageSize', 5)
    b = Buyer()
    code, message, result = b.search_store(key, store_id, pageIndex, pageSize)
    return jsonify({"message": message, "result": result}), code

@bp_buyer.route("/receive", methods=["POST"])
def receive():
    data = request.get_json(silent=True) or {}
    user_id: str = data.get("user_id")
    order_id: str = data.get("order_id")
    token: str = request.headers.get("token")
    b = Buyer()
    code, message = b.receive(user_id, order_id, token)
    return jsonify({"message": message}), code

@bp_buyer.route("/search_order", methods=["POST"])
def search_order():
    data = request.get_json(silent=True) or {}
    user_id: str = data.get("buyer_id")
    search_state: int = data.get("search_state")
    b = Buyer()
    code, message, results = b.search_order(user_id, search_state)
    return jsonify({"message": message, "results": results}), code


@bp_buyer.route("/delete_order", methods=["POST"])
def delete_order():
    data = request.get_json(silent=True) or {}
    user_id: str = data.get("user_id")
    order_id: str = data.get("order_id")
    b = Buyer()
    code, message = b.delete_order(user_id, order_id)
    return jsonify({"message": message}), code