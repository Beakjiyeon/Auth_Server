from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerialzier,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt, bcrypt
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django.contrib.auth import get_user_model
# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class=UserSerialzier
    def post(self,request):
        '''
        # 비밀번호를 암호화 하여 DB 저장
        password=(request.data)['password']
        # 암호화 (password 유니코드형식->바이트형식변환)
        salt=bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        # DB에 저장하기 위해 문자열로 변환
        (request.data)['password'] = hashed_password.decode('utf-8')
        '''
        serializer=UserSerialzier(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        data=request.data
        username=data.get('username','')
        password=data.get('password','')
        
        user=auth.authenticate(username=username,password=password)
        '''
        # DB에 저장된 패스워드 값
        db_password=User.objects.get(username=username).password
        # db 암호화된 비밀 번호와 비교해서 맞다면
        if bcrypt.checkpw(password.encode('utf-8'),db_password.encode('utf-8')):
        '''

        if user:
            print('========user있음=======')
            auth_token=jwt.encode({'username':user.username},str(settings.JWT_SECRET_KEY))
            print('=======있니?======',auth_token)
            serializer=UserSerialzier(user)

            # set cookie
            #response = HttpResponseRedirect(reverse('root'))
            #response.set_cookie(key='token', value=token, domain=settings.COOKIE_DOMAIN)
            #return response
        
            data={'user':serializer.data,'token':auth_token}

            response=Response(data, status=status.HTTP_200_OK)
            response.set_cookie(str(auth_token), user.id, expires=1000*60)

            return response

            # SEND RESPONSE
        else:
             print('========user없음=======')
        return Response({'detail': 'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)

class UserListView(ListCreateAPIView):
    
    serializer_class=UserSerialzier
    permission_classes=(permissions.IsAuthenticated,)
    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

        
    def get_queryset(self):
        User = get_user_model()
        users = User.objects.all()
        return users


class UserDetailView(RetrieveUpdateDestroyAPIView):
    
    serializer_class=UserSerialzier
    permission_classes=(permissions.IsAuthenticated,)
    lookup_field="username" # /admin/username

    def get_queryset(self):
        User = get_user_model()
        users = User.objects.all()
        return users