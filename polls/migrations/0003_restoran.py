# Generated by Django 4.0.4 on 2022-05-14 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_shift_telemetry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restoran',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('place', models.TextField()),
                ('cams', models.JSONField()),
            ],
        ),
    ]
