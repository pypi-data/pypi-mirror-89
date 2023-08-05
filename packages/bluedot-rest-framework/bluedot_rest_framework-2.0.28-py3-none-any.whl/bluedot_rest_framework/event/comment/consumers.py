import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string


EventComment = import_string(api_settings.EVENT['comment']['models'])
EventCommentSerializer = import_string(api_settings.EVENT['comment']['serializers'])

EventCommentLike = import_string(api_settings.EVENT['comment']['like_models'])
EventCommentLikeSerializer = import_string(api_settings.EVENT['comment']['like_serializers'])

class CommentConsumer(WebsocketConsumer):
    def connect(self):
        self.event_id = self.scope['url_route']['kwargs']['schedule_id']
        self.room_group_name = 'chat_%s' % self.event_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        state = text_data_json.get('state', 0)
        if state == 0:
            data = {
                'user_id': text_data_json.get('user_id', None),
                'unionid': text_data_json.get('unionid', None),
                'openid': text_data_json.get('openid', None),
                'nick_name': text_data_json.get('nick_name', None),
                'avatar_url': text_data_json.get('avatar_url', None),
                'schedule_id': self.event_id,
                'data': text_data_json.get('data', None),
            }
            EventComment.objects.create(**data)
        elif state == 1:  # 通过
            _id = text_data_json.get('id', None)
            data = text_data_json.get('data', None)
            event_queryset = EventComment.objects.get(pk=_id)
            event_queryset.state = 1
            event_queryset.data = data
            event_queryset.save()
            data = EventCommentSerializer(EventComment.objects.get(pk=_id)).data
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_chat_message',
                    **data
                }
            )
        elif state == 2:  # 拒绝
            _id = text_data_json.get('id', None)
            event_queryset = EventComment.objects.get(pk=_id)
            event_queryset.sate = 2
            event_queryset.save()
        elif state in [3, 4]:  # 点赞
            data = {
                'user_id': text_data_json.get('user_id', None),
                'unionid': text_data_json.get('unionid', None),
                'openid': text_data_json.get('openid', None),
                'comment_id': text_data_json.get('comment_id', None),
            }
            if state == 3:
                EventCommentLike.objects.create(**data)
                EventComment_queryset=EventComment.objects.get(
                    pk=data['comment_id'])
                EventComment_queryset.inc__like_count = 1
                EventComment_queryset.save()
            else:
                queryset = EventCommentLike.objects.filter(**data)
                if queryset:
                    queryset.delete()
                    EventComment_queryset=EventComment.objects.get(
                    pk=data['comment_id'])
                EventComment_queryset.inc__like_count = 1

            queryset = EventComment.objects.get(pk=data['comment_id'])
            send_data = {
                'comment_id': data['comment_id'],
                'like_count': queryset.like_count,
                'state': state
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_chat_message',
                    **send_data
                }
            )
        elif state == 5:  # 撤回
            _id = text_data_json.get('id', None)
            EventComment_queryset = EventComment.objects.get(pk=_id)
            EventComment_queryset.state = 0
            EventComment_queryset.save()
            send_data = {
                'comment_id': _id,
                'state': state
            }
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_chat_message',
                    **send_data
                }
            )

    def event_chat_message(self, event):
        self.send(text_data=json.dumps({
            **event
        }))
