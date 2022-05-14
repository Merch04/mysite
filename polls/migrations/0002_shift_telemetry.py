# Generated by Django 4.0.4 on 2022-05-14 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('filmingTime', models.JSONField()),
                ('videos', models.JSONField()),
                ('motion', models.JSONField()),
                ('createdAt', models.DateField()),
                ('updatedAt', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Telemetry',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('time', models.IntegerField()),
                ('detectionProbability', models.FloatField()),
                ('detectionCoordinates', models.JSONField()),
                ('commentary', models.TextField()),
                ('isSent', models.SmallIntegerField()),
                ('videoName', models.TextField()),
                ('createdAt', models.DateField()),
                ('updatedAt', models.DateField()),
                ('shiftId', models.TextField()),
            ],
        ),
    ]