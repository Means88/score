from django.db import models
from jsonfield import JSONField


class Album(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title.encode('utf-8')

    def __unicode__(self):
        return self.title


class Score(models.Model):
    title = models.CharField(max_length=255)
    cover = models.URLField(blank=True)
    album = models.ForeignKey(Album, blank=True, null=True)
    description = models.TextField(blank=True)
    artist = models.CharField(max_length=255, blank=True)
    lyricist = models.CharField(max_length=255, blank=True)
    composer = models.CharField(max_length=255, blank=True)
    arranger = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    by = models.CharField(max_length=255, blank=True)
    tags = JSONField(blank=True, default=[])

    def __str__(self):
        return self.title.encode('utf-8')

    def __unicode__(self):
        return self.title
