# Generated by Django 5.2 on 2025-04-11 10:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='taskinstance',
            name='assignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_instances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tasktemplate',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_templates', to='users.group'),
        ),
        migrations.AddField(
            model_name='taskinstance',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='tasks.tasktemplate'),
        ),
    ]
