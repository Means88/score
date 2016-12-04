from rest_framework import viewsets
from score.models import Album, Score
from score.serializers import AlbumSerializer, ScoreSerializer


class AlbumViewset(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ScoreViewset(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
