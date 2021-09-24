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
from models.review import Review
from api.v1.views import app_views
from flask import abort
from flask import request
from flask import make_response
from models import storage


@app_views.route('places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET', 'POST'])
def reviews_list(place_id):
    """retrieves all reviews of a city in the DB or creates a new one"""
    if request.method == 'GET':
        get_place = storage.get("Place", place_id)
        if get_place is None:
            abort(404)
        reviews_list = []
        for review in get_place.reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)

    if request.method == 'POST':
        get_place = storage.get("Place", place_id)
        if get_place is None:
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        if "user_id" not in json_data:
            abort(400, 'Missing user_id')
        get_user = storage.get("User", json_data["user_id"])
        if get_user is None:
            abort(404)
        if "text" not in json_data:
            abort(400, 'Missing text')
        json_data["place_id"] = place_id
        new_review = Review(**json_data)
        storage.save()
        return(make_response(jsonify(new_review.to_dict()), 201))


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET', 'DELETE', 'PUT'])
def reviews_id(review_id):
    """
    retrieves, deletes or updates an specific review
    object filtered by id
    """
    if request.method == 'GET':
        review_by_id = storage.get('Review', review_id)
        if (review_by_id is not None):
            return jsonify(review_by_id.to_dict())
        else:
            abort(404)

    if request.method == 'DELETE':
        review_by_id = storage.get('Review', review_id)
        empty_dict = {}
        if (review_by_id is not None):
            storage.delete(review_by_id)
            storage.save()
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)

    if request.method == 'PUT':
        review_by_id = storage.get('Review', review_id)
        ignored_keys = [
            "id", "created_at", "updated_at", "user_id", "place_id"]
        if(review_by_id is None):
            abort(404)
        json_data = request.get_json()
        if not request.json:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if(key in ignored_keys):
                pass
            else:
                setattr(review_by_id, key, value)
                storage.save()
        return make_response(jsonify(review_by_id.to_dict()), 200)
