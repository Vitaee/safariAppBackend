from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('refresh/token/', TokenRefreshView.as_view(), name="token_refresh" ),
    path('profile', views.UserView.as_view(),name='profile_view'),
    path('register', views.UserRegisterView.as_view(), name='sign_up')

]