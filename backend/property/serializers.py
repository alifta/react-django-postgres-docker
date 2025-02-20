"""
Serializers for the property API.
"""

from rest_framework import serializers
from core.models import Property, Address, Appliance, User


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address objects."""

    class Meta:
        model = Address
        fields = (
            "id",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "country",
            "postal_code",
            "latitude",
            "longitude",
        )
        read_only_fields = ("id",)


class ApplianceSerializer(serializers.ModelSerializer):
    """Serializer for Appliance objects."""

    class Meta:
        model = Appliance
        fields = (
            "id",
            "name",
            "description",
            "brand",
            "model",
            "serial_number",
        )
        read_only_fields = ("id",)


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property objects."""

    # Nest address and appliances similar to tags and ingredients in the recipe serializer.
    address = AddressSerializer(required=False, allow_null=True)
    appliances = ApplianceSerializer(many=True, required=False)
    # Represent the owner with their primary key.
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # Expose computed lot_area in square feet.
    lot_area_square_feet = serializers.FloatField(read_only=True)

    class Meta:
        model = Property
        fields = (
            "property_id",
            "title",
            "description",
            "property_type",
            "address",
            "owner",
            "price",
            "is_available",
            "is_published",
            "lot_area",
            "floor_area",
            "ceiling_height",
            "num_floors",
            "num_rooms",
            "num_bathrooms",
            "num_parking",
            "open_parking",
            "covered_parking",
            "year_built",
            "tax_assessed_value",
            "tax_annual_amount",
            "appliances",
            "notes",
            "created_at",
            "updated_at",
            "lot_area_square_feet",
        )
        read_only_fields = (
            "property_id",
            "created_at",
            "updated_at",
            "lot_area_square_feet",
        )

    def _get_or_create_address(self, address_data):
        """Handle creating an Address from nested data."""
        return Address.objects.create(**address_data)

    def _get_or_create_appliances(self, appliances_data, property_instance):
        """Handle getting or creating appliances and associating them with the property."""
        for appliance in appliances_data:
            # Attempt to use the serial_number as a unique identifier; fall back to name.
            serial_number = appliance.get("serial_number")
            if serial_number:
                appliance_obj, created = Appliance.objects.get_or_create(
                    serial_number=serial_number, defaults=appliance
                )
            else:
                appliance_obj, created = Appliance.objects.get_or_create(
                    name=appliance.get("name"), defaults=appliance
                )
            property_instance.appliances.add(appliance_obj)

    def create(self, validated_data):
        address_data = validated_data.pop("address", None)
        appliances_data = validated_data.pop("appliances", [])
        property_instance = Property.objects.create(**validated_data)
        if address_data:
            address_obj = self._get_or_create_address(address_data)
            property_instance.address = address_obj
            property_instance.save()
        if appliances_data:
            self._get_or_create_appliances(appliances_data, property_instance)
        return property_instance

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)
        appliances_data = validated_data.pop("appliances", None)

        # Update simple fields.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if address_data is not None:
            if instance.address:
                # Update the existing address.
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                instance.address = self._get_or_create_address(address_data)

        if appliances_data is not None:
            # Clear and reassign appliances.
            instance.appliances.clear()
            self._get_or_create_appliances(appliances_data, instance)

        instance.save()
        return instance
