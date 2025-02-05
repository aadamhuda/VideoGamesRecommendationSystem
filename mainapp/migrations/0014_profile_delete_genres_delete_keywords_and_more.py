# Generated by Django 4.1.2 on 2023-02-20 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_alter_game_userscore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=500)),
                ('genre', models.CharField(max_length=150)),
                ('num_players_preference', models.CharField(max_length=50)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Genres',
        ),
        migrations.DeleteModel(
            name='Keywords',
        ),
        migrations.DeleteModel(
            name='TempProfile',
        ),
    ]
