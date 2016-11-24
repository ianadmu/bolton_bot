class ChannelManager:

    def __init__(self, slack_clients):
        self.clients = slack_clients
        channels = self.clients.get_channels()
        self.channel_names = {}
        self.channel_ids = {}
        if channels['ok']:
            for channel in channels['channels']:
                self.channel_names[channel['id']] = channel['name']
                self.channel_ids[channel['name']] = channel['id']

    def get_channel_id(self, identifier):
        if identifier in self.channel_ids:
            return self.channel_ids[identifier]
        elif identifier in self.channel_names:
            return identifier
        elif identifier.replace('#', '') in self.channel_ids:
            return self.channel_ids[identifier.replace('#', '')]
        elif isinstance(identifier, dict):
            return identifier['id']
        else:
            return self.channel_ids['bolton-testing']

    def get_channel_by_id(self, channel_id):
        if channel_id in self.channel_names:
            return self.channel_names[channel_id]
        return None

    def get_channel_by_name(self, name):
        if name in self.channel_ids:
            return self.channel_ids[name]
        return None

    def get_all_channel_ids(self):
        # return a copy of all channel ids
        return list(self.channel_ids.values())

    def get_all_channel_names(self):
        # return a copy of all channel names
        return list(self.channel_names.values())
