# Generated by Django 4.2.5 on 2024-10-26 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0005_remove_task_tags_task_tags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="tags",
        ),
        migrations.AddField(
            model_name="task",
            name="tag",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tasks",
                to="recipes.tag",
                verbose_name="тэг",
            ),
            preserve_default=False,
        ),
    ]
