from django.conf.urls import url
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

CommentConsumer = import_string(api_settings.EVENT['comment']['consumers'])

websocket_urlpatterns = [
    url(r'ws/event/comments/(?P<schedule_id>\w+)', CommentConsumer),
]
