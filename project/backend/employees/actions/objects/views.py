from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class SimpleApiWithAuthentication(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = IsAuthenticated,