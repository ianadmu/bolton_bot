import random
import json
import os.path
import xml.etree.ElementTree as ET 
from datetime import datetime, timedelta
import scripts.weather_controller
from scripts.weather_controller import WeatherController

HOUR_DIFFERENCE_DAYLIGHT_SAVINGS = 5 #for Winnipeg
HOUR_DIFFERENCE_NO_DAYLIGHT_SAVINGS = 6 #for Winnipeg
MIN_PER_HOUR = 60
HR_PER_DAY = 24

class TimeTriggeredEventManager(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.last_random_hour = 0
        self.last_random_minutes = 0
        self.random_interval_minutes = 0
        self.random_hasnt_fired = True
        self.is_just_starting_up = True

    def trigger_ping(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'Ping on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':' 
        self.clients.send_time_triggered_msg('#bolton-testing', msg)

    def trigger_method_log(self, method_name):
        msg = 'Called: {}'.format(method_name)
        self.clients.send_time_triggered_msg('#bolton-testing', msg)

    def trigger_startup_log(self, day, hour, minute, second):
        random_custom_emoji = self.clients.get_random_emoji()
        msg = 'I came back to life on ' + day + ' ' + str(hour)  + ':' + str(minute) + ':' + str(second) + ' :' + str(random_custom_emoji) + ':' 
        self.clients.send_time_triggered_msg('#bolton-testing', msg)

    def trigger_random(self):
        channels = ['heliwolves', 'general', 'random']
        channel = '#{}'.format(random.choice(channels)) 
        tree = ET.parse(os.path.join('./resources', 'random_comments.xml'))
        root = tree.getroot()
        txt = root[int(random.random()*len(root))].text
        self.clients.send_time_triggered_msg(channel, txt)
        self.trigger_method_log('random')

    def check_trigger_random(self, hour, minute):
        random_should_fire_hr = (self.last_random_hour + int(self.random_interval_minutes/MIN_PER_HOUR) + int((self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)/MIN_PER_HOUR))%HR_PER_DAY
        random_should_fire_min = (self.last_random_minutes + self.random_interval_minutes%MIN_PER_HOUR)%MIN_PER_HOUR #math
        if self.random_hasnt_fired or (hour == random_should_fire_hr and minute == random_should_fire_min):
            max_minutes_between_random_events = 720 #12 hours max
            new_random_minutes = int(random.random()*max_minutes_between_random_events) + 1
            if hour >= 8 and hour < 22 and self.random_hasnt_fired == False: 
                self.trigger_random()
            self.last_random_hour = hour
            self.last_random_minutes = minute
            self.random_interval_minutes = new_random_minutes
            if self.random_hasnt_fired:
                #self.clients.upload_file_to_slack() #test file upload
                #self.clients.get_file_info()
                self.random_hasnt_fired = False

    def trigger_wine_club(self):
        tag_users = ['channel', 'here']
        msg = 'Dancing time!! :wine_glass: :wine_glass: :wine_glass: :wine_glass: :wine_glass:'
        txt = '<!{}> {}'.format(random.choice(tag_users), msg) 
        self.clients.send_time_triggered_msg('#boltonsexybutt-co', txt)

    def trigger_drunk_phrase(self):
        channels = ['boltonsexybutt-co', 'general', 'random']
        channel = '#{}'.format(random.choice(channels)) 
        random_custom_emoji = self.clients.get_random_emoji()
        drunk_comments_file = open(os.path.join('./resources', 'drunk_comments.txt'), 'r')
        drunk_comments = drunk_comments_file.read().splitlines()
        txt = '{} :{}:'.format(random.choice(drunk_comments), random_custom_emoji) 
        self.clients.send_time_triggered_msg(channel, txt)

    def trigger_weather(self):
        response = WeatherController.get_weather()
        self.clients.send_time_triggered_msg('#bolton_weather', response)

    def trigger_945(self):
        random_custom_emoji = self.clients.get_random_emoji()
        tag_users = ['channel', 'here']
        kip_msgs = ['@945', '945!', '#945', ':paw_prints: 945!', '~945~', ':horse: 945! giddyup', '945! :heart:', '945! :sweet_potato:', '945!........', '945 time', '945 quickie', '945 o\'clock', '945! :sheep: :panda_face: :slowpoke:', '945! :boom:', ':eggplant: 945.', '945 :coffee:', '_le 945_', '_le fast 945_']
        txt = '<!{}> {} :{}:'.format(random.choice(tag_users), random.choice(kip_msgs), random_custom_emoji) 
        self.clients.send_time_triggered_msg('#boltonsexybutt-co', txt)
        digg_options = ['edition', 'tech', 'technology', 'computer', 'computers', 'fun', 'neowin', '', 'trending', 'programmer']
        digg_msg = '/digg {}'.format(random.choice(digg_options))
        self.clients.send_time_triggered_msg('#boltonsexybutt-co', digg_msg)

    def trigger_mochaccino(self):
        tag_users = ['channel', 'here']
        msgs = ['The mochaccino tastes _amazing_ this morning!', 'Eh, mochaccino ain\'t so great today...', 'HELP! MOCHACCINO EVERYWHERE!',
        'The mochaccino machine won\'t stop dripping help I need an adult', 'WHAT! wHY is my mochaccino _decaf_??!', 'I haven\'t had my mochaccino yet don\'t talk to me',
        'WHERE\'S MY MUG I NEED MOCHACCINO!!', 'Mochaccino mochaccino mochaccino', 'Mochaccino is SO GOOD TODAY HOLY HELL', 
        'Today\'s mochaccino is like an angel pooped out a nice hot cup of coffee mmmmm~', 'Mochaccino status: passable',
        'MOCHACCINO MOCHACCINO MOCHACCINO!!!', 'Who\'s ready for a nice cup o\' mochaccino?', '_le mochaccino_']
        txt = '<!{}> {} :coffee:'.format(random.choice(tag_users), random.choice(msgs))
        self.clients.send_time_triggered_msg('#general', txt)

    def trigger_timed_event(self):
        #get date and time
        curr_datetime = datetime.utcnow() - timedelta(hours=HOUR_DIFFERENCE_DAYLIGHT_SAVINGS) #change here when daylight savings ends
        day = curr_datetime.strftime('%A')
        hour = int(curr_datetime.strftime('%H'))
        minute = int(curr_datetime.strftime('%M'))
        second = int(curr_datetime.strftime('%S'))

        #trigger startup log to testing channel
        if(self.is_just_starting_up):
            self.trigger_startup_log(day, hour, minute, second)
            self.is_just_starting_up = False

        #leaves 10-ish seconds to trigger since method is called every 10-ish seconds and we wantz the if statement to trigger once per min only
        if(second >= 5 and second <= 15):
            #self.trigger_ping(day, hour, minute, second) #will post a ping every minute to testing channel
            self.check_trigger_random(hour, minute)
            if hour % 3 == 0 and minute == 0:
            	self.trigger_weather()
            if day != 'Saturday' and day !='Sunday' and hour == 9 and minute == 45:
                self.trigger_945()
            if day != 'Saturday' and day !='Sunday' and hour == 9 and minute == 0:
                self.trigger_mochaccino()
            if day == 'Friday':
                if hour == 16 and minute == 30:
                    self.trigger_wine_club()
                if (hour == 16 and minute == 31) or (hour == 17 and minute == 0) or (hour == 17 and minute == 30) or (hour == 18 and minute == 0): 
                    self.trigger_drunk_phrase()

