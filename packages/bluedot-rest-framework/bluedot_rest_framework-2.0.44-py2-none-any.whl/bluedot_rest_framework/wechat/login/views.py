import asyncio
import websockets
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
        scene_str = f'bluedot_pc_login_{scene_str}'
        result = OfficialAccount.qrcode.create({
            'expire_seconds': 86400,
            'action_name': 'QR_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        WeChatLogin.objects.create(scene_str=scene_str)
        return Response(result)


async def send(uri, data):
    async with websockets.connect(uri) as websocket:
        await websocket.send(data)
        await websocket.recv()


class WeChatLoginWebSocketView(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        scene_str = ''
        queryset = WeChatLogin.objects.filter(scene_str=scene_str).first()
        user_queryset = User.objects.filter(openid=queryset.openid).first()
        token = jwt_create_token_wechat(
            openid=user_queryset.openid, unionid=user_queryset.unionid, user_id=user_queryset.pk, wechat_id=user_queryset.wechat_id)
        send(scene_str, {'token': token})
        return Response()
