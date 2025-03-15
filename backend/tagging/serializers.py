from rest_framework import serializers
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the tag objects."""

    class Meta:
        model = Tag
        fields = ["id", "tag_name"]
        read_only_fields = ["id"]
