#!/usr/bin/python3
"""
 handles all default RESTFul API actions
 """

from os import abort
from flask import jsonify
from flask.helpers import make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def states_list():
    """retrieves all states objects in the DB or creates a new one"""
    if request.method == 'GET':
        state_dic = storage.all('State')
        states_list = []
        for states in state_dic.values():
            states_list.append(states.to_dict())
        return jsonify(states_list)

    if request.method == 'POST':
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "name" not in json_data:
            abort(400, 'Missing name')
        new_state = State(**json_data)
        storage.save()
        return(make_response(jsonify(new_state.to_dict()), 201))


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def states_id(state_id):
    """retrieves, deletes or updates an specific state object filtered by id"""
    if request.method == 'GET':
        state_by_id = storage.get('State', state_id)
        if (state_by_id is not None):
            return jsonify(state_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        state_by_id = storage.get('State', state_id)
        empty_dict = {}
        if (state_by_id is not None):
            storage.delete(state_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        state_by_id = storage.get('State', state_id)
        ignored_keys = ["id", "created_at", "updated_at"]
        if(state_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(state_by_id, key, value)
                storage.save()
            return make_response(jsonify(state_by_id.to_dict()), 200)
