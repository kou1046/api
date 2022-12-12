import json     
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import glob 
from .models import *
from .serializer import *

class FrameListAPIView(views.APIView):
    def get(self, request, pk,  *args, **kwargs):
        frames = CombinedFrame.objects.filter(frame=pk)
        serializer = FrameListSerializer(frames)
        res = serializer.data
        return Response(res)
    
class PersonAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    
class WDTeacherViewSet(viewsets.ModelViewSet):
    queryset = WDTeacher.objects.all()
    serializer_class = WDTeacherSerializer
    @action(detail=False, methods=['get'])
    def add(self, request):
        people = Person.objects.exclude(id__in=WDTeacher.objects.values_list('person__id', flat=True),
                                        frame__frame__gte=30000, 
                                        frame__frame__lte=150000)\
                               .order_by('?')[:50]
    
        return Response(PersonSerializer(people, many=True).data)

class WTHTeacherViewSet(viewsets.ModelViewSet):
    queryset = WTHTeacher.objects.all()
    serializer_class = WTHTeacherSerializer
    @action(detail=False, methods=['get'])
    def add(self, request):
        people = Person.objects.exclude(id__in=WTHTeacher.objects.values_list('person__id', flat=True),
                                        frame__frame__gte=30000, 
                                        frame__frame__lte=150000)\
                               .order_by('?')[:50]
    
        return Response(PersonSerializer(people, many=True).data)
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer