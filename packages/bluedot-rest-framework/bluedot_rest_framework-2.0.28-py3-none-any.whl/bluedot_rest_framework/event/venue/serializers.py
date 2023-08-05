from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string

EventVenue = import_string(api_settings.EVENT['venue']['models'])


class EventVenueSerializer(CustomSerializer):

    class Meta:
        model = EventVenue
        fields = '__all__'