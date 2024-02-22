#!/usr/bin/env python3
"""Creates hash password model"""


import bcrypt
import logging
from typing import Union
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """encryptes password to hash it"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns new uuid string"""
    return str(uuid4())


class Auth:
    """auth model to interact w authentication db"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates new user w details given and adds to db"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_passwrd = _hash_password(password)

        """save user to db"""
        new_user = self._db.add_user(email, hashed_passwrd)

        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """returns whether successfully located user or not"""
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                passw_bytes = password.encode('utf-8')
                hashed = user.hashed
                if bcrypt.checkpw(passw_bytes, hashed):
                    return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """gets user email and returns session id generated using uuid"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """retrieve user object from corresp session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """deletes session linked to user id given"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)
