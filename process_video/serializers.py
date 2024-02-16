from rest_framework import serializers
from .models import VideoFile
from .process import get_width_height_video, change_video_resolution
import os
import threading


class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFile
        fields = ('id', 'filename', 'file', 'weight', 'height', 'is_processing', 'processing_success')

    def create(self, validated_data):
        new_video = VideoFile.objects.create(**validated_data)
        new_video.save()
        print(new_video.file.path)
        weight, height = get_width_height_video(file_path=new_video.file.path)
        new_video.weight = weight
        new_video.height = height
        new_video.save()
        return new_video
