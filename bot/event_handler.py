import json
import logging
import re

logger = logging.getLogger(__name__)

class RtmEventHandler(object):
    def __init__(self, slack_clients, msg_writer):
        self.clients = slack_clients
        self.msg_writer = msg_writer

    def handle(self, event):

        if 'type' in event:
            self._handle_by_type(event['type'], event)

    def _handle_by_type(self, event_type, event):
        # See https://api.slack.com/rtm for a full list of events
        if event_type == 'error':
            # error
            self.msg_writer.write_error(event['channel'], json.dumps(event))
        elif event_type == 'message':
            # message was sent to channel
            self._handle_message(event)
        elif event_type == 'channel_joined':
            # you joined a channel
            self.msg_writer.write_help_message(event['channel'])
        elif event_type == 'group_joined':
            # you joined a private group
            self.msg_writer.write_help_message(event['channel'])
        else:
            pass

    def is_loud(self,message):
        emoji_pattern = re.compile(":.*:")
        tag_pattern = re.compile("<@.*")
        tokens = message.split()

        if len(tokens) < 2: 
            return False
        for token in message.split():
            if not (token.isupper() or emoji_pattern.match(token)) or tag_pattern.match(token):
                return False

        return True

    def _handle_message(self, event):
        # Filter out messages from the bot itself
        if 'user' in event and not self.clients.is_message_from_me(event['user']):

            msg_txt = event['text']

            if re.search('always', msg_txt.lower()):
                self.msg_writer.write_no_qbot(event['channel'])

            if self.is_loud(msg_txt):
                self.msg_writer.write_loud(event['channel'],msg_txt)

            if re.search('(I|i) choose you', msg_txt):
                self.msg_writer.write_cast_pokemon(event['channel'], msg_txt.lower())

            if re.search('cry|Cry|CRY|crying|Crying|CRYING', msg_txt.lower()):
                self.msg_writer.write_crying_into_my_tea(event['channel'])

            if 'adobo' in msg_txt.lower():
                self.msg_writer.write_adobo(event['channel'])

            if re.search('boyer', msg_txt.lower()):
                self.msg_writer.write_boyer_bot(event['channel'])

            if re.search('weather', msg_txt.lower()):
                self.msg_writer.write_weather(event['channel'])

            if '*' in msg_txt and ' *' not in msg_txt and not msg_txt.startswith('*'):
                self.msg_writer.write_spelling_mistake(event['channel'])

            if re.search('fuck this|Fuck this|FUCK THIS', msg_txt):
                self.msg_writer.write_fuck_this(event['channel'])
                
            if re.search('do it', msg_txt.lower()):
                self.msg_writer.write_do_it(event['channel'])
                
            if msg_txt.lower().startswith('Bolton translate') and msg_txt.lower().endswith(' to french'):
                self.msg_writer.write_to_french(event['channel'], msg_txt)

            if re.search(' ?(B|b)olton', msg_txt.lower()) or self.clients.is_bot_mention(msg_txt) or re.search('qbot', msg_txt.lower()):
                # e.g. user typed: "@pybot tell me a joke!"
                if 'help' in msg_txt.lower():
                    self.msg_writer.write_help_message(event['channel'])
                if re.search('hi |hey|Hey|hello|howdy|Hi |Hello|sup ', msg_txt.lower()) or msg_txt.lower().endswith(' hi') or msg_txt.lower().endswith(' sup'):
                    self.msg_writer.write_greeting(event['channel'], event['user'])
                if re.search('good morning|morning|Morning|Good Morning|Good morning', msg_txt.lower()):
                    self.msg_writer.write_good_morning(event['channel'], event['user'])
                if re.search('good night|night|goodnight|Goodnight|Good night|Good Night|Night', msg_txt.lower()):
                    self.msg_writer.write_good_night(event['channel'], event['user'])
                if re.search('thanks|thank you|thank-you|Thanks|Thank you|Thank-you', msg_txt.lower()):
                    self.msg_writer.write_your_welcome(event['channel'], event['user'])
                if 'joke' in msg_txt.lower():
                    self.msg_writer.write_joke(event['channel'])
                if re.search('who\'?s that pokemon', msg_txt):
                    self.msg_writer.write_whos_that_pokemon(event['channel'])
                if re.search(' ?(B|b)olton it\'?s', msg_txt):
                    self.msg_writer.write_pokemon_guessed_response(event['channel'], event['user'], msg_txt)
                if 'attachment' in msg_txt:
                    self.msg_writer.demo_attachment(event['channel'])
                if 'sad' in msg_txt.lower():
                    self.msg_writer.write_sad(event['channel'])
                if 'kill me' in msg_txt.lower():
                    self.msg_writer.write_bang(event['channel'], event['user'])
                if re.search('(feed)|(hungry)', msg_txt.lower()):
                    self.msg_writer.write_food(event['channel'])
                if re.search('encourage me', msg_txt.lower()):
                    self.msg_writer.write_encouragement(event['channel'], event['user'])
                if 'sort me' in msg_txt.lower():
                    self.msg_writer.write_hogwarts_house(event['channel'], event['user'],  msg_txt)
                if 'sass ' in msg_txt.lower():
                    self.msg_writer.write_sass(event['channel'], msg_txt)	
                if ('945' in msg_txt) and ('?' in msg_txt):
                    self.msg_writer.announce_945(event['channel'])
                if re.search('apologize|apologise', msg_txt.lower()):
                    self.msg_writer.write_apology(event['channel'])
                if 'solve' in msg_txt.lower():
                    self.msg_writer.write_solution(event['channel'],msg_txt)
                if  re.search('explain|why', msg_txt.lower()):
                    self.msg_writer.write_explanation(event['channel'])
                if re.search('sweetpotato me|sweet potato me', msg_txt.lower()):
                    self.msg_writer.write_sweetpotato_me(event['channel'], event['user'])
                if re.search('marry me', msg_txt.lower()):
                    self.msg_writer.write_marry_me(event['channel'])
                if re.search('draw me', msg_txt.lower()):
                    self.msg_writer.write_draw_me(event['channel'])
                if re.search('forever', msg_txt.lower()):
                    self.msg_writer.write_forever(event['channel'])
                else:
                    pass
