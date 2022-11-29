from django.db import models
import uuid

class UuidModel(models.Model):
    class Meta:
        abstract = True
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class BoundingBox(models.Model):
    class Meta:
        db_table = 'boundingbox'
    pk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.IntegerField()
    xmin = models.IntegerField()
    ymin = models.IntegerField()
    xmax = models.IntegerField()
    ymax = models.IntegerField()

class Point(UuidModel):
    class Meta:
        db_table = 'point'
    x = models.FloatField()
    y = models.FloatField()
    p = models.FloatField()

point_names = ['nose', 'neck', 'r_shoulder', 'r_elbow', 'r_wrist', 'l_shoulder', 'l_elbow', 'l_wrist', 'midhip', 'r_hip', 'r_knee',
                'r_ankle', 'l_hip', 'l_knee', 'l_ankle', 'r_eye', 'l_eye', 'r_ear', 'l_ear', 'l_bigtoe','l_smalltoe', 'l_heel', 'r_bigtoe',
                'r_smalltoe', 'r_hell']
class Keypoints(UuidModel):
    class Meta:
        db_table = 'keypoints'
        default_related_name = '+'
    nose = models.OneToOneField(Point, models.CASCADE)
    neck = models.OneToOneField(Point, models.CASCADE)
    r_shoulder = models.OneToOneField(Point, models.CASCADE)
    r_elbow = models.OneToOneField(Point, models.CASCADE)
    r_wrist = models.OneToOneField(Point, models.CASCADE)
    l_shoulder = models.OneToOneField(Point, models.CASCADE)
    l_elbow = models.OneToOneField(Point, models.CASCADE)
    l_wrist = models.OneToOneField(Point, models.CASCADE)
    midhip = models.OneToOneField(Point, models.CASCADE)
    r_hip = models.OneToOneField(Point, models.CASCADE)
    r_knee = models.OneToOneField(Point, models.CASCADE)
    r_ankle = models.OneToOneField(Point, models.CASCADE)
    l_hip = models.OneToOneField(Point, models.CASCADE)
    l_knee = models.OneToOneField(Point, models.CASCADE)
    l_ankle = models.OneToOneField(Point, models.CASCADE)
    r_eye = models.OneToOneField(Point, models.CASCADE)
    l_eye = models.OneToOneField(Point, models.CASCADE)
    r_ear = models.OneToOneField(Point, models.CASCADE)
    l_ear = models.OneToOneField(Point, models.CASCADE)
    l_bigtoe = models.OneToOneField(Point, models.CASCADE)
    l_smalltoe = models.OneToOneField(Point, models.CASCADE)
    l_heel = models.OneToOneField(Point, models.CASCADE)
    r_bigtoe = models.OneToOneField(Point, models.CASCADE)
    r_smalltoe = models.OneToOneField(Point, models.CASCADE)
    r_hell = models.OneToOneField(Point, models.CASCADE)
    @property
    def points(self) -> list[Point]:
        return [getattr(self, name) for name in point_names]

class Group(models.Model):
    class Meta:
        db_table = 'group'
    name = models.CharField(primary_key=True, max_length=50)

class CombinedFrame(UuidModel):
    class Meta:
        db_table = 'frame'
        constraints = [
            models.UniqueConstraint(
                fields = ['frame', 'group'],
                name = 'group_frame_unique'
            )
        ]
    frame = models.IntegerField()
    img_path = models.CharField(max_length=100)
    group = models.ForeignKey(Group, models.CASCADE, related_name='frames')

class Person(UuidModel):
    class Meta:
        db_table = 'person'
    keypoints = models.OneToOneField(Keypoints, models.CASCADE, related_name='+')
    box = models.OneToOneField(BoundingBox, models.CASCADE, related_name='+')
    frame = models.ForeignKey(CombinedFrame, models.CASCADE, related_name='people')