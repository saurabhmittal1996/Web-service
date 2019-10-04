from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import json
from flask_cors import CORS, cross_origin
import os
#from openerp import api,models,fields

app = Flask(__name__)
cors = CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#api = Api(app)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


class User(db.Model):
    id = db.Column(db.Integer)
    username = db.Column(db.String(80), unique=True, primary_key=True)
    password = db.Column(db.String(120), unique=False )

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    print(request.json['username'])
    username = request.json['username']
    password = request.json['password']
    
    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by username
@app.route("/user/<user_name>", methods=["GET"])
#@cross_origin()
def user_detail(user_name):
    user = User.query.get(user_name)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    password = request.json['password']

    user.password = password
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

@app.route("/login/<user_name>/<pass_word>", methods=["GET"])
def user_login(user_name, pass_word):
    all_users = User.query.all()
    logged = False
    for user in all_users:
        if(user.username == user_name):
            if(user.password== pass_word):
                logged = True
                break
    if(logged):
        return jsonify(login = True)
    return jsonify(login = False)
    


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
