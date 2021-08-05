import jwt
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.http import http_date
from django.conf import settings
import time
from .models import StoreUser


class JWTAuthenticationGenerator(object):
    HTTP_AUTHORIZATION = "HTTP_AUTHORIZATION"
    USER_ID_KEY = "uid"
    ALGORITHM = "HS256"
    IAT_KEY = "iat"
    TOKEN_STRING = settings.JWT_STRING
    SECRET_KEY = settings.JWT_SECRET
    TOKEN_RESET_TIMEOUT_DAYS = settings.JWT_RESET_TIMEOUT_DAYS

    def __init__(self, request, *args, **kwargs):
        super(JWTAuthenticationGenerator, self).__init__(*args, **kwargs)
        self.__token = request.META.get(self.HTTP_AUTHORIZATION)
        self.__decoded_data = {}
        self.__is_valid_token = False

    def validate_token(self, verify=True):
        if self.__token and self.__token.startswith(self.TOKEN_STRING):
            token = self.__token[len(self.TOKEN_STRING) + 1:].strip()
            try:
                if verify:
                    self.__decoded_data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
                    self.__is_valid_token = True
                else:
                    self.__decoded_data = jwt.decode(token, verify=False)
                return True
            except Exception as error:
                # Not logging the error on sentry
                # log_on_sentry("Error while validating token", None, 'ERROR', extra={'token': self.__token})
                pass
        return False

    def get_user(self):
        if not self.__is_valid_token:
            return None
        else:
            uid = self.__decoded_data.get(self.USER_ID_KEY)
            try:
                return StoreUser.objects.get(pk=uid)
            except StoreUser.DoesNotExist:
                return None

    @classmethod
    def encode(cls, user_id):
        data = {
            cls.USER_ID_KEY: user_id,
            'exp': timezone.datetime.utcnow() + timezone.timedelta(days=cls.TOKEN_RESET_TIMEOUT_DAYS),
            cls.IAT_KEY: timezone.datetime.utcnow()
        }
        return jwt.encode(data, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    def get_token(self):
        return self.__token[len(self.TOKEN_STRING) + 1:].strip()


def update_session_in_response(request, response, storeUser):
    if request.session.get_expire_at_browser_close():
        max_age = None
        expires = None
    else:
        max_age = request.session.get_expiry_age()
        expires_time = time.time() + max_age
        expires = http_date(expires_time)
    request.session[StoreUser.SESSION_KEY] = storeUser.id
    response.set_cookie(
        settings.SESSION_COOKIE_NAME,
        request.session.session_key, max_age=max_age,
        expires=expires,
        domain=None,
        path=settings.SESSION_COOKIE_PATH,
        secure=settings.SESSION_COOKIE_SECURE or None,
        httponly=settings.SESSION_COOKIE_HTTPONLY or None,
        samesite=settings.SESSION_COOKIE_SAMESITE,
    )
    return response
