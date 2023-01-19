import re
from itertools import groupby

import torch
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import *
from .serializer import *


def to_kebab(s):
    return "-".join(
        re.sub(
            r"(\s|_|-)+",
            " ",
            re.sub(
                r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                lambda mo: " " + mo.group(0).lower(),
                s,
            ),
        ).split()
    )


def to_camel(string, titleCase=False):
    if titleCase:
        return "".join(x.title() for x in string.split("_"))
    else:
        return re.sub("_(.)", lambda m: m.group(1).upper(), string.lower())


class ReadOnlyFrameAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CombinedFrame.objects.all()
    serializer_class = ReadOnlyFrameSerializer

    def get_queryset(self):
        query_names = ["frame", "group"]
        filter_args = {}
        for name in self.request.query_params:
            if name in query_names:
                filter_args[
                    name + "__name" if name == "group" else name
                ] = self.request.query_params[name]
        return CombinedFrame.objects.filter(**filter_args)

    @action(detail=True, methods=["get"])
    def img(self, request, pk):
        return Response(CombinedFrame.objects.get(pk=pk).img_base64)


class PersonAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=True, methods=["get"])
    def img(self, request, pk):
        person = self.queryset.get(pk=pk)
        return Response(person.img_base64)

    @action(detail=True, methods=["get"])
    def screenimg(self, request, pk):
        person = self.queryset.get(pk=pk)
        return Response(
            person.get_visualized_screen_img(color=(0, 0, 255), isbase64=True)
        )


class DeviceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        query_names = ["frame", "group"]
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


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MouseDragViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MouseDrag.objects.all()
    serializer_class = MouseDragSerializer

    def get_queryset(self):
        group_pk = self.kwargs.get("group_pk")
        return Group(pk=group_pk).drags.all()

    @action(detail=False, methods=["get"])
    def distribution(self, request, **kwarg):
        drags = self.get_queryset().select_related("click__frame", "person__box")
        id_drags_map = {
            f"{id_}": list(drags)
            for id_, drags in groupby(
                drags.order_by("person__box__id"),
                lambda drag: drag.person.box.id if drag.person is not None else 0,
            )
        }
        response = []
        for id_, drags in id_drags_map.items():
            xs = [drag.click.frame.frame for drag in drags]
            ys = [drag.time for drag in drags]
            response.append({"ID": id_, "xs": xs, "ys": ys})
        return Response(response)


class InferenceModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InferenceModel.objects.all()
    serializer_class = InferenceModelSerializer

    @action(detail=True, methods=["get"])
    def info(self, request, pk):
        model = InferenceModel.objects.get(pk=pk)
        info = torch.load(model.model_path)
        info.pop("model_state_dict")
        for key in info:
            info[to_camel(key)] = info.pop(key)
        return Response(info)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        model_pk = self.kwargs.get("model_pk")
        return InferenceModel(pk=model_pk).teachers.all()

    @action(detail=False, methods=["get"])
    def distribution(self, request, **kwarg):
        model_pk = self.kwargs.get("model_pk")
        teachers = (
            InferenceModel(pk=model_pk)
            .teachers.select_related("person")
            .order_by("label")
        )
        label_teachers_map = [
            TeacherSerializer(v, many=True).data
            for k, v in groupby(teachers, lambda x: x.label)
        ]
        return Response(label_teachers_map)

    @action(detail=False, methods=["get"])
    def add(self, request, **kwarg):
        model_pk = self.kwargs.get("model_pk")
        teachers = InferenceModel(pk=model_pk).teachers
        people = Person.objects.exclude(
            id__in=teachers.values_list("person__id", flat=True),
            frame__frame__lt=30000,
            frame__frame__gt=150000,
        ).order_by("?")[:50]
        return Response(PersonSerializer2(people, many=True).data)
