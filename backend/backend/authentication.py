# backend/authentication.py
from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Session authentication without CSRF validation.
    Use this when CSRF middleware is disabled.
    """
    def enforce_csrf(self, request):
        return  # Do not enforce CSRF check
