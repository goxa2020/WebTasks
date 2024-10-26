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
        fields = ('id', 'name', 'color', 'slug')
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
    tags = TagSerializer(read_only=True, many=True)
    author = ReadUserSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tags',
            'text',
            'author',
            'name',
            'deadline'
        )
        model = Task


class CreateTaskSerializer(serializers.ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = ReadUserSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tags',
            'text',
            'author',
            'name',
            'deadline'
        )
        model = Task

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        author = self.context.get('request').user
        recipes = Recipe.objects.create(author=author, **validated_data)
        recipes.tags.set(tags_data)
        return recipes

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        recipes = super().update(instance, validated_data)
        recipes.tags.set(tags_data)
        return recipes

    def validate(self, data):
        if self.context['request'].method == 'POST':
            data.pop('user', None)
        return data

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            duplicates = set(tag for tag in tags if tags.count(tag) > 1)
            raise serializers.ValidationError(
                'Тэги должны быть уникальны! Дубликаты: '
                f'{", ".join(duplicates)}.'
            )
        return tags

    def to_representation(self, instance):
        return TaskSerializer(instance, context=self.context).data
