import  jwt
import time
import sqlalchemy
from be.model2.db import db
from be.model2 import error
# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")

# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class User():
    def __init__(self):
        db.__init__(self)



    def register(self, user_id: str, password: str):
        terminal = "terminal_{}".format(str(time.time()))
        try:
            token=""
            self.session.execute(  "INSERT INTO usr (user_id, password, balance, token, terminal) values (:user_id, :password, 0, :token, :terminal)",{"user_id":user_id,"password": password,"token":token,"terminal":terminal })
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_user_id(user_id)

        return 200, "ok"

    def unregister(self, user_id: str, password: str):
        user = self.session.execute("SELECT password from usr where user_id=:user_id",
                                        {"user_id": user_id}).fetchone()
        if user == None:
            code, message = error.error_authorization_fail()
            return code, message

        if password != user.password:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("DELETE from usr where user_id='%s'"% (user_id,))
        self.session.commit()

        return 200, "ok"

    def login(self, user_id: str, password: str,terminal:str):
        token = ""
        user = self.session.execute("SELECT password from usr where user_id=:user_id",{"user_id":user_id}).fetchone()
        if user is None or  password != user.password:
            code, message=error.error_authorization_fail()
            return code, message,token
        token = jwt_encode(user_id, terminal)
        self.session.execute(
            "UPDATE usr set token= '%s' , terminal = '%s' where user_id = '%s'"% (token, terminal, user_id) )
        self.session.commit()
        return 200, "ok", token

    def logout(self,user_id: str, token: str):
        try:
            user = self.session.execute("SELECT token from usr where user_id='%s'" % (user_id)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            self.session.execute(
                "UPDATE usr SET token = '%s' WHERE user_id='%s'" % (newtoken, user_id))
            self.session.commit()
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

    def change_password(self, user_id: str,  old_password: str, new_password: str):
        usr = self.session.execute("SELECT password from usr where user_id='%s'"%(user_id,)).fetchone()
        if usr is None  or old_password != usr.password:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE usr set password = '%s' where user_id = '%s'"%(new_password,user_id), )
        self.session.commit()
        return 200, "ok"