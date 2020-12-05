from django.urls import path
from . import views

urlpatterns = [
    path('animals/<str:animal_name>/', views.animal_detail), # 동물 상세 정보
    path('animals/', views.animal_list), # 동물 종류 전체 목록
    path('today-animal/', views.Random_animal.as_view()), # 오늘의 동물
    path('predict/image/',views.upload_image), # 이미지
    path('save-image/', views.save_image)
]
