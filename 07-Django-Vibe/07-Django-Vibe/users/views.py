from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer, JWTCustomTokenObtainPairSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Handles user registration, login, and profile management.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # Default for ModelViewSet, requires admin for full CRUD

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'register':
            self.permission_classes = [AllowAny]
        elif self.action == 'login':
            self.permission_classes = [AllowAny]
        elif self.action == 'profile':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
             self.permission_classes = [IsAdminUser] # Only admins can list, retrieve, update, or destroy other users
        return super().get_permissions()

    def get_object(self):
        """
        Returns the object that the view is displaying.
        By default this is set to the currently authenticated user for profile actions.
        """
        if self.action == 'profile':
            return self.request.user
        return super().get_object()

    def get_serializer_class(self):
        """
        Returns the serializer class to use for a given action.
        """
        if self.action == 'register':
            return UserCreateSerializer
        elif self.action == 'login':
            return UserLoginSerializer # Using a custom serializer for login to validate credentials
        elif self.action == 'profile':
            return UserSerializer # Standard serializer for viewing/updating own profile
        elif self.action == 'create': # This would be for admin creating users
            return UserCreateSerializer
        return UserSerializer # Default serializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Handles user registration.
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Optionally, you could log the user in automatically here or return a token
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Handles user login.
        Returns JWT tokens upon successful authentication.
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Generate JWT tokens
            token_serializer = JWTCustomTokenObtainPairSerializer()
            token_data = token_serializer.for_user(user) # Use custom method to get tokens
            
            # Combine user details with tokens
            response_data = {
                'user': UserSerializer(user).data,
                'tokens': token_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        Returns the profile of the currently authenticated user.
        """
        user = request.user
        serializer = self.get_serializer_class()(user)
        return Response(serializer.data)

    # Override default create/update/destroy to ensure only admins can manage other users
    def create(self, request, *args, **kwargs):
        # Admins can create users
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # Ensure only admin can update other users, or user can update their own profile (excluding sensitive fields)
        if instance != request.user and not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer_class()(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(instance).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        # Admins can delete users
        instance = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

# Placeholder for other app views
# Example: AddressViewSet
# from addresses.models import Address
# from .serializers import AddressSerializer
# class AddressViewSet(viewsets.ModelViewSet):
#     queryset = Address.objects.all()
#     serializer_class = AddressSerializer
#     permission_classes = [IsAuthenticated] # Example permission

#     def get_queryset(self):
#         # Filter addresses to only show those belonging to the current user
#         if self.request.user.is_authenticated:
#             return Address.objects.filter(user=self.request.user)
#         return Address.objects.none()
