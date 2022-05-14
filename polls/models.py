from django.db import models

# Create your models here.


class Video(models.Model):
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y")

    def __str__(self):
        return self.caption


class Telemetry(models.Model):
    id = models.TextField(primary_key=True)
    time = models.IntegerField()
    detectionProbability = models.FloatField()
    detectionCoordinates = models.JSONField()
    commentary = models.TextField()
    isSent = models.SmallIntegerField()
    videoName = models.TextField()
    createdAt = models.DateField()
    updatedAt = models.DateField()
    shiftId = models.TextField()


class Shift(models.Model):
    id = models.TextField(primary_key=True)
    filmingTime = models.JSONField()
    videos = models.JSONField()
    motion = models.JSONField()
    createdAt = models.DateField()
    updatedAt = models.DateField()


class Restoran(models.Model):
    id = models.TextField(primary_key=True)
    place = models.TextField()
    cams = models.JSONField()
