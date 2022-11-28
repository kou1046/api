from django.http import response
import json     
from .serializer import *

def home(request):
    with open('json_data\\0000000001~0000000010.json', 'r') as f:
        data = json.load(f)
    f = FrameSerializer(data=data, many=True)
    f.is_valid()
    f.save()
    return response.HttpResponse({'test':'test'})
