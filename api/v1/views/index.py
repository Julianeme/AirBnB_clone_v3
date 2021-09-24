#!/usr/bin/python3
"""
Route for /status, returns OK if connection successful
"""
from api.v1.views import app_views
import flask
from flask import jsonify
from models.engine import db_storage, file_storage
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns a status answer when /status is called """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """endpoint that retrieves the number of each objects by type """
    statistics = {}
    classes_dict = {"amenities": "Amenity",
                    "cities": "City",
                    "places": "Place",
                    "reviews": "Review",
                    "states": "State",
                    "users": "User"
                    }
    for key, value in classes_dict.items():
        statistics[key] = storage.count(value)
    return(jsonify(statistics))
