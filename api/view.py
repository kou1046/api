import sys 
from io import BytesIO
import base64
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from itertools import groupby
from .models import *
from .serializer import *
import matplotlib.pyplot as plt 
import matplotlib

sys.path.append('.')
from packages.mycommon import myplot

matplotlib.use('AGG')
for k, v in myplot.get_my_rcparams().items(): plt.rc(k, **v)

class FrameListAPIView(views.APIView):
    def get(self, request, pk,  *args, **kwargs):
        frames = CombinedFrame.objects.filter(frame=pk)
        serializer = FrameListSerializer(frames)
        res = serializer.data
        return Response(res)
    
class PersonAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    @action(detail=True, methods=['get'])
    def img(self, request, pk):
        person = self.queryset.get(pk=pk)
        return Response(person.img_base64)
    @action(detail=True, methods=['get'])
    def screenimg(self, request, pk):
        person = self.queryset.get(pk=pk)
        return Response(person.get_visualized_screen_img(color=(0, 0, 255), isbase64=True))
    
class WDTeacherViewSet(viewsets.ModelViewSet):
    queryset = WDTeacher.objects.all()
    serializer_class = WDTeacherSerializer
    @action(detail=False, methods=['get'])
    def distribution(self, request):
        teachers = WDTeacher.objects.select_related('person').order_by('label')
        label_teachers_map = [WDTeacherSerializer(v, many=True).data
                              for k, v in groupby(teachers, lambda x:x.label)]
        return Response(label_teachers_map)
    @action(detail=False, methods=['get'])
    def add(self, request):
        people = Person.objects.exclude(id__in=WDTeacher.objects.values_list('person__id', flat=True),
                                        frame__frame__gte=30000, 
                                        frame__frame__lte=150000)\
                               .order_by('?')[:50]
        return Response(PersonSerializer2(people, many=True).data)
    
class PTeacherViewSet(viewsets.ModelViewSet):
    queryset = PTeacher.objects.all()
    serializer_class = PTeacherSerializer
    @action(detail=False, methods=['get'])
    def distribution(self, request):
        teachers = PTeacher.objects.select_related('person').order_by('label')
        label_teachers_map = [PTeacherSerializer(v, many=True).data
                              for k, v in groupby(teachers, lambda x:x.label)]
        return Response(label_teachers_map)
    @action(detail=False, methods=['get'])
    def add(self, request):
        people = Person.objects.exclude(id__in=PTeacher.objects.values_list('person__id', flat=True),
                                        frame__frame__gte=30000, 
                                        frame__frame__lte=150000)\
                               .order_by('?')[:50]
        return Response(PersonSerializer2(people, many=True).data)

class WTHTeacherViewSet(viewsets.ModelViewSet):
    queryset = WTHTeacher.objects.all()
    serializer_class = WTHTeacherSerializer
    @action(detail=False, methods=['get'])
    def distribution(self, request):
        teachers = WTHTeacher.objects.select_related('person').order_by('label')
        label_teachers_map = [WTHTeacherSerializer(v, many=True).data
                              for k, v in groupby(teachers, lambda x:x.label)]
        return Response(label_teachers_map)
        
    @action(detail=False, methods=['get'])
    def add(self, request):
        people = Person.objects.exclude(id__in=WTHTeacher.objects.values_list('person__id', flat=True),
                                        frame__frame__gte=30000, 
                                        frame__frame__lte=150000)\
                               .order_by('?')[:50]
        return Response(PersonSerializer2(people, many=True).data)
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer