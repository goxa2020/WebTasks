from django_filters.rest_framework import FilterSet

from recipes.models import Task


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = ('tag', 'author', 'name')