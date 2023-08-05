from bluedot_rest_framework import import_string
from bluedot_rest_framework.utils.serializers import CustomSerializer


EventDataDownload = import_string('EVENT.data_download.models')


class EventDataDownloadSerializer(CustomSerializer):

    class Meta:
        model = EventDataDownload
        fields = '__all__'
