from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import Q
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# import schedule, time
#############
import tensorflow.compat.v1 as tf, sys
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import numpy as np
###############
import base64
import requests
from datetime import datetime
import os

from accounts.models import User
from accounts.models import *
from .models import *
from .serializers import *

# 동물 상세 정보 보여주기
@api_view(['GET'])
def animal_detail(request, animal_name):
    animal = get_object_or_404(Animal, name=animal_name)
    image_serializer = AnimalImageSerializer(animal.animalimage_set.all(), many=True)
    serializer = AnimalSerializer(animal)
    result = {}
    result['detail'] = serializer.data
    result['images'] = image_serializer.data
    return Response(result)

# 동물  목록 총 100개
@api_view(['GET'])
def animal_list(request):
    animals = Animal.objects.all()
    name = request.GET.get('name')
    content = request.GET.get('content')
    serializer = AnimalSerializer(animals, many=True)
    if content and name:
        serializer = AnimalSerializer(Animal.objects.filter(Q(name__contains=name)|Q(characteristics__contains=content)), many=True)
    if content and name==None or (content and name==''):
        serializer = AnimalSerializer(Animal.objects.filter(characteristics__contains=content), many=True)
    if name and content==None or (name and content==''):
        serializer = AnimalSerializer(Animal.objects.filter(name__contains=name), many=True)
    data = serializer.data
    return Response(data)


# 랜덤으로 동물하나 pick
class Random_animal(generics.GenericAPIView):
    serializer_class = AnimalSerializer

    def get(self, request, *args, **kwargs):
        animal = Animal.objects.all().order_by('?')[0]
        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

############## for predict ##########################
def run_inference_on_image(imagePath, labelsFullPath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.


    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        result = []
        i = 1
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
            result.append({i:human_string[2:-3]})
            i += 1
        answer = labels[top_k[0]]
        return result[:5]
###########################################################################



@api_view(['POST'])
def upload_image(request):
    img_string = request.data['img_base64']
    imgdata = base64.b64decode(img_string)
    now = datetime.now()
    now = datetime.timestamp(now)
    filename = f'temp_image_{request.user}.jpg'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    config = ConfigProto(
            device_count = {'GPU': 0}
        )
    config.gpu_options.allow_growth = False
    session = InteractiveSession(config=config)
    modelFullPath = './tmp/output_graph.pb'
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    result = run_inference_on_image(filename, './tmp/output_labels.txt')
    os.remove(filename)
    return Response({'result' : result})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_image(request):
    img_string = request.data['img_base64']
    img_result = request.data['result']
    imgdata = base64.b64decode(img_string)
    now = datetime.now()
    now = datetime.timestamp(now)
    filename = f'{img_result}_{request.user}_{now}.jpg'
    dir_list = os.listdir(settings.MEDIA_ROOT+'/users/')
    if str(request.user) not in dir_list:
        os.makedirs(settings.MEDIA_ROOT+'/users/'+f'{request.user}/')
    media_root = settings.MEDIA_ROOT+'/users/'+f'{request.user}/'+filename
    with open(media_root, 'wb') as f:
        f.write(imgdata)
    animal = get_object_or_404(Animal, english_name=img_result)
    animal_image = AnimalImage.objects.create(
        upload_image=f'users/{request.user}/{filename}',
        animal=animal,
        upload_user=request.user
    )
    encyc = Encyclopedia.objects.create(
        user=request.user,
        image=animal_image
    )
    return Response({'message': '저장 완료'})