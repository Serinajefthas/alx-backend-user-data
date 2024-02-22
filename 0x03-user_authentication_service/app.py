#!/usr/bin/env python3
"""A simple Flask app with user authentication features.
"""
import logging

from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

logging.disable(logging.WARNING)


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET method returning json text of welcome msg"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def new_users() -> str:
    """registers new user if user does not exist, else returns msg"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": "<registered email>",
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """creates new session_id of user if correct login, else abort 401"""
    email, password = request.form.get("email"), request.form.get("password")
    """invalid auth"""
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    status = jsonify({"email": email, "message": "logged in"})
    status.set_cookie("session_id", session_id)
    return status


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """destroys session_id then redirects user to home page, else 403"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    
    AUTH.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
