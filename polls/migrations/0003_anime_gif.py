# Generated by Django 4.0.4 on 2022-05-15 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_video_shiftid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anime_gif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='')),
            ],
        ),
    ]
