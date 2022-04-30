from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.utils.decorators import method_decorator
from django.http import HttpRequest
from Fast.django.decorators.cache.api import static_global_cache_page_renewable, dinamic_global_cache_page_renewable


EMPLOYEE_CACHE_LIST = 'employee_cache' # data is renewed with signals post_save


class SimpleApiWithAuthentication(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = IsAuthenticated,



class CreateAndListViewWithAuthenticationAndEmployeeCache(SimpleApiWithAuthentication, generics.ListCreateAPIView):
        
    @method_decorator(static_global_cache_page_renewable(EMPLOYEE_CACHE_LIST))
    def get(self, request: HttpRequest):
        return super().get(request)



class DetailViewWithAuthenticationAndEmployeeCache(SimpleApiWithAuthentication, generics.RetrieveUpdateDestroyAPIView):
    get_name_id = lambda self, pk : f'{self.group_name}_{pk}'

    def get(self, request: HttpRequest, pk: int):
        return dinamic_global_cache_page_renewable(EMPLOYEE_CACHE_LIST, self.group_name, self.get_name_id(pk))(super().get)(request, pk)