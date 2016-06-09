import logging
import random
import re
import os.path
from datetime import datetime
from loud_manager import LoudManager
from whos_that_pokemon_manager import WhosThatPokemonManager
from pokemon_caster import PokemonCaster
from hogwarts_house_sorter import HogwartsHouseSorter
import scripts.weather_controller
from scripts.weather_controller import WeatherController
from sass_manager import SassManager
from food_getter import FoodGetter
from explanation_manager import ExplanationManager
from apology_manager import ApologyManager
from equation_manager import EquationManager

logger = logging.getLogger(__name__)
class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients
        self.loud_manager = LoudManager()
        self.whos_that_pokemon_manager = WhosThatPokemonManager()
        self.pokemon_caster = PokemonCaster()
        self.hogwarts_house_sorter = HogwartsHouseSorter()
        self.sass_manager = SassManager()
        self.apology_manager = ApologyManager()
        self.food_getter = FoodGetter()
        self.explanation_manager = ExplanationManager()
        self.equation_manager = EquationManager()

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        help_txt = [ "> `hi <@" + bot_uid + ">` - I'll greet back, i don't bite. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> weather` - Let me tell you the weather in Winnipeg. :rainbow:",
            "> `<@" + bot_uid + "> I'm sad` - Maybe I can cheer you up. :wink:",
            "> `<@" + bot_uid + "> sort me` - I'll sort you into one of the four Hogwarts houses! Better hope you don't get :slytherin:",
            "> `<@" + bot_uid + "> apologize` - Sometimes I make mistakes. Tell me when I do so I can apologize. :bow:",
            "> `<@" + bot_uid + "> thanks!` - I also sometimes do well! I also like to be appreciated :innocent:",
            "> `<@" + bot_uid + "> solve <equation>` - Math sucks. I can help! :nerd_face:",
            "> `<@" + bot_uid + "> sass <name>` - I'll be sure to sass <name> until the sun burns out. :smiling_imp:",
            "> `<@" + bot_uid + "> good morning` - I shall wish you a good morning as well! :sunny:",
            "> `<@" + bot_uid + "> good night` - I'll give you a goodnight greeting :crescent_moon:",
            "> `<@" + bot_uid + "> who's that pokemon?` - Are you a pokemon master? :slowpoke:",
            "> `<@" + bot_uid + "> Explain | Why` - I'll explain what's going on. :reginageorge:",
            "> `<@" + bot_uid + "> translate <phrase> to French` - I know flawless French! I'll translate for you :bombardier:",
            "> `<@" + bot_uid + "> marry me` - ...Are you going to propose to me?? _Le gasp_ :le gasp:",
            "> `<@" + bot_uid + "> sweetpotato me` - Sometimes you just need a :sweet_potato",
            "> `Boyer` - Did you know Gord Boyer is my favourite prof? I'll give you one of his wise quotes :nerd_face:",
            "> `Crying` - I cry when you cry :joy:",
            "> `Wiener` - You wanna know who a wiener is? I'll tell you :eggplant:",
            "> `<pokemon> I choose you!` - Are you going to be the very best? :yourturn:",
            "> `encourage` - Let me help you get back on track. :grinning:",
            "> `hungry | feed` - Have some food courtesy of moi :banana:",
            "> `Fuck this` - You're referring to OS, aren't you? Don't worry I got just the video. :+1:",
            "> `Do it` - Need some motivation? This vid should do the trick :sunglasses:"]
        txt = "I'm Bolton Efron." 
        #I'll *_respond_* to the following {0} commands:\n".format(len(help_txt))
        #for val in range(len(help_txt)):
        #    txt += help_txt[val]
        #    txt += '\n'
        
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, txt)
    
    def write_to_french(self, channel_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        tokens = msg.split()
        tokens.remove(tokens[len(tokens) - 1])
        tokens.remove(tokens[len(tokens) - 1])
        tokens.remove(tokens[0])
        tokens.remove(tokens[0])
        response = ' '.join(tokens)
        txt = '_le {}_'.format(response)
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_good_morning(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        good_mornings = ['Good morning', 'Morning', 'Guten Morgen', 'Bonjour', 'Ohayou', 'Good morning to you', 'Aloha', 'Konnichiwashington', 'Buenos dias', ':sunny: Good morning']
        txt = '{}, <@{}>!'.format(random.choice(good_mornings), user_id)
        self.send_message(channel_id, txt)
  
    def write_good_night(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        good_nights = ['Goodnight', ':crescent_moon: Good night', 'Goodnight, my dear', 'Sweet dreams', 'Don\'t let the bed bugs bite', 
        'Pleasant dreams', 'Sleep well', 'Until tomorrow then', 'May your dreams be filled with my beautiful face :zacefron:']
        txt =txt = '{}, <@{}>!'.format(random.choice(good_nights), user_id)
        self.send_message(channel_id, txt)

    def write_your_welcome(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        your_welcomes = ['No problem mon', 'Please don\'t use Comic Sans; this isn\'t a lemonade stand', 'Why, you\'re welcome my friend', 'Don\'t mention it', 'Don\'t mention it', 'You\'re welcome', 'It was a pleasure', 'It was my pleasure', 'No sweat', 'Anytime', '_Le gratitude_ pleases me. :heart: Thank you', 'No worries', 'No, thank you']
        txt = '{}, <@{}>!'.format(random.choice(your_welcomes), user_id)
        self.send_message(channel_id, txt)

    def write_spelling_mistake(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = 'Spelft it wronbg again I see...'
        self.send_message(channel_id, txt)
    
    def write_boyer_bot(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        boyer_responses = ['It was working upstairs--', 'Idk why it\'s not working now', 'Last time I taught this course it was working',
        'Last time I taught this course I didn\'t have to do this', 'I\'ll have to update my notes', 'This was working earlier',
        'Sorry I\'m late', 'Sorry the example wasn\'t working last class, it should be working now', 
        '........so that\'s basically what you\'ll need to do for assignment one', '[After 5 minutes of lecturing] Okay let\'s take a 10-minute break',
        '*Shows up 15 minutes late', '*Takes 15 minutes to notice a raised hand', 'This code came from a tutorial', 'Looks like break-time [Leaves]']
        txt = '_{}_'.format(random.choice(boyer_responses))
        self.send_message(channel_id, txt)

    def write_crying_into_my_tea(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = ':joy: _CRYING INTO MY TEA_ :joy:'
        self.send_message(channel_id, txt)

    def write_adobo(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = 'Leon cook me adobo!!! :adobo:'
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)
        
    def write_encouragement(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, 'Get your shit together <@{0}>'.format(user_id))
        
    def write_food(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        food = self.food_getter.get_random_food()
        self.send_message(channel_id, food)
        
    def write_bang(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        bang = 'BANG you\'re dead <@{}> :gun:'.format(user_id)
        self.send_message(channel_id, bang)

    def write_cast_pokemon(self, channel_id, msg):
        pkmn = self.pokemon_caster.i_choose_you(msg)
        if pkmn is not None:
            self.send_message(channel_id, pkmn)
        
    def write_whos_that_pokemon(self, channel_id):
        self.send_message(channel_id, self.whos_that_pokemon_manager.whos_that_pkmn())

    def write_pokemon_guessed_response(self, channel_id, user_id, msg):
        result = self.whos_that_pokemon_manager.check_response(user_id, msg)
        if result is not None:
            self.send_message(channel_id, result)

    def announce_945(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        time1 = datetime.now()
        time2 = datetime.time(9,45,0)
        time3 = time1 - time2
        self.send_message(channel_id, time1.__str__() +" "+ time2.__str__() + " "+ time3.__str__())
        self.send_message(channel_id,"945 :sunny: time now is " + datetime.now().strftime('%H:%M'))
        self.send_message(channel_id,"What's news?")

    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def write_no_qbot(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        responses = ['Always...', 'Ummm, how \'bout no.', 'ay sus', '_le shrug_ \'k.', 'No. Never. Nope. Nu-uh.']
        txt = '{}'.format(random.choice(responses))
        self.send_message(channel_id, txt)

    def write_fuck_this(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        attachment = "https://www.youtube.com/watch?v=5FjWe31S_0g"
        self.send_message(channel_id, attachment)
        
    def write_do_it(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        attachment = "https://www.youtube.com/watch?v=ZXsQAXx_ao0"
        self.send_message(channel_id, attachment)

    def write_sad(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = "This always cracks me up. :wink:"
        self.send_message(channel_id, txt)
        self.clients.send_user_typing_pause(channel_id)
        attachment = {
            "title": "/giphy bloopin",
            "title_link": "http://giphy.com/gifs/friday-rebecca-black-hurrr-13FsSYo3fzfT2g",
            "image_url": "http://i.giphy.com/13FsSYo3fzfT2g.gif",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id,"", attachments=[attachment], as_user='true')
        txt = "I'm crying into my tea. :joy:"
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def write_weather(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        response = WeatherController.get_weather()
        self.send_message(channel_id, response)

    def write_loud(self,channel_id,origMessage):
        self.loud_manager.write_loud_to_file(origMessage)
        self.send_message(channel_id, self.loud_manager.get_random_loud())

    def write_hogwarts_house(self, channel_id, user_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        response = self.hogwarts_house_sorter.sort_into_house(msg)
        txt = '<@{}>: {}'.format(user_id, response)
        self.send_message(channel_id, txt)
    
    def write_explanation(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, self.explanation_manager.get_explanation())
        
    def write_sass(self, channel_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        txt = self.sass_manager.get_sass(msg)
        self.send_message(channel_id, txt)

    def write_apology(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, self.apology_manager.get_random_apology())

    def write_solution(self, channel_id, msg):
        self.clients.send_user_typing_pause(channel_id)
        self.send_message(channel_id, self.equation_manager.solve(msg))
        
    def write_sweetpotato_me(self, channel_id, user_id):
        self.clients.send_user_typing_pause(channel_id)
        txt = 'Here, <@{}>! :sweet_potato:'.format(user_id)
        self.send_message(channel_id, txt)
        
    def write_marry_me(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        responses = ['OKAY! :ring:', 'Ummm, how \'bout no.', 'Shoot I would...if you were :kiera:', '_le shrug_ \'k.',
                'R-Really? Okay, I shall be your ~bride~ husband from now on!!', 'Sorry but I\'m already married to my job.',
                'Sorry, but I\'m already married to :nicole:', 'HOW DO I KNOW YOU WON\'T CHEAT ON ME WITH QBOT?!??',
                '_le HELLS YES!_', 'Sorry, but you are human, and I am a mere bot. It could never work out between us...',
                ':musical_note: _IF YOU LIKE IT THEN YOU SHOULDA PUT A RING ON IT_ :musical_note:', 'No. Never. Nope. Nu-uh.']
        txt = '{}'.format(random.choice(responses))
        self.send_message(channel_id, txt)


    def write_draw_me(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        file = open(os.path.join('./resources', 'draw_me.txt'), 'r')
        urls = file.read().splitlines()
        txt = '{}'.format(random.choice(urls))
        self.send_message(channel_id, txt)

    def write_forever(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        file = open(os.path.join('./resources', 'forever.txt'), 'r')
        comments = file.read().splitlines()
        txt = '{}'.format(random.choice(comments))
        self.send_message(channel_id, txt)
        self.clients.send_user_typing_pause(channel_id)
        answer = '{}'.format('Just kidding! :laughing:')
        self.send_message(channel_id, answer)
        self.clients.send_user_typing_pause(channel_id)
        #random_custom_emoji = self.clients.get_random_emoji()
        random_custom_emoji = 'trollface'
        emoji =':{}:'.format(random_custom_emoji)
        self.send_message(channel_id, emoji)
