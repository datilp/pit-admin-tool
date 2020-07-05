from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
import sys
import json
import inspect
import datetime
from user.authentication import ExpiringTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.utils.translation import gettext as _
from rest_framework import status, exceptions  # module containing status codes in
#     human readable strings

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication as KnoxTokenAuthentication
from knox.models import AuthToken

from user.serializers import UserSerializer, AuthTokenSerializer


# this view will interact with the database back and forth
# for a given web request/response

# by using the generic CreateAPIView we use a bunch of functionality
# to deal with db interaction.
# Things such as queryset, serializer class, lookup fields, filter,
# pagination, etc
# This view serializer class is the UserSerializer so it knows
# what DB table and fields is using.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


# this version is not working. Not sure where I got this from.
# The problem here is the
# serializer = self.serializer_class(data=request.data)
#
# will be invalid all the time. Not sure if it ever worked.
# for instance the following curl command will login user
# test@lbto.org, which we have already setup via the django
# admin interface in http://localhost:8000/admin
#
# curl -X POST -d email=test@lbto.org -d password=abcd123
# -H 'Accept: application/json;' http://localhost:8000/api/user/login/
# and will return something like:
# {"idToken":"43d4f0e01e9b743a9147e483eecc9083035b8223","localId":3,
# "email":"test@lbto.org","partner":"AZ"}
# The token given should be an expiring type, meaning it will cease to
# be valid after a predefined time.
# See user.authentication and REST_FRAMEWORK_TOKEN_EXPIRE_HOURS
class ObtainExpiringAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    # authentication_classes = (ExpiringTokenAuthentication,)
    # authentication_classes = (ExpiringTokenAuthentication,)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [TokenHasReadWriteScope]
    # sets the renderer so we can use the this view in the HTML/browser
    # renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        print(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
        sys.stdout.write("request data:")
        # request.data['returnSecureToken']=False
        print(json.dumps(request.data))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            sys.stdout.write("Serializer is valid\n")
            auths = self.get_authenticators()
            # hello
            print("Authenticators:")
            print(auths)
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created:
                print("token already exists:")
                print(token)
                for auth in auths:
                    if isinstance(auth, ExpiringTokenAuthentication):
                        auth.authenticate_credentials(token)
                #update the created time of the token to keep it valid
                #token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                token.created = datetime.datetime.utcnow()
                token.save()
                sys.stdout.write(token.created.strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            else:
                sys.stdout.write("token created:\n")
        else:
            sys.stdout.write("Serializer not valid, user probably doesn't exists\n")
            print(json.dumps(serializer.errors))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        # sys.stdout.write("token data:")
        # sys.stdout.write(response.data['token'])
        # token = Token.objects.get(key=response.data['token'])
        print("token structure:")
        # sys.stdout.write(json.dumps([name for name, thing in inspect.getmembers(token.user)]))
        print(token.user.partner)
        return Response({'idToken': token.key,
                         'localId': token.user_id,
                         'email': token.user.email,
                         'partner': token.user.partner})


# knox authentication views
# Note: Add knox to the INSTALL_APPS in settings.py
class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()
        now = datetime.datetime.now()
        expiry_in_secs = self.format_expiry_datetime(instance.expiry)
        expiry_date = datetime.datetime.utcfromtimestamp(int(expiry_in_secs))
        data = {
            'expirationTime': (expiry_date - now).total_seconds(),
            'token': token,
            'userId': request.user.id
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data

    def ppost(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            print("after setting filter: token=", token)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN
                )
        token_ttl = self.get_token_ttl()
        #print("abut to get token?")
        #token = AuthToken.objects.get(request.user)
        #print("token:", token)
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        return Response(data)

    def pppost(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        print("login: Post: serializer:", serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print("login: Post: user:", user)
        #request.user.auth_token.delete()
        login(request, user)
        return super(LoginView, self).post(request, format=None)
        #return self.ppost(request, format=None)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    # sets the renderer so we can use the this view in the HTML/browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        sys.stdout.write("request data:")
        sys.stdout.write(json.dumps(request.data))
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        sys.stdout.write("token data:")
        sys.stdout.write(response.data['token'])
        token = Token.objects.get(key=response.data['token'])
        sys.stdout.write("token structure:")
        # sys.stdout.write(json.dumps([name for name, thing in inspect.getmembers(token.user)]))
        sys.stdout.write(token.user.partner)
        return Response({'idToken': token.key,
                         'localId': token.user_id,
                         'email': token.user.email,
                         'partner': token.user.partner})
    '''
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = {
                'token': token,
                'user': UserSerializer(user).data
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    response.data['token'],
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            sys.stdout.write("in LogoutView\n")
            sys.stdout.write(json.dumps(request.data))
            sys.stdout.write("\n")
            if "token" in request.data:
                sys.stdout.write("Only the token\n")
                sys.stdout.write(request.data['token'])
                sys.stdout.write("\n")
                user = Token.objects.get(key=request.data['token']).user
                sys.stdout.write("deleting user\n")
                user.auth_token.delete()
            else:
                request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        # if getattr(settings, 'REST_SESSION_LOGIN', True):
        #    django_logout(request)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        # if getattr(settings, 'REST_USE_JWT', False):
        #    from rest_framework_jwt.settings import api_settings as jwt_settings
        # #    if jwt_settings.JWT_AUTH_COOKIE:
        #        response.delete_cookie(jwt_settings.JWT_AUTH_COOKIE)
        return response


class CreateTokenView(ObtainAuthToken):
    """Create a new user token for the user"""
    serializer_class = AuthTokenSerializer
    # sets the renderer so we can use the this view in the HTML/browser
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# this endpoint is based on the RetrieveUpdateView which provides
# get, put and patch method handlers.
# So we can read or update this endpoint for instance to get user
# information or update the user.
# Notice that via the permission_classes, i.e. permissions.IsAuthenticated
# we are saying that this view can only work if the user has been
# authenticated already.
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer  # serializer class attribute
    # the authentication class type is going to be token base
    # authentication_classes = (authentication.TokenAuthentication,)
    # the permissions are going to be just that it is authenticated
    permission_classes = (permissions.IsAuthenticated,)

    # with a view since it is linked to a model it will return the database
    # object corresponding to that model.
    # In this case we just want to return the user, so we override the
    # get_object method to do just that.
    def get_object(self):
        """Retrieve and return authentication user"""
        # the authentication_classes will make sure to attach to the request
        # the authenticated user. It is done automatically.
        #print(json.dumps(self.request.user))
        print(self.request.user)
        return self.request.user


# Sample calls to the knox endpoints
# curl -X POST -d email=test@lbto.org -d password=abcd123
#       -H 'Accept: application/json;' http://localhost:8000/api/user/loginx/
# gets:
# {"expiry":"2020-07-02T09:57:51.522904Z",
#  "token":"719a482baa4991adcee186b82d738ec1a407e032a72e2446060bee2d6893590e"}
#  curl -X GET -H "Authorization: Token 719a482baa4991adcee186b82d738ec1a407e032a72e2446060bee2d6893590e"
#       http://localhost:8000/api/user/mex/
# gets
# {"email":"test@lbto.org","name":"test user, hello","partner":"AZ"}
# logout
# curl -X POST -H "Content-Type: application/json" \
# -H "Authorization:Token 719a482baa4991adcee186b82d738ec1a407e032a72e2446060bee2d6893590e" \
# -d token=719a482baa4991adcee186b82d738ec1a407e032a72e2446060bee2d6893590e \
#  http://localhost:8000/api/user/logoutx/
# gets nothing back
class ManageUserViewX(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    authentication_classes = (KnoxTokenAuthentication,)
    serializer_class = UserSerializer  # serializer class attribute
    # the authentication class type is going to be token base
    # authentication_classes = (authentication.TokenAuthentication,)
    # the permissions are going to be just that it is authenticated
    permission_classes = (permissions.IsAuthenticated,)

    # with a view since it is linked to a model it will return the database
    # object corresponding to that model.
    # In this case we just want to return the user, so we override the
    # get_object method to do just that.
    def get_object(self):
        """Retrieve and return authentication user"""
        # the authentication_classes will make sure to attach to the request
        # the authenticated user. It is done automatically.
        #print(json.dumps(self.request.user))
        print(self.request.user)
        return self.request.user
