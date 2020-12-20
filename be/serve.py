import logging
import os
from flask import Flask
from flask import Blueprint
from flask import request
from be.view import auth
from be.view import seller
from be.view import buyer
from be.model2.store import init_database
from be.model2.buyer import tostop
bp_shutdown = Blueprint("shutdown", __name__)


def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()


@bp_shutdown.route("/shutdown")
def be_shutdown():
    tostop()############测试不跑自动取消订单请删去
    shutdown_server()
    return "Server shutting down..."


def be_run():
    this_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(this_path)
    log_file = os.path.join(parent_path, "app.log")
    init_database(parent_path)

    logging.basicConfig(filename=log_file, level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)

    app = Flask(__name__)
    app.register_blueprint(bp_shutdown)
    app.register_blueprint(auth.bp_auth)
    app.register_blueprint(seller.bp_seller)
    app.register_blueprint(buyer.bp_buyer)
    app.run(threaded=True,host='127.0.0.1',port=5001,debug=True,use_reloader=False)