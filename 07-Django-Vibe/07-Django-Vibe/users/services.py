# users/services.py
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserCreateSerializer

User = get_user_model()

class UserService:
    def __init__(self):
        self.user_model = User
        self.user_serializer = UserSerializer
        self.user_create_serializer = UserCreateSerializer

    def get_user_by_id(self, user_id):
        try:
            return self.user_model.objects.get(pk=user_id)
        except self.user_model.DoesNotExist:
            return None

    def create_user(self, user_data):
        serializer = self.user_create_serializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return user

    def get_user_profile(self, user):
        serializer = self.user_serializer(user)
        return serializer.data

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def authenticate_user(self, email, password):
        try:
            user = self.user_model.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
        except self.user_model.DoesNotExist:
            pass
        return None

# Example of how to use UserService (in a view or elsewhere):
# user_service = UserService()
# user = user_service.create_user({'email': 'test@example.com', 'password': 'password123', ...})
# tokens = user_service.generate_tokens(user)
