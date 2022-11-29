from collections import OrderedDict
from rest_framework import serializers
from django.db import transaction, models
from .models import *

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = '__all__'

class Pointserializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

class KeypointsSerializer(serializers.ModelSerializer):
    points = Pointserializer(many=True, write_only=True)
    class Meta:
        model = Keypoints
        fields = point_names + ['points']
        read_only_fields = point_names 
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
    frame_num = serializers.IntegerField(source='frame.frame')
    frame_img_path = serializers.CharField(source='frame.img_path')
    class Meta:
        model = Person
        fields = ['box', 'keypoints', 'frame_num', 'frame_img_path']
        read_only_fields = ['frame_num', 'frame_img_path']

class FrameSerializer(serializers.ModelSerializer):
    people = PersonSerializer(many=True)
    class Meta:
        model = CombinedFrame
        fields = '__all__'
        read_only_fields = ['group']
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if 'group' not in data:
            img_path = data['img_path']
            group_name = img_path[img_path.index('G'):img_path.index('G')+2]
            data['group'] = {'name':group_name}
        return data
    
class FrameListSerializer(serializers.ListSerializer):
    child = FrameSerializer()
    def create(self, validated_data_list:list[OrderedDict]):
        new_people = []
        new_frames = []
        new_boxes = []
        new_keypoints_set = []
        new_points = []
        new_groups = []
        with transaction.atomic():
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

            Point.objects.bulk_create(new_points)
            Keypoints.objects.bulk_create(new_keypoints_set)
            BoundingBox.objects.bulk_create(new_boxes)
            Group.objects.bulk_create(new_groups, ignore_conflicts=True)
            CombinedFrame.objects.bulk_create(new_frames)
            Person.objects.bulk_create(new_people)
        return new_frames
    
    