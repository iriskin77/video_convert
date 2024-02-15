from rest_framework import serializers
from .models import VideoFile
from .process import get_width_height_video
import os


class VideoFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = VideoFile
        fields = ('id', 'filename', 'file', 'weight', 'height', 'is_processing', 'processing_success')

    def create(self, validated_data):
        weight, height = get_width_height_video(file_path=validated_data['file'])
        validated_data['weight'] = weight
        validated_data['height'] = height
        return VideoFile.objects.create(**validated_data)



