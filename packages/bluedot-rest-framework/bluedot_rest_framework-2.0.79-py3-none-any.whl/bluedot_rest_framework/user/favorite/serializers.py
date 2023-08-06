from bluedot_rest_framework.utils.serializers import CustomSerializer
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from rest_framework.serializers import SerializerMethodField

UserFavoriteEvent = import_string(api_settings.USER['favorite']['models'])


class UserFavoriteEventSerializer(CustomSerializer):

    event_data = SerializerMethodField()

    class Meta:
        model = UserFavoriteEvent
        fields = '__all__'

    def get_event_data(self, queryset):

        event_id = queryset.event_id
        event_queryset = Event.objects.filter(pk=event_id).first()
        return {
            "title": event_queryset.title,
            "start_time": event_queryset.start_time,
            "banner": event_queryset.banner
        }
