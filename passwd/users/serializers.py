from rest_framework import serializers


class UserListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    uid = serializers.CharField(max_length=200)
    gid = serializers.CharField(max_length=200)
    comment = serializers.CharField(max_length=200)
    home = serializers.CharField(max_length=200)
    shell = serializers.CharField(max_length=200)
