from flask import Blueprint
from flask import request
from flask import jsonify, render_template
from be.model2 import user
from be.model2.user import User
from be.model2 import error
from .search_func import *
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        password = request.form.get("password", "")
        terminal = request.form.get("terminal", request.headers.get("User-Agent", ""))  # terminal如果不上传会默认设为User-Agent
        u = user.User()
        code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
        if code != 200:
            return render_template('login.html', user_id=user_id, password=password,
                                   result=str({"message": message, "token": token, "code": code}))
        else:
            return render_template('loginskip.html', user_id=user_id, password=password,
                                   result=str({"message": message, "token": token, "code": code}))
    elif request.method == "GET":
        return render_template('login.html')


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.form.get("user_id")
    u = User()
    # token: str = request.headers.get("token")
    token: str = u.gettoken(user_id)
    u = user.User()
    code, message = u.logout(user_id=user_id, token=token)
    if code != 200:
        return render_template('operation.html', user_id=user_id, result={"message": message, "code": code})
    else:
        return render_template('login.html')


@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.form.get("user_id", "")
    password = request.form.get("password", "")
    u = user.User()
    code, message = u.register(user_id=user_id, password=password)
    if code != 200:
        return render_template('login.html', user_id=user_id, password=password,
                               result=str({"message": message, "code": code}))
    else:
        return render_template('loginskip.html', user_id=user_id, password=password,
                               result=str({"message": message, "code": code}))


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    user_id = request.form.get("user_id", "")
    password = request.form.get("password", "")
    u = user.User()
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/password", methods=["POST"])
def change_password():
    user_id = request.form.get("user_id", "")
    old_password = request.form.get("oldPassword", "")
    new_password = request.form.get("newPassword", "")
    u = user.User()
    code, message = u.change_password(user_id=user_id, old_password=old_password, new_password=new_password)
    return jsonify({"message": message}), code


@bp_auth.route("/search_pic", methods=["POST"])
def search_pic():
    from PIL import Image, ImageFile
    picture = request.files["picture"] if request.files.get('picture') else None
    if not picture:
        code, mes = error.error_wrong_input()
        return jsonify({"message": mes}), code
    # picture=Image.open(picture)
    print(type(picture))
    print(type(request.files["picture"]))
    page = request.form.get("page", 1)
    page = 1 if not page else int(page)
    u = user.User()
    code, message = u.search_pic(picture=picture, page=page)
    print(picture)
    print(page)
    print(code)
    print(message)
    return render_template('search.html',
                                   result=str({"message": message, "code": code}))

@bp_auth.route("/search_title_store_id/<string:title>", methods=["GET"])
def search_title_store_id(title):
    print("title:xxxxxxxxxx",title)
    u = user.User()
    code, message = u.search_title_store_id(title=title)
    print(code)
    print(message)
    return render_template('search.html',
                                   result=str({"message": message, "code": code}))

##游戏操作界面
@bp_auth.route("/operation/<string:user_id>", methods=['GET'])
def operation(user_id):
    return render_template('operation.html', user_id=user_id)


@bp_auth.route('/getjs', methods=['POST', 'GET'])
def get_js():
    if request.method == 'post':
        js_variable = request.form
        user_id = request.form.get("user_id", "")
        return jsonify(js_variable, user_id)
    else:
        return render_template('try2.html')


@bp_auth.route("/search_all", methods=["POST"])
def search_all():
    isstore = request.values.getlist("istore")
    store_id = request.form.get("store_id")
    print("isstore:", isstore)
    page = request.form.get("page", 1)
    page = 1 if not page else int(page)
    print("page:", page)
    button = request.values.get("button")
    if not (page):
        code, mes = error.error_wrong_input()
        return jsonify({"message": mes}), code
    if not (isstore):  # 全文搜索
        if (button=="author"):
            author = request.form.get("author")
            print("author:", author)
            if not (author):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_author(author, page)
        elif (button=="book_intro"):
            book_intro = request.form.get("book_intro")
            if not (book_intro):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_book_intro(book_intro, page)
        elif (button=="tags"):
            tags = request.form.get("tags")
            if not (tags):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_tags(tags, page)
        elif (button=="title"):
            title = request.form.get("title")
            if not (title):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_title(title, page)
        else:
            code, mes = error.error_wrong_input()
            return jsonify({"message": mes}), code
    else:  # 店内搜索
        if not (store_id):
            code, mes = error.error_wrong_input()
            return jsonify({"message": mes}), code
        if (button=="author"):
            author = request.form.get("author")
            if not (author):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_author_in_store(author, page,store_id)
        elif (button=="book_intro"):
            book_intro = request.form.get("book_intro")
            if not (book_intro):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_book_intro_in_store(book_intro, page,store_id)
        elif (button=="tags"):
            tags = request.form.get("tags")
            if not (tags):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_tags_in_store(tags, page,store_id)
        elif (button=="title"):
            title = request.form.get("title")
            if not (title):
                code, mes = error.error_wrong_input()
                return jsonify({"message": mes}), code
            else:
                return search_title_in_store(title, page,store_id)
        else:
            code, mes = error.error_wrong_input()
            return jsonify({"message": mes}), code
    # u = user.User()
    # code, message = u.search_pic(picture=picture, page=page)
    # code, message = [1, 2]
    # return jsonify({"message": message}), code
