from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from recipes.models import Task, Tag, User


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'deadline',
        'tag',
    )
    fields = (
        'name',
        'author',
        'deadline',
        'tag',
        'text',
    )
    list_filter = ('author', 'tag')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'color_tag')

    @admin.display(description='цвет тэга')
    def color_tag(self, color_tag):
        return mark_safe(
            (
                '<div style="width: 20px; height: 20px; background-color:'
                f'{color_tag.color};"></div>'
            )
        )


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'fio',
        'count_tasks',
    )

    def count_tasks(self, count_tasks):
        return count_tasks.tasks.count()


admin.site.unregister(Group)