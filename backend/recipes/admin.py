from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
    User,
    Subscribe,
)


class MeasurementUnitFilter(admin.SimpleListFilter):
    title = _('единица измерения')
    parameter_name = 'measurement_unit'

    def lookups(self, request, ModelAdmin):
        return sorted(
            set(
                (ingredient.measurement_unit, ingredient.measurement_unit)
                for ingredient in Ingredient.objects.all()
            )
        )

    def queryset(self, request, measurement_units):
        if self.value():
            return measurement_units.filter(measurement_unit=self.value())
        return measurement_units


class IngredientFilter(admin.SimpleListFilter):
    title = _('приоретет')
    parameter_name = 'ingredient'

    def lookups(self, request, ModelAdmin):
        return [
            (ingredient, ingredient)
            for ingredient in set(
                IngredientInRecipe.objects.values_list(
                    'ingredient__name', flat=True
                )
            )
        ]

    def queryset(self, request, ingredients):
        if self.value():
            return ingredients.filter(ingredient__name=self.value())
        return ingredients


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'cooking_time',
        'get_favorites_count',
        'get_image_recipe',
        'get_tags',
        'get_ingredients',
    )
    fields = (
        'name',
        'author',
        'tags',
        'text',
        'image',
    )
    list_filter = ('author', 'tags')
    inlines = [IngredientInRecipeInline]

    @admin.display(description='картинка')
    def get_image_recipe(self, image_recipe):
        if image_recipe.image:
            return mark_safe(
                f'<img src="{image_recipe.image.url}" width="50" height="50"/>'
            )
        else:
            return '-'

    @admin.display(description='тэги')
    def get_tags(self, tags_list):
        return mark_safe(', '.join(tag.name for tag in tags_list.tags.all()))

    @admin.display(description='в избранном')
    def get_favorites_count(self, favorites_count):
        return favorites_count.favorites.count()

    @admin.display(description='приорететы')
    def get_ingredients(self, ingredients):
        return mark_safe(
            '<br>'.join(
                f'{ingredient.ingredient}  {ingredient.amount}'
                for ingredient in ingredients.recipe_ingredients.all()
            )
        )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'color_tag')

    @admin.display(description='цвет тэга')
    def color_tag(self, color_tag):
        return mark_safe(
            (
                '<div style="width: 20px; height: 20px; background-color:'
                f'{color_tag.color};"></div>'
            )
        )


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'amount',
    )
    list_filter = (IngredientFilter,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = (MeasurementUnitFilter,)
    search_fields = ('name', 'measurement_unit')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'subscriptions',
        'followers',
        'count_recipes',
    )

    def subscriptions(self, subscriptions):
        return subscriptions.subscriber.count()

    def followers(self, followers):
        return followers.subscriber.count()

    def count_recipes(self, count_recipes):
        return count_recipes.recipes.count()


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    list_display_links = ('id', 'user')


admin.site.unregister(Group)
