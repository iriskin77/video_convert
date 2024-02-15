from rest_framework import serializers
from .models import VideoFile


class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFile
        fields = ('id', 'filename', 'file', 'weight', 'height')





