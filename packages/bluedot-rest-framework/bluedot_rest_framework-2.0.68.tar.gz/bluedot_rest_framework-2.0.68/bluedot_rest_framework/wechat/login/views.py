from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from bluedot_rest_framework.utils.oss import OSS
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from bluedot_rest_framework.wechat import OfficialAccount
from bluedot_rest_framework.wechat import OfficialAccount
from bluedot_rest_framework import import_string

from .models import WeChatLogin

User = import_string('USER.models')


class WeChatLoginView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = request.query_params.get('code', '')
        result = OfficialAccount.qrcode.create({
            'expire_seconds': 86400,
            'action_name': 'QR_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        WeChatLogin.objects.create(scene_str=scene_str)
        return Response(result)


class WeChatLoginWebSocketView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = request.query_params.get('scene_str', '')
        openid = request.query_params.get('openid', '')
        user_queryset = User.objects.filter(openid=openid).first()
        token = jwt_create_token_wechat(openid=user_queryset.openid, unionid=user_queryset.unionid,
                                        userid=user_queryset.pk, wechat_id=user_queryset.wechat_id)
        return HttpResponse("""<script>
var url = 'wss://cpa-global-wechat.bluewebonline.com/ws/wechat/login/""" + scene_str + """'
var ws = new WebSocket(url);
ws.onopen = function() {
    ws.send(JSON.stringify({token:'"""+token+"""'}));
};
</script>""")
