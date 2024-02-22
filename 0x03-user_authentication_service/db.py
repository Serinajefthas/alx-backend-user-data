#!/usr/bin/env python3
"""DB module
"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """returns User object and adds user to db"""
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """find user by filtering user tbl by input args"""
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
            if user is None:
                raise NoResultFound("Not found")
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("Invalid") from e

    def update_user(self, user_id: int, **kwargs: dict[str, str]) -> None:
        """updates user's attributes w user id and arbitary keywords"""
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise NoResultFound(f"No user found with id {user_id}")

        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute '{key}'")

        """saves to db"""
        try:
            self._session.commit()
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request")
