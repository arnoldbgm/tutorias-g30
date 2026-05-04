# addresses/services.py
from .models import Address
from .serializers import AddressSerializer

class AddressService:
    def __init__(self):
        self.address_model = Address
        self.address_serializer = AddressSerializer

    def get_user_addresses(self, user):
        addresses = self.address_model.objects.filter(user=user)
        serializer = self.address_serializer(addresses, many=True)
        return serializer.data

    def create_address(self, user, address_data):
        serializer = self.address_serializer(data=address_data)
        serializer.is_valid(raise_exception=True)
        address = serializer.save(user=user)
        return address

    def update_address(self, address, address_data):
        serializer = self.address_serializer(address, data=address_data, partial=True)
        serializer.is_valid(raise_exception=True)
        address = serializer.save()
        return address

    def delete_address(self, address):
        address.delete()

    def set_default_address(self, user, address_id):
        # First, unset any existing default address for the user
        self.address_model.objects.filter(user=user, is_default=True).update(is_default=False)
        # Then, set the new address as default
        try:
            address = self.address_model.objects.get(user=user, pk=address_id)
            address.is_default = True
            address.save()
            return address
        except self.address_model.DoesNotExist:
            return None

# Example usage:
# from users.models import User
# address_service = AddressService()
# user = User.objects.get(pk=1)
# addresses = address_service.get_user_addresses(user)
# new_address = address_service.create_address(user, {...})
