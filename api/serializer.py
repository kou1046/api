from collections import OrderedDict
from rest_framework import serializers
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
    def create(self, validated_data:OrderedDict):
        people = validated_data.pop('people')
        validated_data['group'], created = Group.objects.get_or_create(**validated_data['group'])
        instance = super().create(validated_data)
        for person in people:
            box = BoundingBox.objects.create(**person['box'])
            for name, point in person['keypoints'].items():
                person['keypoints'][name] = Point.objects.create(**point)
            keypoints = Keypoints.objects.create(**person['keypoints'])
            Person.objects.create(box=box, keypoints=keypoints, frame=instance)
        return instance