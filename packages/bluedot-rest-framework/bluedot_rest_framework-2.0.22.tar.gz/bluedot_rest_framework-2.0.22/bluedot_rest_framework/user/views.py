from rest_framework.response import Response
from rest_framework import status
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler,jwt_get_openid_handler
from .frontend_views import FrontendView


User = import_string(api_settings.USER['models'])
UserSerializer = import_string(api_settings.USER['serializers'])


class UserView(CustomModelViewSet, FrontendView):
    model_class = User
    serializer_class = UserSerializer

    filterset_fields = {
        'wechat_profile__nick_name': ['contains'],
        'level': ['exact'],
    }

