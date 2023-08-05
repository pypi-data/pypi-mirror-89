from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
EventConfiguration = import_string(
    api_settings.EVENT['configuration']['models'])


class EventConfigurationSerializer(CustomSerializer):

    class Meta:
        model = EventConfiguration
        fields = '__all__'
