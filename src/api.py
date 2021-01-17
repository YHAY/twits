from flask import Flask, json
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


@app.route("/users", methods=["POST"])
def join():
    return {'status': 'success'}


@app.route("/users", methods=["DELETE"])
def deㅣ_user():
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
    app.run(debug=True)
