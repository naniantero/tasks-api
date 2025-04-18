# Generated by Django 5.2 on 2025-04-11 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RewardInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('redeemed', 'Redeemed')], default='pending', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RewardTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('credits', models.PositiveIntegerField(default=0)),
                ('priority', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
