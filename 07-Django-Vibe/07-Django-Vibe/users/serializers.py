from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, used for retrieving user details.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['email', 'is_active', 'is_staff', 'date_joined'] # Email should be unique and not updatable here

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    Includes password confirmation.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, label=_("Confirm password"), style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(_("The passwords must match."))
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login, using email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password) and user.is_active:
                attrs['user'] = user
                return attrs
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        return attrs

class JWTCustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for JWT token pair to include user's ID and name in the token payload.
    """
    @classmethod
    def for_user(cls, user):
        serializer = cls()
        token = serializer.get_token(user)
        data = {'refresh': str(token), 'access': str(token.access_token),}
        return data

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom claims to the token payload
        user = self.user # 'self.user' is set by the parent's validate method
        data['user'] = {
            'id': user.id,
            'full_name': user.get_full_name(),
            'email': user.email,
            'is_staff': user.is_staff,
        }
        return data

# Placeholder for other app serializers
# Example: AddressSerializer
# from addresses.models import Address
# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']
