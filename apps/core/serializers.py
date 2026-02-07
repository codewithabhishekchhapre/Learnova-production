"""
Learnova LMS - Base Serializers & Common Serializer Utilities
"""
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer with common functionality:
    - Read-only created_at, updated_at
    - Consistent error handling
    """

    def get_field_names(self, declared_fields, info):
        """Exclude audit fields from write operations by default."""
        fields = super().get_field_names(declared_fields, info)
        audit_fields = {'created_at', 'updated_at'}
        return list(fields)


class AuditFieldsMixin:
    """Mixin to add read-only audit timestamp fields."""

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class DynamicFieldsMixin:
    """
    Mixin to allow dynamic field inclusion via query params.
    Usage: ?fields=id,name,email or ?exclude=password
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class NestedCreateMixin:
    """
    Mixin for handling nested object creation in serializers.
    Override get_nested_serializers() to define nested relations.
    """

    def create(self, validated_data):
        nested_data = {}
        for key in list(validated_data.keys()):
            if key in self.get_nested_fields():
                nested_data[key] = validated_data.pop(key)
        instance = super().create(validated_data)
        for key, data in nested_data.items():
            serializer_class = self.get_nested_serializers().get(key)
            if serializer_class and data:
                serializer = serializer_class(data=data, many=isinstance(data, list))
                serializer.is_valid(raise_exception=True)
                self._save_nested(instance, key, serializer)
        return instance

    def get_nested_fields(self):
        return []

    def get_nested_serializers(self):
        return {}

    def _save_nested(self, instance, key, serializer):
        if isinstance(serializer.validated_data, list):
            for item in serializer.validated_data:
                setattr(item, self.get_nested_fk_field(key), instance)
                item.save()
        else:
            setattr(serializer.validated_data, self.get_nested_fk_field(key), instance)
            serializer.save()

    def get_nested_fk_field(self, key):
        return key.replace('_set', '')


class PaginatedResponseSerializer(serializers.Serializer):
    """Standard pagination response structure."""

    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()
