from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler,jwt_get_openid_handler

UserFavoriteEvent = import_string(api_settings.USER['favorite']['models'])
UserFavoriteEventSerializer = import_string(api_settings.USER['favorite']['serializers'])

class UserFavoriteEventView(CustomModelViewSet, AllView):

    """用户收藏"""
    model_class = UserFavoriteEvent
    serializer_class = UserFavoriteEventSerializer
    filterset_fields = {
        'event_id': ['exact'],
    }

    def create(self, request, *args, **kwargs):
        _type = self.request.data.get('_type', None)
        user_id = jwt_get_userid_handler(self.request.auth)
        if _type == 0:
            self.model_class.objects.filter(
                user_id=user_id, event_id=request.data.get('event_id', None)).delete()
            return Response()
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='my-favorite', url_name='my-favorite')
    def my_favorite(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(self.request.auth)
        queryset = self.model_class.objects.filter(
            user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(self.request.auth)
        queryset = self.model_class.objects.filter(
            user_id=user_id, event_id=request.query_params.get('event_id', None)).first()
        if queryset:
            return Response({"code": 1})
        else:
            return Response({"code": 0})
