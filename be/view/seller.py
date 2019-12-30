from flask import Blueprint, render_template
from flask import request,redirect
from flask import jsonify
from be.model2 import seller
from be.model2.user import User
import json

bp_seller = Blueprint("seller", __name__, url_prefix="/seller")


@bp_seller.route("/create_store", methods=["POST"])
def seller_create_store():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("user_id")
    store_id: str = request.form.get("store_id")
    s = seller.Seller()
    code, message = s.create_store(user_id, store_id)
    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})


@bp_seller.route("/add_book", methods=["POST"])
def seller_add_book():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("user_id")
    store_id: str = request.form.get("store_id")
    book_info: str = request.form.get("book_info")
    stock_level: str = request.form.get("stock_level", 0)

    s = seller.Seller()
    code, message = s.add_book(user_id, store_id, book_info.get("id"),book_info.get("price"), json.dumps(book_info), stock_level)

    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})


@bp_seller.route("/add_stock_level", methods=["POST"])
def add_stock_level():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("user_id")
    store_id: str = request.form.get("store_id")
    book_id: str = request.form.get("book_id")
    add_num: str = request.form.get("add_stock_level", 0)

    s = seller.Seller()
    code, message = s.add_stock_level(user_id, store_id, book_id, add_num)

    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})

@bp_seller.route("/send_books", methods=["POST"])
def send_books():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("seller_id")
    order_id: str = request.form.get("order_id")

    s = seller.Seller()
    code, message = s.send_books(user_id, order_id)

    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})