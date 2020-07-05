from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
import sys

EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 0.2)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):

        try:
            print("In ExpiringTokenAuthentication:")
            print(key)
            token = self.get_model().objects.get(key=key)
        #except self.model.DoesNotExist:
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        print("Token created @" + token.created.strftime("%m/%d/%Y, %H:%M:%S"))
        #sys.stdout.write("Token created" + token.created.toString() + "\n")
        #if token.created < timezone.now() - timedelta(hours=EXPIRE_HOURS):
        if token.created < timezone.now() - timedelta(seconds=EXPIRE_HOURS*60*60):
            print("Token has expired")
            token.user.auth_token.delete()
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)
