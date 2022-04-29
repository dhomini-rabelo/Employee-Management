from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView


class SimpleJsonApi(APIView):
    renderer_classes = [JSONRenderer]
