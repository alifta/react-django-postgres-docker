"""
Views for the recipe APIs.
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

from core.models import Ingredient, Recipe, Tag
from recipe import serializers


@extend_schema_view(
    list=extend_schema(
        # summary="List all recipes",
        parameters=[
            OpenApiParameter(
                name="tags",
                type=OpenApiTypes.STR,
                description="Comma separated list of tag IDs to filter recipes",
            ),
            OpenApiParameter(
                name="ingredients",
                type=OpenApiTypes.STR,
                description="Comma separated list of ingredient IDs to filter recipes",
            ),
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        tags = self.request.query_params.get("tags")
        ingredients = self.request.query_params.get("ingredients")
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user).order_by("-id").distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer
        if self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="assigned_only",
                type=OpenApiTypes.INT,
                enum=[0, 1],
                description="Filter by items assigned to recipes.",
            )
        ]
    )
)
class BaseRecipeAttrViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Base viewset for recipe attributes."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(int(self.request.query_params.get("assigned_only", 0)))
        queryset = self.queryset

        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)

        return queryset.filter(user=self.request.user).order_by("-name").distinct()


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""

    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""

    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
