from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
EventComment = import_string(api_settings.EVENT['comment']['models'])
EventCommentLike = import_string(api_settings.EVENT['comment']['like_models'])

class EventCommentSerializer(CustomSerializer):
    class Meta:
        model = EventComment
        fields = '__all__'


class EventCommentLikeSerializer(CustomSerializer):
    class Meta:
        model = EventCommentLike
        fields = '__all__'

 



