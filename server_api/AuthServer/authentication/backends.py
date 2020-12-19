import jwt
from rest_framework import authentication,exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self,request):
        auth_data=authentication.get_authorization_header(request)
        print('=====auth_data는======',auth_data)
        print('=====auth_data는======',type(auth_data))
        if not auth_data:
            print('===아니란다')
            return None
        
        prefix,token=str(auth_data.decode('utf-8')).split(' ')
        
        print('====prefix====',prefix)
        print('====token=====',token)

        try:
            payload=jwt.decode(token,str(settings.JWT_SECRET_KEY))
            user=User.objects.get(username=payload['username'])
            return (user,token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid, login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired, login')
        return super().authenticate(request)