#!/usr/bin/env python3
""" Auth module
"""
from flask import request
from typing import List


class Auth():
    """ Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns bool of whether path is in list execluded_paths or not """
        return False

    def authorization_header(self, request=None) -> str:
        """returns authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns current user"""
        return None
