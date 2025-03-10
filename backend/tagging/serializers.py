from rest_framework import serializers
from recipes.models import Ingredient, Recipe
from tags.models import Tag, TaggedItem


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag objects."""

    class Meta:
        model = Tag
        fields = ["id", "tag_name"]
        read_only_fields = ["id"]
