from dataclasses import fields

from rest_framework import serializers

from general import models


class StateSerializer(serializers.ModelSerializer):
    """Serializer for State Model"""

    class Meta:
        model = models.State
        fields = "__all__"
        read_only_fields = ["id"]


class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for District Model"""

    class Meta:
        model = models.District
        fields = "__all__"
        read_only_fields = ["id"]


class ProfessionSerializer(serializers.ModelSerializer):
    """Serializer for Profession Model"""

    class Meta:
        model = models.Profession
        fields = "__all__"
        read_only_fields = ["id"]
