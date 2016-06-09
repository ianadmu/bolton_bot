import os.path
import random
import re

sass_flag = re.compile('sass[a-z]* ')

class SassManager(object):

    def __init__(self):
        self.sass_file = open(os.path.join('./resources', 'sass.txt'), 'r')
        self.sassy_remarks = self.sass_file.readlines()

    def get_sass(self, msg):
        target = self.get_target(msg)
        sass = random.choice(self.sassy_remarks)
        return 'Hey, {}! {}'.format(target, sass)

    def get_target(self, msg):
        token = re.split(sass_flag, msg.lower())
        target = self.format_target(token[1]) #lower().encode('ascii','ignore') is causing tags to not work
        return target

    def format_target(self, target):
        if target == 'me':
            return 'you'
        elif target == 'yourself':
            return 'Zac Efron'
        elif '<@' in target:
            return target.upper()
        else:
            return target.title()
