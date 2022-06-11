from jose import jwt, JWTError
from ninja.security import HttpBearer
from django.conf import settings
import time
from config.utils.schemas import UserPretinence

from user.models import MyUser

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            user_info = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        except JWTError:
            return {
                'token': 'unauthorized',
            }
        
        if user_info:
            return {
                'pk': str(user_info['pk']),
                'department': str(user_info['department']),
                'branch': str(user_info['branch']),
                'role': str(user_info['role']),
            }

def get_user_access_token(user: MyUser, user_pretinence: UserPretinence):
    token = jwt.encode(
        {
            'pk': str(user.pk),
            'department': str(user_pretinence.department),
            'branch': str(user_pretinence.branch),
            'role': str(user_pretinence.role),
            'claims':{
                "exp": round( time.time() ) + 604800
            }
        }, 
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )
    return {
        'access': str(token),
    }

def get_user_refresh_token(user: MyUser):
    token = jwt.encode(
        {
            'pk': str(user.pk),
            'claims':{
                "exp": round( time.time() ) + 864000
            }
        }, 
        key=settings.SECRET_KEY,
        algorithm='HS256'
    )
    return {
        'refresh': str(token),
    }