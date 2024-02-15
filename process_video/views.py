from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VideoFile
from .serializers import VideoFileSerializer
from rest_framework.generics import ListAPIView
from .process import get_width_height_video, change_video_resolution
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
import threading
# Create your views here.


class ListApiFiles(ListAPIView):

    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer


class FileApi(APIView):

    parser_classes = (MultiPartParser,)

    def get(self, request, pk=None):

        video = VideoFile.objects.get(pk=pk)
        serialized_data = VideoFileSerializer(video)

        return Response({'id': serialized_data.data['id'],
                         'filename': serialized_data.data['filename'],
                         'is_processing': serialized_data.data['is_processing'],
                         'processing_success': serialized_data.data['processing_success']})

    def post(self, request):

        serialized_data = VideoFileSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"id": serialized_data.data['id']})

        return Response({"Result": status.HTTP_500_INTERNAL_SERVER_ERROR, "Error": serialized_data.errors})

    def delete(self, request, pk=None):

        if pk is not None:
            video = VideoFile.objects.get(pk=pk)
            video.delete()
            return Response({'success': True})

        return Response({'success': False})


@api_view(['PATCH'])
def patch_resolution(request, pk):
    video_file = VideoFile.objects.get(pk=pk)
    serializer = VideoFileSerializer(instance=video_file, data=request.data, partial=True)
    if serializer.is_valid():
        path = video_file.file.path
        weight: int = serializer.validated_data['weight']
        height: int = serializer.validated_data['height']
        thread = threading.Thread(target=change_video_resolution, args=[path, weight, height, pk])
        thread.start()
        return Response({'success': 200})

    return Response({'error': serializer.errors})
