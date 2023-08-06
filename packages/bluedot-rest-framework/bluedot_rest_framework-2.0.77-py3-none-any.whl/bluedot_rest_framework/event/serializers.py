from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework import import_string


Event = import_string('EVENT.models')


class EventSerializer(CustomSerializer):

    class Meta:
        model = Event
        fields = '__all__'
