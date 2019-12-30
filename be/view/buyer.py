from flask import Blueprint, render_template
from flask import request
from flask import jsonify,redirect
from be.model2.buyer import Buyer
from be.model2.user import User
from be.model2 import error
import threading, multiprocessing
bp_buyer = Blueprint("buyer", __name__, url_prefix="/buyer")
import simplejson
import json

@bp_buyer.route("/new_order", methods=["POST"])
def new_order():
    # u=User()
    # user_id = request.form.get("user_id")
    # print("user_id;",user_id)
    # print("request.headers.get('token'):", request.headers.get("token"))
    # print("u.gettoken(user_id):",u.gettoken(user_id))
    # if request.headers.get("token")!=u.gettoken(user_id):
    #     return redirect('/auth/login')
    user_id: str = request.form.get("user_id")
    store_id: str = request.form.get("store_id")
    books=request.form.get("books").split("\n")
    for i in range(len(books)):
        a_=books[i].split(" ")
        if len(a_)==1:
            books[i]={"id":int(a_[0]),"count":1}
        elif len(a_)==2:
            books[i] = {"id": int(a_[0]), "count": int(a_[1])}
        else:
            code, mes = error.error_wrong_input()
            return code, mes
    id_and_count = []
    print(books)
    print(type(books))
    for book in books:
        book_id = book.get("id")
        count = book.get("count")
        id_and_count.append((book_id, count))

    b = Buyer()
    code, message, order_id = b.order(user_id, store_id, id_and_count)
    return render_template('operation.html',user_id=user_id,result={"message": message, "order_id": order_id,"code":code})


@bp_buyer.route("/payment", methods=["POST"])
def payment():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("user_id")
    order_id: str = request.form.get("order_id")
    password: str = request.form.get("password")
    b = Buyer()
    code, message = b.pay(user_id, password, order_id)
    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})


@bp_buyer.route("/add_funds", methods=["POST"])
def add_funds():
    u=User()
    user_id = request.form.get("user_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    password = request.form.get("password")
    add_value = int(request.form.get("add_value"))
    b = Buyer()
    code, message = b.add_money(user_id, password, add_value)
    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})

@bp_buyer.route("/receive_books", methods=["POST"])
def send_books():
    u=User()
    user_id = request.form.get("buyer_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("buyer_id")
    order_id: str = request.form.get("order_id")

    b = Buyer()
    code, message = b.receive_books(user_id, order_id)
    return render_template('operation.html', user_id=user_id,
                           result={"message": message, "code": code})

@bp_buyer.route("/search_order", methods=["POST"])
def search_order():
    u=User()
    user_id = request.form.get("buyer_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("buyer_id")

    b = Buyer()
    code, message,ret = b.search_order(user_id)
    print(json.dumps(ret))
    return render_template('operation.html',user_id=user_id,result={"message": message, "history record": ret,"code":code})

@bp_buyer.route("/cancel_order", methods=["POST"])
def cancel():
    u=User()
    user_id = request.form.get("buyer_id")
    if request.headers.get("token")!=u.gettoken(user_id):
        return redirect('/auth/login')
    user_id: str = request.form.get("buyer_id")
    order_id: str = request.form.get("order_id")
    b = Buyer()
    code, message = b.cancel(user_id,order_id)
    return render_template('operation.html',user_id=user_id,result={"message": message,"code":code})