# Generated by Django 4.1.2 on 2023-02-21 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_profile_delete_genres_delete_keywords_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='genre',
            field=models.CharField(max_length=500),
        ),
    ]
