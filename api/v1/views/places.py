#!/usr/bin/python3
"""
 handles all default RESTFul API actions
 """

from os import abort
from flask import jsonify
from flask.helpers import make_response
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response
from models import storage


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def places_list(city_id):
    """retrieves all places of a city in the DB or creates a new one"""
    if request.method == 'GET':
        get_city = storage.get("City", city_id)
        if get_city is None:
            abort(404)
        place_list = []
        for place in get_city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)

    if request.method == 'POST':
        get_city = storage.get("City", city_id)
        if get_city is None:
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "name" not in json_data:
            abort(400, 'Missing name')
        if "user_id" not in json_data:
            abort(400, 'Missing user_id')
        get_user = storage.get("User", json_data["user_id"])
        if get_user is None:
            abort(404)
        json_data["city_id"] = city_id
        new_place = Place(**json_data)
        storage.save()
        return(make_response(jsonify(new_place.to_dict()), 201))


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def places_id(place_id):
    """retrieves, deletes or updates an specific place object filtered by id"""
    if request.method == 'GET':
        place_by_id = storage.get('Place', place_id)
        if (place_by_id is not None):
            return jsonify(place_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        place_by_id = storage.get('Place', place_id)
        empty_dict = {}
        if (place_by_id is not None):
            storage.delete(place_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        place_by_id = storage.get('Place', place_id)
        ignored_keys = [
            "id", "created_at", "updated_at", "user_id", "city_id"]
        if(place_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(place_by_id, key, value)
                storage.save()
        return make_response(jsonify(place_by_id.to_dict()), 200)
