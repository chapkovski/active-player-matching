from channels.generic.websockets import JsonWebsocketConsumer
import logging

from match.models import Player

logger = logging.getLogger(__name__)


class WPTracker(JsonWebsocketConsumer):
    url_pattern = (r'^/wp_tracker/(?P<player_pk>[0-9]+)$')

    def clean_kwargs(self):
        self.player_pk = self.kwargs['player_pk']

    def get_player(self):
        self.clean_kwargs()
        return Player.objects.get(pk=self.player_pk)

    def connect(self, message, **kwargs):
        """When a new client is connected we find the task and feed it back to him"""
        player = self.get_player()
        logger.info(f'client {player.participant.code} connected....')

    def receive(self, content, **kwargs):
        """When the new message is receved, we register it (updating current task). and feed him/her back a new task."""
        player = self.get_player()
        logger.info(f'status message from client {player.participant.code} received: {content}')
        player.active = content['status']
        player.save()