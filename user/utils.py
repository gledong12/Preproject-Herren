import jwt
import json

from django.http   import JsonResponse
from subscribe_email.my_settings  import SECRET_KEY, ALGORITHM

from user.models  import User


def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization', None)
            if not access_token:
                request.user = None
                return func(self, request, *args, **kwargs)
            payload         = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            login_user      = User.objects.get(id=payload['user_id'])
            request.user    = login_user
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
    return wrapper

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            print('111111111111111111')
            print(request.headers)
            access_token = request.headers.get('authorization')
            
            payload      = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            login_user   = User.objects.get(id=payload['user_id'])
            request.user = login_user
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
    return wrapper
