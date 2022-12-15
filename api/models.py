from django.db import models
import uuid
import numpy as np 
import cv2
import datetime
import base64


class UUIDModel(models.Model):
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
    @property
    def center_x(self) -> float:
        return float(self.xmax - self.xmin)/2. + float(self.xmin)
    @property
    def center_y(self) -> float:
        return float(self.ymax - self.ymin)/2. + float(self.ymin)

class Point(UUIDModel):
    class Meta:
        db_table = 'point'
    x = models.FloatField()
    y = models.FloatField()
    p = models.FloatField()

point_names = ['nose', 'neck', 'r_shoulder', 'r_elbow', 'r_wrist', 'l_shoulder', 'l_elbow', 'l_wrist', 'midhip', 'r_hip', 'r_knee',
                'r_ankle', 'l_hip', 'l_knee', 'l_ankle', 'r_eye', 'l_eye', 'r_ear', 'l_ear', 'l_bigtoe','l_smalltoe', 'l_heel', 'r_bigtoe',
                'r_smalltoe', 'r_hell']
class Keypoints(UUIDModel):
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
    
class CombinedFrame(UUIDModel):
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
    @property
    def img(self) -> np.ndarray:
        return cv2.imread(self.img_path)
    @property
    def img_base64(self) -> str: 
        ret, dst_data = cv2.imencode('.jpg', self.img)
        return base64.b64encode(dst_data)
    def get_visualized_image(self, draw_keypoints:bool=False, color:tuple[int, int, int]=(0, 0, 0), point_radius:int=5, thickness:int=3) -> np.ndarray:
        img = self.img.copy()
        for person in self.people:
            cv2.putText(img, f'ID:{person.box.id}', (person.box.xmin, person.box.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1., color, thickness)
            cv2.rectangle(img, (person.box.xmin, person.box.ymin), (person.box.xmax, person.box.ymax), color, thickness)
            if draw_keypoints:
                for point in person.keypoints.points:
                    cv2.circle(img, (int(point.x), int(point.y)), point_radius, color, thickness)
        return img

class MousePos(UUIDModel):
    class Meta:
        db_table = 'mouse_position'
        constraints = [
            models.UniqueConstraint(
                fields = ['group', 'time'],
                name = 'unique_mouse_position'
            )
        ]
    group = models.ForeignKey(Group, models.CASCADE, related_query_name='mouse_postions')
    time = models.TimeField()
    x = models.IntegerField()
    y = models.IntegerField()

class MouseClick(UUIDModel):
    class Meta:
        db_table = 'click'
    time = models.TimeField()
    x = models.IntegerField()
    y = models.IntegerField()
    frame = models.OneToOneField(CombinedFrame, models.CASCADE, null=True)
    
class MouseRelease(UUIDModel):
    class Meta:
        db_table = 'release'
    time = models.TimeField()
    x = models.IntegerField()
    y = models.IntegerField()
    frame = models.OneToOneField(CombinedFrame, models.CASCADE, null=True)

class Device(UUIDModel):
    class Meta:
        db_table = 'device'
    screenshot_path = models.CharField(max_length=100)
    frame = models.OneToOneField(CombinedFrame, models.CASCADE)
    group = models.ForeignKey(Group, models.CASCADE, 'devices')
    mouse_pos = models.ForeignKey(MousePos, models.PROTECT)
    mouse_click = models.OneToOneField(MouseClick, models.PROTECT, null=True)
    mouse_release = models.OneToOneField(MouseRelease, models.PROTECT, null=True)
    @property
    def screenshot(self) -> np.ndarray:
        return cv2.imread(self.screenshot_path)
    @property
    def screenshot_base64(self):
        ret, dst_data = cv2.imencode('.jpg', self.screenshot)
        return base64.b64encode(dst_data)
    @property
    def drawn_screenshot(self) -> np.ndarray:
        ss = self.screenshot
        color = (0, 0, 0) if self.mouse_click is None and self.mouse_release is None else (0, 0, 255)
        cv2.circle(ss, (self.mouse_pos.x, self.mouse_pos.y), 5, color, 10)
        return ss
    @property
    def drawn_screenshot_base64(self) -> np.ndarray:
        ret, dst_data = cv2.imencode('.jpg', self.drawn_screenshot)
        return base64.b64encode(dst_data)
    
    
class PersonManager(models.Manager):
    def __getitem__(self, index:int):
        return self.all()[index]
class Person(UUIDModel):
    
    class Meta:
        db_table = 'person'
    objects = PersonManager()
    keypoints = models.OneToOneField(Keypoints, models.CASCADE, related_name='+')
    box = models.OneToOneField(BoundingBox, models.CASCADE, related_name='+')
    frame = models.ForeignKey(CombinedFrame, models.CASCADE, related_name='people')
    @property
    def img(self) -> np.ndarray:
        frame_img = self.frame.img
        screen_height, screen_width, _ = frame_img.shape
        img = frame_img[(self.box.ymin if self.box.ymin >= 0 else 0):(self.box.ymax if self.box.ymax <= screen_height else screen_height),
                        (self.box.xmin if self.box.xmin >= 0 else 0):(self.box.xmax if self.box.xmax <= screen_width else screen_width)]
        return img
    @property
    def img_base64(self):
        ret, dst_data = cv2.imencode('.jpg', self.img)
        return base64.b64encode(dst_data)
    def get_visualized_screen_img(self, draw_keypoints:bool=False,
                                  color:tuple[int, int, int]=(0, 0, 0), point_radius:int=5, thickness:int=3,
                                  isbase64=False
                                  ) -> np.ndarray:
        img_copy = self.frame.img
        cv2.rectangle(img_copy, (self.box.xmin, self.box.ymin), (self.box.xmax, self.box.ymax), color, thickness)
        if draw_keypoints:
            for point in self.keypoints.points:
                cv2.circle(img_copy, (int(point.x), int(point.y)), point_radius, color, thickness)
        if isbase64:
            ret, dst_data = cv2.imencode('.jpg', img_copy)
            return base64.b64encode(dst_data)
        return img_copy
    def get_visualized_img(self, color:tuple[int, int, int]=(0, 0, 0), point_radius:int=5, thickness:int=3,
                           isbase64=False
                           ) -> np.ndarray:
        img_copy = self.img.copy()
        for point in self.keypoints.points:
            cv2.circle(img_copy, (int(point.x)-self.box.xmin, int(point.y)-self.box.ymin), point_radius, color, thickness)
        if isbase64:
            ret, dst_data = cv2.imencode('.jpg', img_copy)
            return base64.b64encode(dst_data)
        return img_copy
    
class MouseDrag(UUIDModel):
    class Meta:
        db_table = 'drag'
        constraints = [
            models.UniqueConstraint(
                fields = ['click', 'group', 'release'],
                name = 'unique_drag'
            )
        ]
    click = models.OneToOneField(MouseClick, on_delete=models.CASCADE)
    release = models.OneToOneField(MouseRelease, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='drags')
    person = models.OneToOneField(Person, models.CASCADE, null=True)
    @property
    def distance(self) -> float:
        return np.linalg.norm(np.array([self.click.x-self.release.x, self.click.y-self.release.y]))
    @property
    def time(self) -> float:
        d = datetime.datetime.now().date()
        td = datetime.datetime.combine(d, self.release.time) - datetime.datetime.combine(d, self.click.time)
        return td.total_seconds()

class Teacher(models.Model):
    class Meta:
        abstract = True
    person = models.OneToOneField(Person, models.CASCADE, unique=True)
    label = models.IntegerField(default=0)
    
class WDTeacher(Teacher): #Watching Display Teacher
    class Meta:
        db_table = 'watching_display_teacher'
    
class PTeacher(Teacher): #Programming Teacher
    class Meta:
        db_table = 'programming_teacher'
        
class WTHTeacher(Teacher): #What They Have Teacher
    class Meta:
        db_table = 'what_they_have_teacher'
    