from rest_framework import serializers
from .models import VideoFile
from .process import get_width_height_video


class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFile
        fields = ('id', 'filename', 'file', 'width', 'height', 'is_processing', 'processing_success')

    def create(self, validated_data):
        new_video = VideoFile.objects.create(**validated_data)
        new_video.save()
        width, height = get_width_height_video(file_path=new_video.file.path)
        new_video.width = width
        new_video.height = height
        new_video.save()
        return new_video
