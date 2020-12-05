from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.LoginAPI.as_view()),
    path("signup/", views.RegistrationAPI.as_view()),
    path("users/<str:username>/encyclopedia/", views.get_encyclopedia), # 도감 확인'
    path('social_signup/', views.social_signup),
    path('new_kakao/', views.new_kakao),
    path('<str:nickname>/find_id/', views.find_id),
    path('users/me/', views.UserAPI.as_view()),
    path('users/<str:username>/me/', views.profile),
    path('change_pw/',views.change_password),
]