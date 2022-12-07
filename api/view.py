import json     
from rest_framework import status, views
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import glob 
from .models import *
from .serializer import *

class FrameListAPIView(views.APIView):
    def get(self, request, pk,  *args, **kwargs):
        frames = CombinedFrame.objects.filter(frame=pk)
        serializer = FrameListSerializer(frames)
        res = serializer.data
        return Response(res)
    
class WDTeacherListApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        return ret 
    queryset = WDTeacher.objects.all()
    serializer_class = WDTeacherSerializer

class WTHTeacherListApiView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        ret = super().get(request, *args, **kwargs)
        return ret 
    queryset = WTHTeacher.objects.all()
    serializer_class = WDTeacherSerializer

class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer