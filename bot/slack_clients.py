
import logging
import re
import time
import json
import random
import os.path

from slacker import Slacker
from slackclient import SlackClient

logger = logging.getLogger(__name__)


class SlackClients(object):
    def __init__(self, token):
        self.token = token

        # Slacker is a Slack Web API Client
        self.web = Slacker(token)

        # SlackClient is a Slack Websocket RTM API Client
        self.rtm = SlackClient(token)

    def bot_user_id(self):
        return self.rtm.server.login_data['self']['id']
    
    #I failed at this. But leaving here to try another day!    
    # def get_user_name(self, user):
    #     return self.rtm.login_data['self']['name']

    def is_message_from_me(self, user):
        return user == self.rtm.server.login_data['self']['id']

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

    def send_time_triggered_msg(self, channel_name, msg):
    	self.rtm.api_call('chat.postMessage', as_user='true:', channel=channel_name, text="{}".format(msg.encode('ascii', 'ignore')))

    def get_random_emoji(self): #this method only gets custom emojis not all slack emojis
    	response = self.rtm.api_call('emoji.list')
    	emojis = response['emoji'].items()
    	return emojis[int(random.random()*len(emojis))][0]

    def get_user_name(self, user_id): #method not working yet
    	response = self.rtm.api_call('users.info', user=user_id)
    	user_info = response['user'].items()
    	return user_info[1][1]

    def upload_file_to_slack(self): 
    	my_file = os.path.join('./resources', 'pokemon_correct.txt')  #files = {'file': open('test.png', 'rb')}
    	self.web.files.upload(my_file, channels='#bolton-testing')
    	#file = response['file'].items()
    	#self.rtm.api_call('chat.postMessage', as_user='true:', channel='#zacefron-testing', text=response)
    	#self.rtm.api_call('files.upload', filename='pokemon_correct.txt', file=open(os.path.join('./resources', 'pokemon_correct.txt'), 'rb'), channels='#zacefron-testing')

    def get_file_info(self): 
    	response = self.rtm.api_call('files.info', file='F19NX4WJD')
    	files = response['file'].items()
    	self.rtm.api_call('chat.postMessage', as_user='true:', channel='#bolton-testing', text=files[16][0])
    	response2 = self.rtm.api_call('users.info', user='U15FDSK5M')
    	user_info = response2['user'].items()
    	self.rtm.api_call('chat.postMessage', as_user='true:', channel='#bolton-testing', text=user_info[0][2])