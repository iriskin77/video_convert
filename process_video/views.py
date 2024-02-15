from rest_framework.response import Response
from rest_framework import status
from .models import VideoFile
from .serializers import VideoFileSerializer
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
# Create your views here.


class ListApiFiles(ListAPIView):

    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer


class FileApi(APIView):

    parser_classes = (MultiPartParser,)

    def get(self, request, pk, *args, **kwargs):
        #pk = self.kwargs['pk']
        video = VideoFile.objects.filter(pk=pk)
        serialized_data = VideoFileSerializer(data=video)
        if serialized_data.is_valid():
            return Response({'id': serialized_data.validated_data['id'],
                             'processing': serialized_data.validated_data['processing'],
                             'processing_success': serialized_data.validated_data['processing_success']})
        else:
            return Response({'error': serialized_data.errors})

    def post(self, request):

        serialized_data = VideoFileSerializer(data=request.data)

        if serialized_data.is_valid():
            serialized_data.save()

            return Response({"response status": status.HTTP_201_CREATED})
        else:
            return Response({"Result": status.HTTP_500_INTERNAL_SERVER_ERROR, "Error": serialized_data.errors})
