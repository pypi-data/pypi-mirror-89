from bluedot_rest_framework.utils.serializers import CustomSerializer
from .models import WeChatQrcode


class WeChatQrcodeSerializer(CustomSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'
