from django.contrib import admin
from score.models import Album, Score


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class ScoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'artist')


admin.site.register(Album, AlbumAdmin)
admin.site.register(Score, ScoreAdmin)
