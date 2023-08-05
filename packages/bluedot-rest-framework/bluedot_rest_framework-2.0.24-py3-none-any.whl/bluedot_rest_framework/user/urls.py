from rest_framework.routers import DefaultRouter
from django.utils.module_loading import import_string
from bluedot_rest_framework.settings import api_settings


UserView = import_string(api_settings.USER['views'])

router = DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, basename='user')
urlpatterns = router.urls
