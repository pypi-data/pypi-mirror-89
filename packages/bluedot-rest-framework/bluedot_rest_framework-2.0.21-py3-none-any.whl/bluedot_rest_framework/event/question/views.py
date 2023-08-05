from rest_framework import status
from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create
from bluedot_rest_framework.utils.jwt_token import jwt_get_openid_handler

from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string


EventQuestion = import_string(api_settings.EVENT['question']['models'])
EventQuestionUser = import_string(
    api_settings.EVENT['question']['user_models'])
EventQuestionSerializer = import_string(
    api_settings.EVENT['question']['serializers'])
EventQuestionUserSerializer = import_string(
    api_settings.EVENT['question']['user_serializers'])


class EventQuestionView(CustomModelViewSet):
    model_class = EventQuestion
    serializer_class = EventQuestionSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        event_id = self.request.data.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        if queryset:
            partial = kwargs.pop('partial', False)
            serializer = self.get_serializer(
                queryset, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class EventQuestionUserView(CustomModelViewSet):
    model_class = EventQuestionUser
    serializer_class = EventQuestionUserSerializer
    filterset_fields = {
        'event_id': {
            'type': 'string',
            'filter': ''
        }

    }

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        openid = jwt_get_openid_handler(request.auth)
        data = EventQuestionUser.objects.filter(
            event_id=event_id, openid=openid).first()
        if data:
            serializer = self.get_serializer(data)
            return Response({'code': '1', 'data': serializer.data})
        else:
            return Response({'code': '0'})

    def perform_create(self, serializer):
        return user_perform_create(self.request.auth, serializer)
