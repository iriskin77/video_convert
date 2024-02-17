import threading
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView
from .models import VideoFile
from .serializers import VideoFileSerializer
from .process import change_video_resolution
# Create your views here.


class ListApiFiles(ListAPIView):

    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer


class FileApi(APIView):

    parser_classes = (MultiPartParser, JSONParser)

    def get(self, request, pk):
        """""Получить файл по его uuid"""""
        try:
            video = VideoFile.objects.get(pk=pk)
            serialized_data = VideoFileSerializer(video)

            return Response({'id': serialized_data.data['id'],
                         'filename': serialized_data.data['filename'],
                         'is_processing': serialized_data.data['is_processing'],
                         'processing_success': serialized_data.data['processing_success']})

        except Exception as ex:
            return Response({'error': str(ex)})

    def post(self, request):
        """""Загрузить файл"""""
        serialized_data = VideoFileSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()
            return Response({"id": serialized_data.data['id']})

        return Response({"error": serialized_data.errors})

    def patch(self, request, pk):
        """""Изменить разрешение файла"""""
        try:
            video_file = VideoFile.objects.get(pk=pk)
            serializer = VideoFileSerializer(instance=video_file, data=request.data, partial=True)

            if serializer.is_valid():
                path = video_file.file.path
                width: int = serializer.validated_data['width']
                height: int = serializer.validated_data['height']
                thread = threading.Thread(target=change_video_resolution, args=[path, width, height, pk])
                thread.start()
                serializer.save()
                return Response({'success': 200})

            return Response({'error': serializer.errors})

        except Exception as ex:
            return Response({'error': str(ex)})

    def delete(self, request, pk):
        """""Удалить файл по его uuid"""""
        try:
            video = VideoFile.objects.get(pk=pk)
            video.delete()
            return Response({'success': True})

        except Exception as ex:
            return Response({'error': str(ex)})
