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
    def distribution(self, request):
        teachers = WTHTeacher.objects.select_related('person').order_by('label')
        label_teachers_map = dict([(k, list(v)) for k, v in groupby(teachers, lambda x:x.label)])
        xs = [[t.person.box.center_x for t in ts] for ts in label_teachers_map.values()]
        ys = [[t.person.frame.frame / 25 for t in ts] for ts in label_teachers_map.values()]
        labels = [f'{k} ({len(v)})' for k, v in label_teachers_map.items()]
        colors = ['k', 'r', 'b']
        fig, ax = myplot.scatter_hist(xs, ys, colors, labels)
        fig.legend()
        ax[0].set(xlabel='x_center [px]', ylabel='time [sec]')
        ofs = BytesIO()
        fig.savefig(ofs, format='svg')
        return Response(base64.b64encode(ofs.getvalue()).decode())
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