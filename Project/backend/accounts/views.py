from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login

from allauth.account.views import SignupView

from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import *

from knox.models import AuthToken

from animals.models import *
from animals.serializers import *

from decouple import config

from django.db.models import Q

class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    User = get_user_model()
    def post(self, request, *args, **kwargs):
        body = {}
        try:    
            User.objects.get(email=request.data["username"])
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                update_last_login(None, user)       #최근 로그인 시간 저장    
                u_last_login = user.last_login
                up_last_login = u_last_login.strftime('%Y-%m-%d %H:%M:%S')
                user.last_login = up_last_login
                return Response(
                    {
                        "user": UserSerializer(
                            user, context=self.get_serializer_context()
                        ).data,
                        "token": AuthToken.objects.create(user)[1],
                    }
                )
            else:
                user = User.objects.get(email=request.data["username"])
                serializer = UserSerializer(user)
                data = serializer.data
                body["error"] = { "password" : "비밀번호가 일치하지 않습니다." ,'message': data["register_login_method"]}
                return Response(body)
        except: # ID 없음
            body["error"] = {
                "username": "아이디 정보가 없습니다."
                }
            return Response(body)
        

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    User = get_user_model()
    def get(self, request, *args, **kwargs):
        body = {}
        nickname=request.GET.get("nickname")
        serializer=UserSerializer(User.objects.filter(Q(nickname=nickname)), many=True)
        if serializer.data:
            return Response({'error': '해당 닉네임은 이미 존재합니다.'})
        return Response({'message': '중복 값 없음'})

    def post(self, request, *args, **kwargs):
        body = {}
        try:    # 이미 가입된 ID인지 확인
            User.objects.get(username=request.data["username"])
            body["error"] = {
                        "username": "해당 아이디는 이미 존재합니다."
                    }
            return Response(body)
        except: # 아이디 & 비밀번호 제한조건 확인
            if len(request.data["username"]) < 6:
                body["error"] = {
                        "username": "아이디는 6자리 이상이어야 합니다."
                    }
                return Response(body)
            if len(request.data["password"]) < 8:
                body["error"] = { "password" : "비밀번호는 8자리 이상이어야 합니다." }
                return Response(body)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        update_last_login(None, user)       #최근 로그인 시간 저장    
        u_last_login = user.last_login
        up_last_login = u_last_login.strftime('%Y-%m-%d %H:%M:%S')
        user.last_login = up_last_login
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated]) #로그인 확인
def get_encyclopedia(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    data = {}
    if user == request.user: #본인 확인 
        animals = Animal.objects.all()
        animals_serializer = AnimalSerializer(animals, many=True)
        for i in animals_serializer.data:
            temp_image = [i['image_1'], i['image_2'], i['image_3'],i['image_4'],i['image_5']]
            data[f'{i["id"]}'] = {'name': i['name'] ,'english_name': i['english_name'],'encyclopedia': False, 'images': temp_image, 'upload_date':[]}
        images = AnimalImage.objects.filter(upload_user=request.user)
        image_serializer = AnimalImageSerializer(images, many=True)
        for i in image_serializer.data:
            data[f'{i["animal"]}']['images']=[]
        for i in image_serializer.data:
            data[f'{i["animal"]}']['upload_date'].append(i["upload_date"])
            data[f'{i["animal"]}']['images'].append(i["upload_image"])
            data[f'{i["animal"]}']['encyclopedia'] = True
    else:
        data = {'message': '본인만 확인 가능'}
    return Response(data)

@api_view(['GET'])
def find_id(request, nickname):
    User = get_user_model()
    if User.objects.filter(nickname=nickname).exists():
        user = User.objects.get(nickname=nickname)
        if user.register_login_method == 'Kakao':
            return Response({'login_method': '카카오 로그인 회원은 카카오 아이디 찾기 후 카카오 로그인하기를 이용해 주십시오.'})
        else:
            serializer = UserSerializer(user)
            email = serializer.data.get('email')
            userId, domain = email.split('@')
            return JsonResponse({'email': userId[:3]+'*'*(len(userId)-3) +'@'+ domain[:3]+'*'*(len(domain)-3)})
    return JsonResponse({'message':'Error'})

@api_view(['POST'])
def social_signup(request):
    nickname = request.data['nickname']
    username = nickname + str(request.data['username'])
    User = get_user_model()
    if User.objects.filter(nickname=nickname).exists(): # DB에 존재하는 경우 로그인
        user = User.objects.get(nickname=nickname)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        serializer = UserSerializer(user)
        return Response({'message':'기존 카카오 회원 로그인', 'token': AuthToken.objects.create(user)[1], 'user': serializer.data })
    else: # DB에 존재하지 않는 경우
        return Response({'new': {'username': username, 'nickname': nickname, 'email':request.data['email']}})
    return Response({'message' : 'Error'})

@api_view(['POST'])
def new_kakao(request):
    User = get_user_model()
    pwd = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
    new_user = User.objects.create(username=request.data['username'], password=pwd, nickname=request.data['nickname'], email=request.data['email'], register_login_method="Kakao") 
    login(request, new_user, backend="django.contrib.auth.backends.ModelBackend")
    serializer = UserSerializer(new_user)
    return Response({'message':'신규 카카오 회원 로그인', "token": AuthToken.objects.create(new_user)[1], 'user': serializer.data})
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    User = get_user_model()
    user = User.objects.get(username=username)
    if user == request.user:
            # 비밀번호 변경
        if request.method == 'PUT':
            current_pw = request.data.get('password')
            new_pw1 = request.data.get('newpassword')
            new_pw2 = request.data.get('checkpassword')
            if check_password(current_pw, user.password):
                if new_pw1 == new_pw2:
                    user.set_password(new_pw1)
                    user.save()
                    serializer = UserSerializer(instance=user)
                    return Response({'message' : 'Success', 'user': serializer.data})
                else:
                    return Response({'error' : '새 비밀번호를 확인해 주세요.'})
            else:
                return Response({'error' : '기존 비밀번호를 확인해 주세요.'})
        # 회원 탈퇴
        elif request.method == 'DELETE':
            if request.user == user:
                user.delete()
                return Response({'message' : 'Delete user'})
            return Response({'error' : '본인만 탈퇴할 수 있습니다.'})
        return Response({'error' : 'Error'})
    return Response({'error' : '회원 정보가 존재하지 않습니다.'})

class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        images = AnimalImage.objects.filter(upload_user=request.user)
        image_serializer = AnimalImageSerializer(images, many=True)
        user_serializer = UserSerializer(user)
        
        animal_id = []
        for i in image_serializer.data:
            animal_id.append(i["animal"])
        cnt = len(set(animal_id))
        data = user_serializer.data
        data['total_ency'] = cnt
        return Response(data)

import string
import random
from django.core.mail import send_mail

def email_auth_num(): # 랜덤 8자리 생성
    LENGTH = 8
    string_pool = string.ascii_letters + string.digits
    auth_num = ""
    for i in range(LENGTH):
        auth_num += random.choice(string_pool)
    return auth_num

def contents(new_password,username,email):
    char = username+"("+email+")"+"님의 새로운 비밀번호는 "+"'"+new_password +"'" + " 입니다."
    # print(char)
    return char

@api_view(['GET'])
def change_password(request):
    User = get_user_model()
    email = request.GET.get('email')
    nickname = request.GET.get('nickname')
    if User.objects.filter(email=email).exists():
        user = get_object_or_404(User, email=email)
        if user.register_login_method == 'Kakao':
            return Response({'message': '카카오 로그인 회원은 비밀번호 재발급이 불가능합니다.'})
        else:
            if user.nickname == nickname:
                new_password = email_auth_num() # 새로운 비밀번호
                user.set_password(new_password)
                user.save()
                send_mail(
                    '안녕하십니까 수상한동물사전 에서 새로 발급한 비밀번호 입니다.', 
                    contents(new_password,user.username,email),
                    'dmswo708@naver.com',
                    [str(email)],
                    fail_silently=False,
                    )
                return JsonResponse({'message':'메일을 확인해주세요.'})
            else:
                JsonResponse({'message':'해당 닉네임은 존재하지 않습니다.'})
    else:
        return JsonResponse({'message':'해당 이메일은 존재하지 않습니다.'})