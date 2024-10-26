from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import FileResponse

from api.filters import TaskFilter
from api.permissions import IsAuthorOrReadOnly
from api.pagination import LimitPageNumberPagination
from api.serializers import (
    CreateTaskSerializer,
    DefaultTaskSerializer,
    TaskSerializer,
    TagSerializer,
)
from recipes.models import (
    Tag,
    Task,
    User,
)


class UserView(UserViewSet):
    pagination_class = LimitPageNumberPagination


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TaskSerializer
        return CreateTaskSerializer


class TagViewSet(
    viewsets.ReadOnlyModelViewSet,
):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
