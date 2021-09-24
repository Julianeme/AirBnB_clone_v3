#!/usr/bin/python3
"""
 handles all default RESTFul API actions
 """

from os import abort
from flask import jsonify
from flask.helpers import make_response
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response
from models import storage


@app_views.route('/users',
                 strict_slashes=False, methods=['GET', 'POST'])
def users_list():
    """Retrieves the list of all Amenity objects or creates a new one"""
    if request.method == 'GET':
        get_users = storage.all("User")
        if get_users is None:
            abort(404)
        user_list = []
        for user in get_users.values():
            user_list.append(user.to_dict())
        return jsonify(user_list)

    if request.method == 'POST':
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "email" not in json_data:
            abort(400, 'Missing email')
        if "password" not in json_data:
            abort(400, 'Missing password')
        new_user = User(**json_data)
        storage.save()
        return(make_response(jsonify(new_user.to_dict()), 201))


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """
    retrieves, deletes or updates an specific amenity object filtered by id
    """
    if request.method == 'GET':
        user_by_id = storage.get('User', user_id)
        if (user_by_id is not None):
            return jsonify(user_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        user_by_id = storage.get('User', user_id)
        empty_dict = {}
        if (user_by_id is not None):
            storage.delete(user_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        user_by_id = storage.get('User', user_id)
        ignored_keys = ["id", "created_at", "updated_at", "email"]
        if(user_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(user_by_id, key, value)
                storage.save()
            return make_response(jsonify(user_by_id.to_dict()), 200)
