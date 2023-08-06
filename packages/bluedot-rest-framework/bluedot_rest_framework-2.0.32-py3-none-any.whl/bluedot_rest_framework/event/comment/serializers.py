from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string

EventComment = import_string('EVENT.comment.models')
EventCommentLike = import_string('EVENT.comment.like_models')


class EventCommentSerializer(CustomSerializer):
    class Meta:
        model = EventComment
        fields = '__all__'


class EventCommentLikeSerializer(CustomSerializer):
    class Meta:
        model = EventCommentLike
        fields = '__all__'
