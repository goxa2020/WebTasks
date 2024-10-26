from django_filters.rest_framework import FilterSet, filters

from recipes.models import Task


class TaskFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')


    class Meta:
        model = Task
        fields = ('tags', 'author', 'name')
