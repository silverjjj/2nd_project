from django.db import models
from django.conf import settings

# Create your models here.

class Animal(models.Model):
    name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    avg_weight = models.CharField(max_length=100, null=True)
    avg_size = models.CharField(max_length=100, null=True)
    distribution_area = models.CharField(max_length=100, null=True)
    characteristics = models.TextField(blank=True)
    image_1 = models.ImageField(upload_to="images", blank=True)
    image_2 = models.ImageField(upload_to="images", blank=True)
    image_3 = models.ImageField(upload_to="images", blank=True)
    image_4 = models.ImageField(upload_to="images", blank=True)
    image_5 = models.ImageField(upload_to="images", blank=True)
    

class AnimalImage(models.Model):
    upload_image = models.ImageField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True) # 업로드 시간
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    upload_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 업로드 유저
