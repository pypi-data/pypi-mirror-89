
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler,jwt_get_openid_handler


EventRegister = import_string(api_settings.EVENT['register']['models'])
EventRegisterSerializer = import_string(api_settings.EVENT['register']['serializers'])


class UserEventView(CustomModelViewSet):
    model_class = EventRegister
    serializer_class = EventRegisterSerializer
    filterset_fields = {       
        'state': ['exact'],
    }

    def list(self, request, *args, **kwargs):
        state = request.query_params.get('state', None)
        openid = jwt_get_openid_handler(request.auth)
        queryset = self.model_class.objects.filter(openid=openid)
        filters = {
            'id__in': [item.event_id for item in queryset]}
        now_time = datetime.now()

        if state == '2':
            filters['start_time__lt'] = now_time
        elif state == '3':
            filters['start_time__lt'] = now_time
            filters['end_time__gt'] = now_time
        elif state == '4':
            filters['end_time__lt'] = now_time
        event_queryset = Event.objects.filter(**filters)
        serializer = EventSerializer(event_queryset, many=True)
        return Response(serializer.data)
