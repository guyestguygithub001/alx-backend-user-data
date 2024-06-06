#!/usr/bin/env python3
"""This module provides session authentication functionality for the API with expiration and storage support."""

from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth

class SessionDBAuth(SessionExpAuth):
    """This class provides methods for handling session authentication with expiration and storage support."""

    def create_session(self, user_id=None) -> str:
        """Generates a new session ID for a given user ID and stores it in the database."""
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves the user ID associated with a given session ID from the database."""
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Terminates the current session and removes it from the database."""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True

