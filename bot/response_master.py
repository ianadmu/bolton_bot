import random
import json
import os.path
import re
import datetime


class Response:

    names = ["bolton", "qbot"]

    def __init__(
        self, phrases, words, emoji, responses, reactions,
        use_hash, named, start, end, sender, rateLimiter, msg_writer
    ):
        self.phrases = phrases
        self.words = words
        self.emoji = emoji
        self.responses = responses
        self.reactions = reactions
        self.use_hash = use_hash
        self.named = named
        self.start = start
        self.end = end
        self.sender = sender
        self.lastTimeResponded = datetime.datetime(1995, 1, 9)
        self.rateLimiter = rateLimiter
        self.msg_writer = msg_writer

    def rateLimit(self):
        # Don't call this unless you got a valid response
        allowedResponse = (
            self.lastTimeResponded +
            self.rateLimiter <= datetime.datetime.now()
        )
        if allowedResponse:
            self.lastTimeResponded = datetime.datetime.today()
        return allowedResponse

    def get_reaction_response(self, reaction, channel_id, ts):
        if reaction in self.emoji and self.rateLimit():
            self._react_to_message(channel_id, ts)
            return self.random()
        return ""

    def get_response(self, message, tokens, channel_id, user_id, ts):
        has_trigger = False
        is_named = False
        lower_msg = message.lower()

        for phrase in self.phrases:
            if lower_msg.startswith(phrase) or (" " + phrase) in lower_msg:
                has_trigger = True
                continue

        if not has_trigger:
            for word in self.words:
                for token in tokens:
                    if word == token:
                        has_trigger = True
                        continue

        for name in Response.names:
            if name in lower_msg:
                is_named = True

        if has_trigger and (not self.named or is_named) and self.rateLimit():
            self._react_to_message(channel_id, ts)

            # Get written response to trigger message
            result = self.hash(message) if self.use_hash else self.random()
            return self._replace_variables(result, user_id)
        return ""

    def _react_to_message(self, channel_id, ts):
        # React to trigger message if appropriate
        if len(self.reactions) > 0:
            reaction_emoji = random.choice(self.reactions)
            self.msg_writer.send_reaction(reaction_emoji, channel_id, ts)

    def _replace_variables(self, response_msg, user_id):
        if "user_id" in response_msg:
            response_msg = response_msg.replace(
                'user_id', '<@{}>'.format(user_id)
            )
        if "random_emoji" in response_msg:
            response_msg = response_msg.replace(
                "random_emoji", ":" + self.msg_writer.get_emoji() + ":"
            )
        return response_msg

    def hash(self, text):
        hashValue = 11
        for character in text:
            hashValue *= 47
            hashValue += ord(character)
        if len(self.responses) > 0:
            return (
                self.start + self.responses[hashValue % len(self.responses)] +
                self.end
            )
        else:
            return ""

    def random(self):
        if len(self.responses) > 0:
            return self.start + random.choice(self.responses) + self.end
        else:
            return ""


class Response_master:
    string_split = "[\s\.,?!]"

    def __init__(self, msg_writer):
        try:
            self.msg_writer = msg_writer
            master_file = open(os.path.join('./resources', 'events.txt'), 'r')
            json_events = json.load(master_file)
            self.events = []
            for event in json_events["Events"]:
                use_hash = "Hash" in event and event["Hash"]
                named = "Named" in event and event["Named"]
                start = ""
                end = ""
                sender = ""
                rateLimiter = datetime.timedelta(seconds=60)
                if "Start" in event:
                    start = event["Start"]
                if "End" in event:
                    end = event["End"]
                if "Sender" in event:
                    sender = event["Sender"]
                if "RateLimiter" in event:
                    rateLimiter = datetime.timedelta(
                        seconds=event["RateLimiter"]
                    )
                phrases = []
                words = []
                emoji = []
                if "Words" in event["Triggers"]:
                    for w in event["Triggers"]["Words"]:
                        words.append(w)
                if "Phrases" in event["Triggers"]:
                    for p in event["Triggers"]["Phrases"]:
                        phrases.append(p)
                if "Emoji" in event["Triggers"]:
                    for e in event["Triggers"]["Emoji"]:
                        emoji.append(e)

                reactions = []
                if "Reactions" in event:
                    for reaction_emoji in event["Reactions"]:
                        reactions.append(reaction_emoji)

                responses = []
                if "Formatting" in event:
                    responses = self.get_formatting(event["Formatting"])

                if "Responses" in event:
                    for r in event["Responses"]:
                        responses.append(r)
                self.events.append(
                    Response(
                        phrases, words, emoji, responses, reactions,
                        use_hash, named, start, end, sender, rateLimiter,
                        msg_writer,
                    )
                )
        except:
            msg_writer.write_error("Error loading JSON file")
            self.events = []

    def process_reaction(self, response, channel_id, ts):
        combined_responses = ""
        sender = None
        for event in self.events:
            current_response = event.get_reaction_response(
                response, channel_id, ts
            )
            if current_response != "":
                current_response += '\n'
                if event.sender:
                    sender = event.sender
            combined_responses += current_response

        self.send_message(channel_id, combined_responses, sender)

    def process_message(self, msg_text, channel_id, user_id, ts):
        combined_responses = ""
        tokens = re.split(self.string_split, msg_text.lower())
        sender = None
        for event in self.events:
            current_response = event.get_response(
                msg_text, tokens, channel_id, user_id, ts
            )
            if current_response != "":
                current_response += '\n'
                if event.sender:
                    sender = event.sender
            combined_responses += current_response

        self.send_message(channel_id, combined_responses, sender)

    def send_message(self, channel, message, sender):
        if message:
            if sender:
                self.msg_writer.send_slow_message_as_other(
                    message, channel, sender, ':' + sender + ':'
                )
            else:
                self.msg_writer.write_slow(message, channel)

    def get_formatting(self, event):
        try:
            if "Format" in event:
                text = event["Format"]
                response_list = []
                for item in re.findall('{(.+?)}', text):
                    temp_list = []
                    if item in event:
                        if len(response_list) == 0:
                            for num in range(len(event[item])):
                                temp_list.append(
                                    text.replace(
                                        "{" + item + "}", event[item][num]
                                    )
                                )
                        else:
                            for index in range(len(response_list)):
                                for num in range(len(event[item])):
                                    temp_list.append(
                                        response_list[index].replace(
                                            "{" + item + "}", event[item][num]
                                        )
                                    )
                    else:
                        raise Exception(
                            "BAD JSON FORMATTING: item not in event"
                        )
                    response_list = temp_list
                return response_list
            else:
                raise Exception("BAD JSON FORMATTING: Format not in event")
        except Exception as e:
            self.msg_writer.write_error(str(e))
