# Generated by Django 4.1.2 on 2023-02-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_tempprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('release_date', models.DateField(default='1970-01-01')),
                ('genre', models.CharField(max_length=200)),
                ('platforms', models.CharField(max_length=50)),
                ('developer', models.CharField(max_length=50)),
                ('esrb_rating', models.CharField(max_length=50)),
                ('esrbs', models.CharField(max_length=100)),
                ('metascore', models.IntegerField()),
                ('userscore', models.DecimalField(decimal_places=1, max_digits=3)),
                ('num_players', models.CharField(max_length=50)),
                ('summary', models.TextField()),
            ],
        ),
    ]
