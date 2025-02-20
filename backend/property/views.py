"""
Views for the property APIs.
"""

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Property, Amenity, PropertyPhoto
from property import serializers


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="property_type",
                type=OpenApiTypes.STR,
                description="Filter by property type (e.g., house, apartment, condo, townhouse)",
            ),
        ]
    )
)
class PropertyViewSet(viewsets.ModelViewSet):
    """View for managing property APIs."""

    queryset = Property.objects.all()
    serializer_class = serializers.PropertySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve properties for the authenticated owner, optionally filtering by property type."""
        property_type = self.request.query_params.get("property_type")
        queryset = self.queryset
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        return (
            queryset.filter(owner=self.request.user).order_by("-property_id").distinct()
        )

    def get_serializer_class(self):
        """Return the appropriate serializer class based on action."""
        if self.action == "list":
            return serializers.PropertySerializer
        if self.action == "upload_photo":
            return serializers.PropertyPhotoSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Assign the authenticated user as the owner when creating a property."""
        serializer.save(owner=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-photo")
    def upload_photo(self, request, pk=None):
        """Upload a photo to a property."""
        property_obj = self.get_object()
        serializer = self.get_serializer(property_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AmenityViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage amenities in the database."""

    queryset = Amenity.objects.all()
    serializer_class = serializers.AmenitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter amenities by an 'assigned_only' query parameter.
        Note: Amenity is not user-specific in the model, so we list all by default.
        """
        assigned_only = bool(int(self.request.query_params.get("assigned_only", 0)))
        queryset = self.queryset
        if assigned_only:
            # Assuming amenities linked to properties via the PropertyAmenity junction.
            queryset = queryset.filter(amenity_properties__isnull=False)
        return queryset.order_by("-name").distinct()


class PropertyPhotoViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Manage property photo uploads."""

    queryset = PropertyPhoto.objects.all()
    serializer_class = serializers.PropertyPhotoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Limit photos to properties owned by the authenticated user."""
        return self.queryset.filter(property__owner=self.request.user)
