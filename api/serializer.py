from collections import OrderedDict
from rest_framework import serializers
from django.db import transaction, models
import base64
from .models import *


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = ['xmin', 'xmax', 'ymin', 'ymax', 'id']
        
class Pointserializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['x', 'y', 'p']

class KeypointsSerializer(serializers.ModelSerializer):
    points = Pointserializer(many=True, write_only=True)
    for p in point_names:
        exec(f'{p} = Pointserializer(read_only=True)')
    class Meta:
        model = Keypoints
        fields = point_names + ['points']
        
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        points = data.pop('points')
        ret:dict[str, dict[str, float]] = {}
        for key, point in zip(point_names, points):
            ret[key] = point
        return ret

class PersonSerializer(serializers.ModelSerializer):
    box = BoxSerializer()
    keypoints = KeypointsSerializer()
    img = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ['id', 'box', 'keypoints', 'img']
    def get_img(self, instance:Person):
        return instance.get_visualized_screen_img(isbase64=True, color=(0, 0, 255))
    
class PersonSerializer2(serializers.ModelSerializer):
    box = BoxSerializer()
    frameNum = serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = ['id', 'box', 'frameNum']
    def get_frameNum(self, instance:Person):
        return instance.frame.frame
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
class FrameSerializer(serializers.ModelSerializer):
    people = PersonSerializer(many=True)
    img = serializers.SerializerMethodField()
    group = GroupSerializer(read_only=True)
    class Meta:
        model = CombinedFrame
        fields = ['group', 'img_path', 'people', 'frame', 'img']
        extra_kwargs = {
            'img_path':{'write_only':True}
        }
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'group' not in data:
            img_path = data['img_path']
            group_name = img_path[img_path.index('G'):img_path.index('G')+2]
            data['group'] = {'name':group_name}
        return data
    def get_img(self, instance:CombinedFrame):
        with open(instance.img_path, 'rb') as f:
            img = base64.b64encode(f.read())
        return img.decode('utf-8')
    
class FrameListSerializer(serializers.ListSerializer):
    child = FrameSerializer()
    def create(self, validated_data_list:list[OrderedDict]):
        new_people = []
        new_frames = []
        new_boxes = []
        new_keypoints_set = []
        new_points = []
        new_groups = []
        for validated_data in validated_data_list:
            people = validated_data.pop('people')
            new_group = Group(**validated_data['group'])
            validated_data['group'] = new_group
            new_frame = CombinedFrame(**validated_data)
            new_groups.append(new_group)
            new_frames.append(new_frame)
            for person in people:
                for name, point in person['keypoints'].items():
                    new_point = Point(**point)
                    person['keypoints'][name] = new_point
                    new_points.append(new_point)
                new_box = BoundingBox(**person['box'])
                new_keypoints = Keypoints(**person['keypoints'])
                new_person = Person(box=new_box, keypoints=new_keypoints, frame=new_frame)
                new_boxes.append(new_box); new_keypoints_set.append(new_keypoints)
                new_people.append(new_person)
        with transaction.atomic():
            Point.objects.bulk_create(new_points)
            Keypoints.objects.bulk_create(new_keypoints_set)
            BoundingBox.objects.bulk_create(new_boxes)
            Group.objects.bulk_create(new_groups, ignore_conflicts=True)
            CombinedFrame.objects.bulk_create(new_frames)
            Person.objects.bulk_create(new_people)
        return new_frames
    
class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouseClick 
        fields = '__all__'
        
class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MouseRelease
        fields = '__all__'
        
class DragSerializer(serializers.ModelSerializer):
    click = ClickSerializer()
    release = ReleaseSerializer()
    class Meta:
        model = MouseDrag
        fields = '__all__'
    
class WDTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WDTeacher
        fields = ['person', 'label']

class WTHTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WTHTeacher
        fields = ['person', 'label']
class PTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = PTeacher
        fields = ['person', 'label']