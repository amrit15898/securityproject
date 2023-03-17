from rest_framework import serializers


class AvalancheUpload(serializers.Serializer):
    file = serializers.FileField()

