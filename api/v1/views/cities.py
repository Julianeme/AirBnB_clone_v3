#!/usr/bin/python3
"""
 handles all default RESTFul API actions
 """

from os import abort
from flask import jsonify
from flask.helpers import make_response
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response
from models import storage


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def cities_list(state_id):
    """retrieves all cities of a state in the DB or creates a new one"""
    if request.method == 'GET':
        get_state = storage.get("State", state_id)
        if get_state is None:
            abort(404)
        ct_list = []
        for city in get_state.cities:
            ct_list.append(city.to_dict())
        return jsonify(ct_list)

    if request.method == 'POST':
        get_state = storage.get("State", state_id)
        if get_state is None:
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "name" not in json_data:
            abort(400, 'Missing name')
        json_data["state_id"] = state_id
        new_city = City(**json_data)
        storage.save()
        return(make_response(jsonify(new_city.to_dict()), 201))


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def cities_id(city_id):
    """retrieves, deletes or updates an specific city object filtered by id"""
    if request.method == 'GET':
        city_by_id = storage.get('City', city_id)
        if (city_by_id is not None):
            return jsonify(city_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        city_by_id = storage.get('City', city_id)
        empty_dict = {}
        if (city_by_id is not None):
            storage.delete(city_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        city_by_id = storage.get('City', city_id)
        ignored_keys = ["id", "created_at", "updated_at", "state_id"]
        if(city_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(city_by_id, key, value)
                storage.save()
            return make_response(jsonify(city_by_id.to_dict()), 200)
