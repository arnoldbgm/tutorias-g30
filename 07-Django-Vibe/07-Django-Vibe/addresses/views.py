# addresses/views.py
from rest_framework import viewsets, permissions
from .models import Address
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows addresses to be viewed or edited.
    Users can only manage their own addresses.
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the addresses for
        the currently authenticated user.
        """
        user = self.request.user
        return Address.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        Associate the address with the current user upon creation.
        """
        serializer.save(user=self.request.user)
