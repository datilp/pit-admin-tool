from django.urls import path  # allows to create paths within our app

from knox.views import LogoutAllView
from knox.views import LoginView as KnoxLoginView
from . import views

app_name = 'user'  # part of the url reverse loopkup functionality

urlpatterns = [
    # the path will be user/create and will be wired to the CreateUserView
    # The app_name and the below name='create' helps with the url reverse
    # lookup done in the test functions.
    # Finally we want to include this url on the app main urls in app/urls.py
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('tokenkx/', views.CustomObtainAuthToken.as_view(), name='token2'),
    #path('login/', views.CustomObtainAuthToken.as_view(), name='login'),
    path('login/', views.ObtainExpiringAuthToken.as_view(), name='login'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path(r'loginkx/', KnoxLoginView.as_view(), name='knox_login'),
    path('loginx/', views.LoginView.as_view(), name='loginx'),
    path('logoutx/', LogoutAllView.as_view(), name='knox_logout'),
    path('mex/', views.ManageUserViewX.as_view(), name='mex'),
]
