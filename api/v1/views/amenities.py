#!/usr/bin/python3
"""
 handles all default RESTFul API actions
 """

from os import abort
from flask import jsonify
from flask.helpers import make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response
from models import storage


@app_views.route('/amenities',
                 strict_slashes=False, methods=['GET', 'POST'])
def amenities_list():
    """Retrieves the list of all Amenity objects or creates a new one"""
    if request.method == 'GET':
        get_amenities = storage.all("Amenity")
        if get_amenities is None:
            abort(404)
        amenities_list = []
        for amenity in get_amenities.values():
            amenities_list.append(amenity.to_dict())
        return jsonify(amenities_list)

    if request.method == 'POST':
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "name" not in json_data:
            abort(400, 'Missing name')
        new_amenity = Amenity(**json_data)
        storage.save()
        return(make_response(jsonify(new_amenity.to_dict()), 201))


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def amenities_id(amenity_id):
    """
    retrieves, deletes or updates an specific amenity object filtered by id
    """
    if request.method == 'GET':
        amenity_by_id = storage.get('Amenity', amenity_id)
        if (amenity_by_id is not None):
            return jsonify(amenity_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        amenity_by_id = storage.get('Amenity', amenity_id)
        empty_dict = {}
        if (amenity_by_id is not None):
            storage.delete(amenity_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        amenity_by_id = storage.get('Amenity', amenity_id)
        ignored_keys = ["id", "created_at", "updated_at"]
        if(amenity_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(amenity_by_id, key, value)
                storage.save()
            return make_response(jsonify(amenity_by_id.to_dict()), 200)
