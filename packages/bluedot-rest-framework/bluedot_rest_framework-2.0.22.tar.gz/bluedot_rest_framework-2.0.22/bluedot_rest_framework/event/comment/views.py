from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, user_perform_create, AllView
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from bluedot_rest_framework.utils.jwt_token import jwt_get_userid_handler


EventComment = import_string(api_settings.EVENT['comment']['models'])
EventCommentSerializer = import_string(api_settings.EVENT['comment']['serializers'])

EventCommentLike = import_string(api_settings.EVENT['comment']['like_models'])
EventCommentLikeSerializer = import_string(api_settings.EVENT['comment']['like_serializers'])

class EventCommentView(CustomModelViewSet):
    model_class = EventComment
    serializer_class = EventCommentSerializer
    filterset_fields = {
        'event_id': ['exact'],
        'schedule_id': ['exact'],
        'state': ['exact']
    }
    # def perform_create(self, serializer):
    #     return user_perform_create(self.request.auth, serializer)

    @action(detail=False, methods=['get'], url_path='show', url_name='show')
    def show(self, request, *args, **kwargs):
        user_id = jwt_get_userid_handler(request.auth)
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data
        for item in data:
            item['is_like'] = 0
            if CommentUpvote.objects.filter(user_id=user_id, event_chat_id=item['id']):
                item['is_like'] = 1
        return Response(data)


class EventCommentLikeView(CustomModelViewSet):
    model_class = EventCommentLike
    serializer_class = EventCommentLikeSerializer

