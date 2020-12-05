from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from animals.models import *

# Create your models here.
class User(AbstractUser):
  REGISTER_LOGIN_EMAIL = "email"
  REGISTER_LOGIN_GOOGLE = "google"
  REGISTER_LOGIN_KAKAO = "kakao"

  REGISTER_LOGIN_METHOD_1 = (
      (REGISTER_LOGIN_EMAIL, "Email"),
      (REGISTER_LOGIN_GOOGLE, "Google"),
      (REGISTER_LOGIN_KAKAO, "Kakao"),
  )
  nickname = models.CharField(max_length=100, null=True)
  register_login_method = models.CharField(
        max_length=50, choices=REGISTER_LOGIN_METHOD_1, default=REGISTER_LOGIN_EMAIL
    )

class History(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 업로드한 유저
  image = models.ForeignKey(AnimalImage, on_delete=models.CASCADE) # 업로드 사진
  result = models.TextField() # 분석 결과
  classify_date = models.DateTimeField(auto_now_add=True) # 업로드 시간
  accuracy = models.FloatField(default=0) # 정확도

class Encyclopedia(models.Model): # 이미지와 연결되어 있어서 품종 컬럼 필요 없음
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저 하나는 도감 하나를 가짐
  image = models.ForeignKey(AnimalImage, on_delete=models.CASCADE, null=True) # 1:N 업로드 이미지 연결

class Suggestion(models.Model): # 건의사항 받을 때
  title = models.CharField(max_length=100)
  content = models.TextField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)