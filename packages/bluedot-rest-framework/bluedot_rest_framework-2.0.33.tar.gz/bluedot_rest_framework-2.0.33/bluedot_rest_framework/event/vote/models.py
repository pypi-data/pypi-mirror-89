from django.db import models
from bluedot_rest_framework.question.abstract_models import AbstractQuestion, AbstractQuestionUser


class EventVote(AbstractQuestion):
    event_id = models.IntegerField()
    state= models.IntegerField(default=0)

    class Meta:
        db_table = 'event_vote'


class EventVoteUser(AbstractQuestionUser):

    class Meta:
        db_table = 'event_vote_user'
