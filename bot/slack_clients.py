
import logging
import re
import time
import random
import os.path

from slacker import Slacker
from slackclient import SlackClient
from messenger import Messenger
from channel_manager import ChannelManager

from common import TESTING_CHANNEL

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

        self.msg_writer = Messenger(self)
        self.channel_manager = ChannelManager(self)

        # Set up bot_id
        self.bot_id = None
        self.startUp()

    def startUp(self):
        response = self.send_message_as_other(
            'Initializing bot_id...', TESTING_CHANNEL, 'bolton', ':boltonefron:'
        )
        if self.bot_id is None and 'message' in response:
            message = response['message']
            if 'bot_id' in message:
                self.bot_id = message['bot_id']
                self.msg_writer.erase_history(
                    'bolton erase 1',
                    self.channel_manager.get_channel_id(TESTING_CHANNEL),
                    float(time.time())
                )
                # msg_text = 'Initialized bot_id: ' + self.bot_id
                # self.send_message(msg_text, TESTING_CHANNEL)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']

    def is_message_from_me(self, message):
        if 'user' in message and message['user'] == self.bot_user_id():
            return True
        elif (
            'bot_id' in message and self.bot_id is not None and
            (
                message['bot_id'] == self.bot_id
                # message['bot_id'] == 'B1S057DV0' or
                # message['bot_id'] == 'B15JNU2AU'
            )
        ):
            return True
        return False

    def is_bot_mention(self, message):
        bot_user_name = self.rtm.server.login_data['self']['id']
        if re.search("@{}".format(bot_user_name), message):
            return True
        else:
            return False

    def send_user_typing_pause(self, channel_id, sleep_time=3.0):
        user_typing_json = {"type": "typing", "channel": channel_id}
        self.rtm.server.send_to_websocket(user_typing_json)
        time.sleep(sleep_time)

    # this method only gets a team's custom emojis and NOT all slack emojis
    def get_random_emoji(self):
        response = self.rtm.api_call('emoji.list')
        emojis = response['emoji'].items()
        return emojis[int(random.random()*len(emojis))][0]

    def send_message_as_other(self, msg_text, channel_id, username, emoji):
        response = self.rtm.api_call(
                'chat.postMessage', token=str(self.token), channel=channel_id,
                text=msg_text, link_names=1, username=username,
                unfurl_links=True, icon_emoji=emoji
        )

        # Make sure the message gets sent to bolton-testing at least
        if 'error' in response:
            response = str(response) + "\nOriginal message:\n" + msg_text
            self.send_message(response, TESTING_CHANNEL)
        return response

    def send_message(self, msg_text, channel):
        response = self.rtm.api_call(
            'chat.postMessage', token=str(self.token), channel=channel,
            text=msg_text, as_user=True, link_names=1, unfurl_links=True
        )
        # Make sure the message gets sent to bolton-testing at least
        if 'error' in response:
            response = str(response) + "\nOriginal message:\n" + msg_text
            self.send_message(response, TESTING_CHANNEL)
        return response

    def update_message(self, updated_msg_text, channel, timestamp):
        response = self.rtm.api_call(
            'chat.update', token=str(self.token), channel=channel,
            text=updated_msg_text, as_user=True, link_names=1,
            unfurl_links=True, ts=timestamp
        )
        # Make sure the message gets sent to bolton-testing at least
        if 'error' in response:
            response = (
                str(response) + "\nOriginal message:\n" + updated_msg_text
            )
            self.send_message(response, TESTING_CHANNEL)
        return response

    def get_message_history(self, channel_id, count=None):
        response = self.rtm.api_call(
            'channels.history', token=str(self.token), channel=channel_id,
            count=count
        )
        if 'error' in response:
            error_msg = "`get_message_history` error:\n" + str(response)
            self.msg_writer.write_error(error_msg)
        return response

    def delete_message(self, channel_id, timestamp):
        response = self.rtm.api_call(
            'chat.delete', token=str(self.token), channel=channel_id,
            as_user=True, ts=timestamp
        )
        if 'error' in response:
            error_msg = "`delete_message` error:\n" + str(response)
            self.msg_writer.write_error(error_msg)
        return response

    def send_attachment(self, txt, channel_id, attachment):
        # this does not return the response object that rtm does
        return self.web.chat.post_message(
            channel_id, txt, attachments=[attachment], as_user='true'
        )

    def get_users(self):
        response = self.rtm.api_call('users.list', token=str(self.token))
        if 'error' in response:
            error_msg = "`get_users` error:\n" + str(response)
            self.msg_writer.write_error(error_msg)
        return response

    def get_channels(self):
        response = self.rtm.api_call(
            'channels.list', token=str(self.token), exclude_archived=1,
        )
        if 'error' in response:
            error_msg = "`get_channels` error:\n" + str(response)
            self.msg_writer.write_error(error_msg)
        return response

    def get_groups(self):
        return self.rtm.api_call('groups.list', token=str(self.token))

    def get_ims(self):
        return self.rtm.api_call('im.list', token=str(self.token))

    def send_reaction(self, emoji_name, channel, timestamp):
        response = self.rtm.api_call(
            "reactions.add", token=str(self.token), name=emoji_name,
            channel=channel, timestamp=timestamp
        )
        if 'error' in response and response['error'] != 'already_reacted':
            error_msg = "`send_reaction` error:\n" + str(response)
            self.msg_writer.write_error(error_msg)
        return response

    def upload_file_to_slack(self, filepath, filename, channel):
        my_file = os.path.join(filepath, filename)
        return self.web.files.upload(my_file, channels=channel)
