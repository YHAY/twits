from flask import Flask, json, request
from flask_restful import Api

from DBManager import *

app = Flask(__name__)
api = Api(app)


@app.route("/users", methods=["POST"])
def join():
    user = request.get_json()
    print("user : ", user)
    if "id" and "pw" and "name" and "country" and "device_num" in user:
        req_result, msg = join(user["id"], user["pw"], user["name"], user["country"], user["device_num"])
        if req_result:
            return {'status': 'success'}
        else:
            return {'status': 'failed'}
    else:
        return {'status': 'failed',
                'detail': 'not enough request contents'}


@app.route("/users", methods=["DELETE"])
def deㅣ_user():
    #
    return {'status': 'success'}


@app.route("/users", methods=["GET"])
def user_list():
    data = {'status': 'success'}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/users/logout", methods=["PUT"])
def logout():
    return {'status': 'success'}


@app.route("/game/matching", methods=["PUT"])
def matching():
    return {'status': 'success'}


@app.route("/game/round/<game_token>/choice/<choice_num>", methods=["PUT"])
def choice(game_token, choice_num):
    return {
        'status': 'success',
        'round':game_token,
        'choice_num':choice_num
        }


@app.route("/game/round/<game_token>", methods=["GET"])
def result(game_token):
    return {
        'status': 'success',
        'round':game_token
    }


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host="192.168.0.100", port=5000, debug=True)
