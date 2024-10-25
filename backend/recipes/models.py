from api.validators import validate_bad_username, validate_username

from backend.settings import (
    LONG_CHARFIELD,
    MID_CHARFIELD,
    NAME_LEGNTH,
    SHORT_CHARFIELD,
)

from colorfield.fields import ColorField

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


TEXT_SIZE = 15


class User(AbstractUser):
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=20,
        validators=[validate_bad_username, validate_username],
    )

    fio = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fio']

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self) -> str:
        return self.username[:TEXT_SIZE]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='подписчик',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='преподователь',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('author',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_subscription'
            )
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


class Tag(models.Model):
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    color = ColorField(
        verbose_name="цвет",
        unique=True,
        validators=[
            RegexValidator(
                r'^#[0-9a-fA-F]{6}$',
                'Введите цвет в формате RGB, в формате #000000',
            )
        ],
    )
    slug = models.SlugField(
        max_length=SHORT_CHARFIELD,
        unique=True,
        verbose_name='читаемая часть URL',
    )

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    measurement_unit = models.CharField(
        max_length=200, verbose_name='единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'приоритет'
        verbose_name_plural = 'приорететы'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='name_unit_unique'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=NAME_LEGNTH, verbose_name='название')
    image = models.ImageField(upload_to='recipes/image', null=True, blank=True)
    text = models.TextField(verbose_name='описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='приорететы',
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='тэги'
    )
    cooking_time = models.CharField(max_length=NAME_LEGNTH, verbose_name='сроки выполнения')
    pub_date = models.DateTimeField('дата опубликации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'проект'
        verbose_name_plural = 'проекты'

    def __str__(self) -> str:
        return f'{self.name[:TEXT_SIZE]}, {self.author}'


class IngredientInRecipe(models.Model):
    recipes = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Количество должно быть больше 0.'),
        ],
        verbose_name=_('мера'),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipes', 'ingredient'], name='unique_combination'
            )
        ]
        verbose_name = 'приоретет в проекте'
        verbose_name_plural = 'приорететы в проекте'

    def __str__(self) -> str:
        return f'{self.recipes} - {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites'
    )

    class Meta:
        verbose_name = 'изрбанное'
        verbose_name_plural = 'избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique__favorites',
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'список проекта'
        verbose_name_plural = 'список проектов'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique__shopping_cart',
            )
        ]

    def get_shopping_cart_ingredients(self):
        ingredients = (
            IngredientInRecipe.objects.filter(recipes__shopping_cart=self)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(amount=models.Sum('amount'))
        )
        return ingredients

    def __str__(self):
        return f'{self.user} {self.recipe}'
