from flask import Flask, json, request
from flask_restful import Api

from DBManager import *
from schema.schema_set import *
from jsonschema import validate
import sys

app = Flask(__name__)
api = Api(app)

db_manager = DBManager()


# 요청을 받으면, json validator먼저 거치도록 만들것.
WIN = 1
LOSE = 0
TIE = 99

'''
남은 일
1. json validator전체 적용(ok)
2. 전체 점검
2. jwt적용
'''


@app.route("/users", methods=["POST"])
def join():
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, matching_schema)
    if not status_code == 401:
        req_result, msg = db_manager.join(req_body["id"], req_body["pw"], req_body["name"], req_body["country"], req_body["device_num"])
        if req_result:
            resp = {'status': 'success'}
        else:
            status_code = 401
            resp = {
                "error_code": 20003,  # 조금있다가 따로 빼자.
                "message": "Join-in Failed",
                "detail": msg
            }
    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/users", methods=["DELETE"])
def del_user():
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, matching_schema)
    if not status_code == 401:
        if db_manager.del_user(req_body["id"], req_body["pw"], req_body["country"]):
            resp = {'status': 'success'}
        else:
            status_code = 401
            resp = {
                "error_code": 20003,
                "message": "Delete User Failed",
                "detail": "No exist user."
            }
    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/users", methods=["GET"])
def login():
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, matching_schema)
    if not status_code == 401:
        token = db_manager.login(req_body["id"], req_body["pw"], req_body["device_number"])
        # db_manager.set_wait(token)  # add user into matches table. > 사람이 start를 누르는 순간, 들어가야함.
        resp = {"token": token}

    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/users/logout", methods=["PUT"])
def logout():
    # 해당 사용자의 정보를 match테이블에서 지운다.
    # 해당 사용자가 혹시 waiting or matches 같은 테이블에 있으면 무조건 지웁니다.
    return {'status': 'success'}


@app.route("/game/matching/<user_token>", methods=["PUT"])
def matching(user_token):
    # status_code = 200
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, matching_schema)
    if not status_code == 401:
        # matching table에 올린다. 그리고 match 테이블에서 상대가 있는지 찾아서 resp.
        # 1. d있다면 상대방의 이름(name), game_token, id
        #현재 사용자의 상태가 어떠한지 확인.
        #RESULT = user_token, state, rival_token
        state, additional_info = db_manager.get_user_state(user_token)
        # print("result : ", result)
        if state:
            # 만약 play중이라면, game테이블에서 찾아서 응답을 보내줄 것! > 지속적으로 matching으로 요청할 것이기 때문.
            if state == PLAYING:
            # if result[0][1] == PLAYING:
                # db_manager.get_game(result[0][0])
                result = db_manager.get_match_list(user_token)
                resp = {
                    "user_token": user_token,
                    "game_auth": result[0][0],
                    "rival": result[0][1]
                }
            # if state == PLAYING:
            else:# waiting
                waiting_list = db_manager.get_waiting_list()
                if waiting_list:
                    rival_token = waiting_list[0][0]
                    resp = set_matching(user_token, rival_token)
                # update count time.
        else:
            # waiting도 playing도 아닌 상황. 그 이전의 상황일 경우
            # waiting테이블을 검색해서 가능한 사람있으면 바로 mathcing해서 보내고.
            waiting_list = db_manager.get_waiting_list()
            if waiting_list:
                rival_token = waiting_list[0][0]
                resp = set_matching(user_token, rival_token)
            else:
                # 없으면 waiting테이블에 넣기
                # add user into waiting.
                db_manager.insert_waiting(user_token)
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


def set_matching(user_token, rival_token):
    # matching!!
    game_token = str(uuid.uuid4())
    db_manager.set_match(user_token, rival_token, game_token)
    db_manager.set_match(rival_token, user_token, game_token)
    db_manager.rm_from_wait(rival_token)
    # results = db_manager.get_match_list(user_token)
    resp = {
        "user_token": user_token,
        "game_auth": game_token,
        "rival": rival_token
    }
    return resp


@app.route("/game/round/<game_token>/choice/<choice_num>", methods=["PUT"])
def choice(game_token, choice_num):
    # status_code = 200
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, choice_schema)
    if not status_code == 401:
        if "user" and "datetime" in req_body:
            user_token = req_body["user"]
            choice_time = req_body["datetime"]
            # need check expired game_token?
            db_manager.set_choice(user_token, game_token, choice_num, choice_time)
            # 여기에서 result가 나올 수 있으면, result결과값을 줄까?
            resp = {
                'game_token': game_token
            }
    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


@app.route("/game/round/<game_token>", methods=["GET"])
def result(game_token):
    # 시간측정할거면 여기서 해야됨.
    # status_code = 200
    req_body = request.get_json()
    status_code, resp = schema_validate(req_body, matching_schema)
    if not status_code == 401:
        if "user" in req_body:
            win, result = db_manager.am_i_win(game_token)
            win_record = db_manager.get_win_record(req_body["user"])
            if result: # win result exist in result table.
                # already exist result. 결과가 나온상태
                game_result = 1 if win else 0
                resp = {
                    "result": game_result,
                    "win": [game_result, win_record[0][1]+1],
                    "game_token": game_token
                }
            else:
                # make a result. 결과를 내야하는 상태
                rsp_result = set_result(game_token)
                if rsp_result == WIN:
                    game_result = "win"
                elif rsp_result == LOSE:
                    game_result = "lose"
                else:
                    game_result = "tie"

                resp = {
                    "result": game_result,
                    "win": [game_result, win_record[0][1]+1],
                    "game_token": game_token
                }
    response = app.response_class(
        response=json.dumps(resp),
        status=status_code,
        mimetype='application/json'
    )
    return response


def set_result(game_token, user_token):
    # do make a result.
    user_list = db_manager.get_choices(game_token)
    if user_list:
        if len(user_list[0]) > 1:
            # 대전중인 상대가 있을때
            user_index = -1
            rival_index = -1
            for index, user in enumerate(user_list):
                if user[0][0] == user_token:
                    user_index = index
                else:
                    rival_index = index
            result = rock_scissors_paper(user_list[0][user_index], user_list[0][rival_index])
            # profile 테이블에 기록
            db_manager.update_profile_win(user_token, result)

            # result 테이블에 기록 > 같은 game_token에 전부 업데이트.
            db_manager.update_result(game_token, user_token, result)
            # send result
            return result


def rock_scissors_paper(user_num, rival_num):
    if user_num == rival_num:
        return TIE
    elif user_num == 2 and rival_num == 0:
        # user (paper), rival (rock)
        return WIN
    elif rival_num == 2 and user_num == 0:
        # rival (paper), user (rock)
        return LOSE
    else:
        if user_num < rival_num:
            return WIN
        else:
            return LOSE


def schema_validate(request_body, schema_rule):
    try:
        validate(instance=request_body, schema=schema_rule)
    except:
        # lack of json body.
        status_code = 401
        resp = {
            "error_code": 20003,
            "message": "Matching Request Failed",
            "detail": "Check your request. Not enough requests." + sys.exc_info()[1]
        }
        return status_code, resp
    else:
        return 200, {}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
