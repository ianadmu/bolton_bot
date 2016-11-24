class UserManager:

    def __init__(self, slack_clients, msg_writer):
        self.msg_writer = msg_writer
        self.users = slack_clients.get_users()
        self.user_names = dict()
        self.user_ids = dict()
        for user in self.users['members']:
            self.user_names[user['id']] = user['name']
            self.user_ids[user['name']] = user['id']

    def print_all_users(self, channel):
        for name in self.user_ids:
            self.msg_writer.send_message(
                name + ": " + self.user_ids[name], channel
            )

    def get_user_by_id(self, user_id):
        if user_id in self.user_names:
            return self.user_names[user_id]
        return None

    def get_user_by_name(self, name):
        if name in self.user_names:
            return self.user_names[name]
        return None

    def get_users_mentioned(self, message):
        mentioned_users = set()
        for token in message.split():
            if token in self.user_ids:
                mentioned_users.add(token)
        return mentioned_users
