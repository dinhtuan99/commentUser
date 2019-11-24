import datetime
import time
from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request


@app.route('/')  # to check whether the application is running correctly on port
def hello_world():
    return "Hello babe!!!"


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _userId = _json['userId']
    _comment = _json['comment']
    x = time.strptime(time.strftime("%H:%M:%S", time.localtime()).split(',')[0], '%H:%M:%S')
    _date = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    # validate the received values
    if _userId and _comment and _date and request.method == 'POST':
        # save details
        id = mongo.db.user.insert({'userId': _userId, 'comment': _comment, 'date': _date})
        resp = jsonify('Comment added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/update', methods=['PUT'])
def update_user():
    _json = request.json
    _id = _json['_id']
    _userId = _json['userId']
    _comment = _json['comment']
    x = time.strptime(time.strftime("%H:%M:%S", time.localtime()).split(',')[0], '%H:%M:%S')
    _date = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
    # validate the received values
    if _userId and _comment and _date and _id and request.method == 'PUT':

        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'userId': _userId, 'comment': _comment, 'date': _date}})
        resp = jsonify('Comment updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Comment deleted successfully!')
    resp.status_code = 200
    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run()
