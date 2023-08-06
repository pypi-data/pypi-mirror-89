from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from ..tokens import magic_token


class MagicLinkBackend(BaseBackend):
    def get_user(self, uid64):
        try:
            # get user id base on uid64
            uid = force_text(urlsafe_base64_decode(uid64))
            user = get_user_model().objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        return user

    def authenticate(self, request, uid64, token):
        user = self.get_user(uid64)
        if user is not None and magic_token.check_token(user, token):
            return user
        else:
            return None
