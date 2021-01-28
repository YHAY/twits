from flask import Flask, json, request
from flask_restful import Api

from DBManager import *

app = Flask(__name__)
api = Api(app)

db_manager = DBManager()


# 요청을 받으면, json validator먼저 거치도록 만들것.


@app.route("/users", methods=["POST"])
def join():
    user = request.get_json()
    print("user : ", user)
    if "id" and "pw" and "name" and "country" and "device_num" in user:
        req_result, msg = db_manager.join(user["id"], user["pw"], user["name"], user["country"], user["device_num"])
        if req_result:
            return {'status': 'success'}
        else:
            return {
                "error_code": 20003,  # 조금있다가 따로 빼자.
                "message": "Join-in Failed",
                "detail": msg
            }
    else:
        return {
            "error_code": 20003,
            "message": "Join-in Failed",
            "detail": "Check your request. Not enough requests."
        }


@app.route("/users", methods=["DELETE"])
def deㅣ_user():
    #
    return {'status': 'success'}


# @app.route("/users", methods=["GET"])
# def user_list():
#     data = {'status': 'success'}
#     response = app.response_class(
#         response=json.dumps(data),
#         status=200,
#         mimetype='application/json'
#     )
#     return response


@app.route("/users", methods=["GET"])
def login():
    user = request.get_json()
    status_code = 200
    if not user:  # no exist json body.
        resp = {
            "error_code": 20003,
            "message": "login Failed",
            "detail": "Check your request. Not enough requests."
        }
        status_code = 401
    else:
        if "id" and "pw" and "device_number" in user:
            token = db_manager.login(user["id"], user["pw"], user["device_number"])
            resp = {"token": token}

        else:  # lack of json body.
            status_code = 401
            resp = {
                "error_code": 20003,
                "message": "login Failed",
                "detail": "Check your request. Not enough requests."
            }

    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/users/logout", methods=["PUT"])
def logout():
    # 해당 사용자의 정보를 match테이블에서 지운다.
    return {'status': 'success'}


@app.route("/game/matching/<user_token>", methods=["PUT"])
def matching(user_token):
    # matching table에 올린다. 그리고 match 테이블에서 상대가 있는지 찾아서 resp.
    # 1. d있다면 상대방의 이름(name), game_token,

    # find rival in match table.
    rival_uuid = db_manager.get_match(user_token)
    status_code = 200
    if rival_uuid:
        print("rival exist")
        # wait인 사람이 있으면 바로 매칭해서 send.
        # rival_uuid가 1개 일 수도 있고, 아닐 수도 있음. > random select user & find rival name(not user_token)
        #
        resp = {
            "error_code": 20003,
            "message": "login Failed",
            "detail": "Check your request. Not enough requests."
        }
        """
        "token":"abcdefg12345",
        "game_auth":"abc123",
        "rival":"user1"
        """
    else:
        # wait인 사람이 없으면 대기 테이블로 넘어감.
        print("no one exist in waiting line")
        status_code = 400
        db_manager.set_wait()
        resp = {
            "error_code": 20003,
            "message": "Failed to matching",
            "detail": "no exist user to match"
        }

    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/game/round/<game_token>/choice/<choice_num>", methods=["PUT"])
def choice(game_token, choice_num):
    return {
        'status': 'success',
        'round': game_token,
        'choice_num': choice_num
    }


@app.route("/game/round/<game_token>", methods=["GET"])
def result(game_token):
    return {
        'status': 'success',
        'round': game_token
    }



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host="192.168.0.100", port=5000, debug=True)
