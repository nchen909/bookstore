from flask import Blueprint
from flask import request
from flask import jsonify,render_template
from be.model2 import user

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login", methods=["POST","GET"])
def login():
    if request.method=="POST":
        user_id = request.form.get("user_id", "")
        password = request.form.get("password", "")
        terminal = request.form.get("terminal", request.headers.get("User-Agent",""))#terminal如果不上传会默认设为User-Agent
        u = user.User()
        code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
        if code!=200:
            return render_template('login.html', user_id=user_id, password=password,result=str({"message": message, "token": token,"code":code}))
        else:
            return render_template('loginskip.html', user_id=user_id, password=password,result=str({"message": message, "token": token,"code":code}))
    elif request.method=="GET":
        return render_template('login.html')
        


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.form.get("user_id")
    token: str = request.headers.get("token")
    u = user.User()
    code, message = u.logout(user_id=user_id, token=token)
    if code != 200:
        return render_template('login.html', user_id=user_id,
                               result=str({"message": message,"code":code}))
    else:
        return render_template('loginskip.html', user_id=user_id,
                               result=str({"message": message,"code":code}))



@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.form.get("user_id", "")
    password = request.form.get("password", "")
    u = user.User()
    code, message = u.register(user_id=user_id, password=password)
    if code != 200:
        return render_template('login.html', user_id=user_id, password=password,
                               result=str({"message": message,"code":code}))
    else:
        return render_template('loginskip.html', user_id=user_id, password=password,
                               result=str({"message": message,"code":code}))


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

@bp_auth.route("/search_author", methods=["POST"])
def search_author():
    author = request.form.get("author", "")
    page = request.form.get("page", "")
    u = user.User()
    code, message = u.search_author(author=author, page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_book_intro", methods=["POST"])
def search_book_intro():
    book_intro = request.form.get("book_intro", "")
    page = request.form.get("page", "")
    u = user.User()
    code, message = u.search_book_intro(book_intro=book_intro, page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_tags", methods=["POST"])
def search_tags():
    tags = request.form.get("tags", "")
    page = request.form.get("page", "")
    u = user.User()
    code, message = u.search_tags(tags=tags, page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_title", methods=["POST"])
def search_title():
    title = request.form.get("title", "")
    page = request.form.get("page", "")
    u = user.User()
    code, message = u.search_title(title=title, page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_author_in_store", methods=["POST"])
def search_author_in_store():
    author = request.form.get("author", "")
    page = request.form.get("page", "")
    store_id = request.form.get("store_id", "")
    u = user.User()
    code, message = u.search_author_in_store(author=author,store_id=store_id,page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_book_intro_in_store", methods=["POST"])
def search_book_intro_in_store():
    book_intro = request.form.get("book_intro", "")
    page = request.form.get("page", "")
    store_id = request.form.get("store_id", "")
    u = user.User()
    code, message = u.search_book_intro_in_store(book_intro=book_intro, store_id=store_id,page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_tags_in_store", methods=["POST"])
def search_tags_in_store():
    tags = request.form.get("tags", "")
    page = request.form.get("page", "")
    store_id = request.form.get("store_id", "")
    u = user.User()
    code, message = u.search_tags_in_store(tags=tags, store_id=store_id,page=page)
    return jsonify({"message": message}), code
@bp_auth.route("/search_title_in_store", methods=["POST"])
def search_title_in_store():
    title = request.form.get("title", "")
    page = request.form.get("page", "")
    store_id = request.form.get("store_id", "")
    u = user.User()
    code, message = u.search_title_in_store(title=title,store_id=store_id, page=page)
    return jsonify({"message": message}), code

@bp_auth.route("/search_pic", methods=["POST"])
def search_pic():
    picture = request.files.get("picture","")
    page = request.form.get("page", "")
    u = user.User()
    code, message = u.search_pic(picture=picture, page=page)
    return jsonify({"message": message}), code


##游戏操作界面
@bp_auth.route("/operation/<string:user_id>", methods=['GET'])
def operation(user_id):
    return render_template('operation.html',user_id=user_id)

@bp_auth.route('/getjs', methods=['POST','GET'])
def get_js():
    if request.method == 'post':
        js_variable = request.form
        user_id = request.form.get("user_id", "")
        return jsonify(js_variable,user_id)
    else:
        return render_template('try2.html')