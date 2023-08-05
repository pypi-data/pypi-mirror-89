import datetime

from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'BLUEDOT_REST_FRAMEWORK', None)

DEFAULTS = {
    'EVENT': {
        'models': 'bluedot_rest_framework.event.models.Event',
        'serializers': 'bluedot_rest_framework.event.serializers.EventSerializer',
        'views': 'bluedot_rest_framework.event.views.EventView',
        'chat': {
            'models': 'bluedot_rest_framework.event.chat.models.EventChat',
            'serializers': 'bluedot_rest_framework.event.chat.serializers.EventChatSerializer',
            'views': 'bluedot_rest_framework.event.chat.views.EventChatView',
            'consumers': 'bluedot_rest_framework.event.chat.consumers.ChatConsumer',
            'routing': 'bluedot_rest_framework.event.chat.routing.websocket_urlpatterns',
        },
        'configuration': {
            'models': 'bluedot_rest_framework.event.configuration.models.EventConfiguration',
            'serializers': 'bluedot_rest_framework.event.configuration.serializers.EventConfigurationSerializer',
            'views': 'bluedot_rest_framework.event.configuration.views.EventConfigurationView',
        },
        'data_download': {
            'models': 'bluedot_rest_framework.event.data_download.models.EventDataDownload',
            'serializers': 'bluedot_rest_framework.event.data_download.serializers.EventDataDownloadSerializer',
            'views': 'bluedot_rest_framework.event.data_download.views.EventDataDownloadView',
        },
        'question': {
            'models': 'bluedot_rest_framework.event.question.models.EventQuestion',
            'serializers': 'bluedot_rest_framework.event.question.serializers.EventQuestionSerializer',
            'views': 'bluedot_rest_framework.event.question.views.EventQuestionView',
            'user_models': 'bluedot_rest_framework.event.question.models.EventQuestionUser',
            'user_serializers': 'bluedot_rest_framework.event.question.serializers.EventQuestionUserSerializer',
            'user_views': 'bluedot_rest_framework.event.question.views.EventQuestionUserView',
        },
        'register': {
            'models': 'bluedot_rest_framework.event.register.models.EventRegister',
            'serializers': 'bluedot_rest_framework.event.register.serializers.EventRegisterSerializer',
            'views': 'bluedot_rest_framework.event.register.views.EventRegisterView',
        },
        'schedule': {
            'models': 'bluedot_rest_framework.event.schedule.models.EventSchedule',
            'serializers': 'bluedot_rest_framework.event.schedule.serializers.EventScheduleSerializer',
            'views': 'bluedot_rest_framework.event.schedule.views.EventScheduleView',
        },
        'speaker': {
            'models': 'bluedot_rest_framework.event.speaker.models.EventSpeaker',
            'serializers': 'bluedot_rest_framework.event.speaker.serializers.EventSpeakerSerializer',
            'views': 'bluedot_rest_framework.event.speaker.views.EventSpeakerView',
        },
        'comment': {
            'models': 'bluedot_rest_framework.event.comment.models.EventComment',
            'serializers': 'bluedot_rest_framework.event.comment.serializers.EventCommentSerializer',
            'views': 'bluedot_rest_framework.event.comment.views.EventCommentView',
            'like_models': 'bluedot_rest_framework.event.comment.models.EventCommentLike',
            'like_serializers': 'bluedot_rest_framework.event.comment.serializers.EventCommentLikeSerializer',
            'like_views': 'bluedot_rest_framework.event.comment.views.EventCommentLikeView',
            'consumers': 'bluedot_rest_framework.event.comment.consumers.CommentConsumer',
            'routing': 'bluedot_rest_framework.event.comment.routing.websocket_urlpatterns',
        },
        'vote': {
            'models': 'bluedot_rest_framework.event.vote.models.EventVote',
            'serializers': 'bluedot_rest_framework.event.vote.serializers.EventVoteSerializer',
            'views': 'bluedot_rest_framework.event.vote.views.EventVoteView',
            'user_models': 'bluedot_rest_framework.event.vote.models.EventVoteUser',
            'user_serializers': 'bluedot_rest_framework.event.vote.serializers.EventVoteUserSerializer',
            'user_views': 'bluedot_rest_framework.event.vote.views.EventVoteUserView',
        },
        'venue': {
            'models': 'bluedot_rest_framework.event.venue.models.EventVenue',
            'serializers': 'bluedot_rest_framework.event.venue.serializers.EventVenueSerializer',
            'views': 'bluedot_rest_framework.event.venue.views.EventVenueView',
        },
    },
    'USER': {
        'models': 'bluedot_rest_framework.user.models.User',
        'serializers': 'bluedot_rest_framework.user.serializers.UserSerializer',
        'views': 'bluedot_rest_framework.user.views.UserView',
    }
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'EVENT',
    'USER'
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS)
# event_settings = api_settings.EVENT


# def transform_objects(settings):
#     for key in settings:
#         if isinstance(settings[key], dict):
#             transform_objects(settings[key])
#         else:
#             print(settings[key])


# transform_objects(event_settings)
