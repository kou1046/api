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
    
class ReadOnlyFrameAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CombinedFrame.objects.all()
    serializer_class = ReadOnlyFrameSerializer
    def get_queryset(self):
        query_names = ["frame", "group"]
        filter_args = {}
        for name in self.request.query_params:
            if name in query_names:
                filter_args[name + "__name" if name == "group" else name] = self.request.query_params[name]
        return CombinedFrame.objects.filter(**filter_args)
    @action(detail=True, methods=["get"])
    def img(self, request, pk):
        return Response(CombinedFrame.objects.get(pk=pk).img_base64)
    
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
                                        frame__frame__lt=30000, 
                                        frame__frame__gt=150000)\
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
                                        frame__frame__lt=30000, 
                                        frame__frame__gt=150000)\
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
                                        frame__frame__lt=30000, 
                                        frame__frame__gt=150000)\
                               .order_by('?')[:50]
        return Response(PersonSerializer2(people, many=True).data)
    
class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    def get_queryset(self):
        query_names = ["frame", 'group']
        filter_args = {}
        for name in self.request.query_params:
            if name in query_names:
                if name == "frame":
                    key = name + "__frame"
                if name == "group":
                    key = name + "__name"
                filter_args[key] = self.request.query_params[name]
        return Device.objects.filter(**filter_args)
    @action(detail=True, methods=["get"])
    def screenshot(self, request, pk):
        return Response(Device.objects.get(pk=pk).drawn_screenshot_base64)
    
class MouseDragViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MouseDrag.objects.all()
    serializer_class = MouseDragSerializer
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class InferenceModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InferenceModel.objects.all()
    serializer_class = InferenceModelSerializer
    def get_queryset(self):
        query_names = ["name"]
        filter_args = {}
        for param in self.request.query_params:
            if param in query_names:
                filter_args[param] = self.request.query_params[param]
        return self.queryset.filter(**filter_args)
    @action(detail=False, methods=["get"])
    def teachers(self, request):
        return Response(TeacherSerializer(self.queryset.all()[0].teachers).data)