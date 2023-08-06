from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string


EventVote = import_string('EVENT.vote.models')
EventVoteUser = import_string('EVENT.vote.user_models')


class EventVoteSerializer(CustomSerializer):

    class Meta:
        model = EventVote
        fields = '__all__'


class EventVoteUserSerializer(CustomSerializer):

    class Meta:
        model = EventVoteUser
        fileds = '__all__'
