from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    Tag,
    User,
)


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        fields = (
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'password',
        )
        model = User


class ReadUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'username',
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and author.subscribing.filter(user=user).exists()
        )


class SubscribeSerializer(ReadUserSerializer):
    recipes_count = SerializerMethodField(
        method_name='get_recipes_count', read_only=True
    )
    recipes = SerializerMethodField()

    class Meta(ReadUserSerializer.Meta):
        fields = (
            *ReadUserSerializer.Meta.fields,
            'recipes_count',
            'recipes',
        )
        read_only_fields = ('email', 'username', 'last_name', 'first_name')

    def get_recipes_count(self, user):
        return user.recipes.count()

    def get_recipes(self, user):
        recipes_limit = int(
            self.context['request'].query_params.get('recipes_limit', 10**10)
        )
        return DefaultRecipeSerializer(
            user.recipes.all()[:recipes_limit],
            many=True,
        ).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class ReadIngredientRecipeSerializer(serializers.ModelSerializer):
    id = IntegerField(write_only=True)
    amount = IntegerField(required=True)
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount', 'name', 'measurement_unit')

    def get_measurment_unit(self, ingredient):
        return ingredient.ingredient.measurement_unit

    def get_name(self, ingredient):
        return ingredient.ingredient.name


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.ReadOnlyField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class DefaultRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = ReadUserSerializer(read_only=True)
    image = Base64ImageField(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True, read_only=True, source='recipe_ingredients'
    )
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tags',
            'text',
            'image',
            'author',
            'name',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'cooking_time',
        )
        model = Recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and request.user.shopping_cart.filter(
                recipe=obj, user=request.user
            ).exists()
        )


class CreateRecipeSerializer(serializers.ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    author = ReadUserSerializer(read_only=True)
    ingredients = ReadIngredientRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'pub_date',
            'tags',
            'text',
            'image',
            'author',
            'name',
            'ingredients',
            'cooking_time',
        )
        model = Recipe

    @staticmethod
    def fill_recipe_ingredients(recipes, ingredients_data):
        recipes.ingredients.clear()
        recipes_ingredients = [
            IngredientInRecipe(
                recipes=recipes,
                ingredient_id=ingredient_data['id'],
                amount=ingredient_data['amount'],
            )
            for ingredient_data in ingredients_data
        ]
        IngredientInRecipe.objects.bulk_create(recipes_ingredients)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        author = self.context.get('request').user
        recipes = Recipe.objects.create(author=author, **validated_data)
        recipes.tags.set(tags_data)
        self.fill_recipe_ingredients(recipes, ingredients_data)
        return recipes

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)
        recipes = super().update(instance, validated_data)
        recipes.tags.set(tags_data)
        self.fill_recipe_ingredients(recipes, ingredients_data)
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

    @staticmethod
    def validate_unique_ingredients(ingredients):
        if len(ingredients) != len(
            set(tuple(ingredient.items()) for ingredient in ingredients)
        ):
            duplicates = set(
                [
                    tuple(sorted(sort.items()))
                    for sort in ingredients
                    if ingredients.count(sort) > 1
                ]
            )
            raise serializers.ValidationError(
                (
                    f'Приорететы должны быть уникальными. Дубликаты: '
                    f'{duplicates}'
                )
            )
        return ingredients

    def validate_ingredients(self, ingredients):
        if not isinstance(ingredients, list):
            raise serializers.ValidationError('Приорететы должны быть списком.')
        return self.validate_unique_ingredients(ingredients)

    def validate_image(self, image):
        if not image:
            raise serializers.ValidationError(
                'Изображение не должно быть пустым'
            )
        return image

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data
