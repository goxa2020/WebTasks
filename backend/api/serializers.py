from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField



from recipes.models import (
    Task,
    Tag,
    User,
)


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = (
            'username',
            'id',
            'fio',
            'password',
        )
        model = User


class ReadUserSerializer(UserSerializer):
    class Meta:
        fields = (
            'username',
            'id',
            'fio',
        )
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color')
        model = Tag


class DefaultTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'deadline',
        )


class TaskSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True, many=False)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tag',
            'text',
            'author',
            'doer',
            'name',
            'deadline'
        )
        model = Task


class CreateTaskSerializer(serializers.ModelSerializer):
    tag = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=False)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tag',
            'text',
            'author',
            'doer',
            'name',
            'deadline'
        )
        model = Task

    def create(self, validated_data):
        author = validated_data.pop('author', None)
        if not author:
            return
        recipes = Task.objects.create(author=author, **validated_data)
        return recipes

    def validate(self, data):
        if self.context['request'].method == 'POST':
            data.pop('user', None)
        return data

    def to_representation(self, instance):
        return TaskSerializer(instance, context=self.context).data