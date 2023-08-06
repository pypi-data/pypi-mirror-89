from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string


EventQuestion = import_string('EVENT.question.models')
EventQuestionUser = import_string('EVENT.question.user_models')


class EventQuestionSerializer(CustomSerializer):

    class Meta:
        model = EventQuestion
        fields = '__all__'


class EventQuestionUserSerializer(CustomSerializer):

    class Meta:
        model = EventQuestionUser
        fields = '__all__'
