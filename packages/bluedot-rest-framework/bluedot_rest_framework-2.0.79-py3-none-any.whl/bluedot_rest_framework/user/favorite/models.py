from django.db import models


class UserFavoriteEvent(models.Model):

    unionid = models.CharField(max_length=100)
    openid = models.CharField(max_length=100)
    user_id = models.CharField(max_length=32)
    event_id = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_favorite_event'
