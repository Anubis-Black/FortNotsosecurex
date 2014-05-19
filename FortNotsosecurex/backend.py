from django.contrib.auth.models import User


class Backend(object):
    @staticmethod
    def authenticate(username=None, password=None):
        try:
            user = User.objects.raw(
                "SELECT * FROM auth_user WHERE username = '" + username + "' AND password = '" + password + "'")[0]

            return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None