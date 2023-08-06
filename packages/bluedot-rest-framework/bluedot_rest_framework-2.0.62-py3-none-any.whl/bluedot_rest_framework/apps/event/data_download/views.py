import requests
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from bluedot_rest_framework.utils.crypto import AESEncrypt
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler, jwt_get_userinfo_handler, jwt_get_openid_handler
from bluedot_rest_framework.apps.event.frontend_views import FrontendView
from bluedot_rest_framework.apps.user import UserModel
from .models import EventDataDownload
from .serializers import EventDataDownloadSerializer


class EventDataDownloadView(CustomModelViewSet, FrontendView):
    model_class = EventDataDownload
    serializer_class = EventDataDownloadSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id', None)
        queryset = self.model_class.objects.filter(event_id=event_id).first()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='send-email', url_name='send-email')
    def send_email(self, request, *args, **kwargs):
        data_list = request.data["data"]
        openid = jwt_get_openid_handler(request.auth)
        email = UserModel.objects.get(openid=openid).profile["email"]
        email = AESEncrypt.decrypt(email)
        email = EmailMessage(subject='【下载资料】' + 'title',
                             from_email=settings.EMAIL_HOST_USER, to=[email])
        url_list = [data['url'] for data in data_list]
        # pdf = [requests.get(url).content for url in url_list]

        return Response({"code": "200"})
