from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser


# just to serve as a user object
class UserObject:
    def __init__(self, user_id):
        self.id = user_id
        self.is_authenticated = True
        
class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)

        if not auth or not auth.startswith('Bearer '):
            return None  # No authentication header, treat as anonymous

        try:
            token = auth.split(' ')[1]
            payload = UntypedToken(token).payload
            user_id = payload.get('user_id')

            # Simulate user or return AnonymousUser
            if not user_id:
                raise AuthenticationFailed("Invalid token: User ID not found")
            user = UserObject(user_id)
            return (user, None)
            
        except Exception as e:
            raise AuthenticationFailed(f"Invalid token: {str(e)}")

