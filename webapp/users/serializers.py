from rest_framework import serializers


class StringListField(serializers.ListField):
    child = serializers.CharField()


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    uid = serializers.CharField(max_length=200)
    gid = serializers.CharField(max_length=200)
    comment = serializers.CharField(max_length=200)
    home = serializers.CharField(max_length=200)
    shell = serializers.CharField(max_length=200)


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    gid = serializers.CharField(max_length=200)
    members = StringListField()
