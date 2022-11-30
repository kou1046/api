import json     
from rest_framework import status, views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import *
from .serializer import *

class FrameListAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        frames = CombinedFrame.objects.filter(frame=3, group__name='G3')
        serializer = FrameListSerializer(frames)
        res = serializer.data
        print(args)
        return Response(res)
    
class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer