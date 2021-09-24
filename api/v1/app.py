#!/usr/bin/python3
"""
Blueprint register and teardown implementation for session
close after query
"""

from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask import Flask
import os
from flask import jsonify
from flask.helpers import make_response
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.config["DEBUG"] = True


@app.teardown_appcontext
def appcontext(exception):
    """closes storage after each call"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handler for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', "0.0.0.0"),
            port=os.getenv('HBNB_API_PORT', "5000"), threaded=True)
