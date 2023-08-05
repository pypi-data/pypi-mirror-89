from bluedot_rest_framework.utils.serializers import CustomSerializer
from rest_framework.serializers import SerializerMethodField
from bluedot_rest_framework.settings import api_settings
from django.utils.module_loading import import_string
from bluedot_rest_framework.wechat.models import WeChatUser

User = import_string(api_settings.USER['models'])



class UserSerializer(CustomSerializer):
    wechat_data=SerializerMethodField()
    class Meta:
        model = User
        fields = '__all__'
    

    def get_wechat_data(self, queryset):
        wechat_id = queryset.wechat_id
        wechat_queryset = WeChatUser.objects.filter(pk=wechat_id).first()
        return {
            'nick_name': wechat_queryset.nick_name,
            'gender': wechat_queryset.gender,
            'language': wechat_queryset.language,
            'city': wechat_queryset.city,
            'province': wechat_queryset.province,
            'country': wechat_queryset.country,
            'avatar_url':wechat_queryset.avatar_url
        }
