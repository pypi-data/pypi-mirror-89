import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string


Comment = import_string(api_settings.EVENT['comment']['models'])
CommentSerializer = import_string(api_settings.EVENT['comment']['serializers'])

CommentUpvote = import_string(api_settings.EVENT['comment']['like_models'])
CommentUpvoteSerializer = import_string(api_settings.EVENT['comment']['like_serializers'])

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
                'interaction_id': self.event_id,
                'data': text_data_json.get('data', None),
            }
            Comment.objects.create(**data)
        elif state == 1:  # 通过
            _id = text_data_json.get('id', None)
            data = text_data_json.get('data', None)
            Comment.objects.get(pk=_id).update(state=state, data=data)
            data = CommentSerializer(Comment.objects.get(pk=_id)).data
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'event_chat_message',
                    **data
                }
            )
        elif state == 2:  # 拒绝
            _id = text_data_json.get('id', None)
            Comment.objects.get(pk=_id).update(state=state)
        elif state in [3, 4]:  # 点赞
            data = {
                'user_id': text_data_json.get('user_id', None),
                'unionid': text_data_json.get('unionid', None),
                'openid': text_data_json.get('openid', None),
                'comment_id': text_data_json.get('comment_id', None),
            }
            if state == 3:
                CommentUpvote.objects.create(**data)
                Comment.objects.get(
                    pk=data['comment_id']).update(inc__like_count=1)
            else:
                queryset = CommentUpvote.objects.filter(**data)
                if queryset:
                    queryset.delete()
                    Comment.objects.get(
                        pk=data['comment_id']).update(dec__like_count=1)

            queryset = Comment.objects.get(pk=data['comment_id'])
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
            Comment.objects.get(pk=_id).update(state=0)
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
