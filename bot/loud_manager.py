import random
import os.path


class LoudManager(object):
    def __init__(self):
        self.loud_file = open(os.path.join('./resources', 'louds.txt'), 'a+')
        self.loud_cache = list()
        self.cache_loaded = False

    def write_loud_to_file(self, loudMessage):
        loudMessage = loudMessage.encode("utf8")
        self.loud_file.write(loudMessage.replace("\n", " ")+"\n")
        self.loud_cache.append(loudMessage)

    def load_loud_cache(self):
        self.loud_cache = list(self.loud_file.readlines())

    def get_random_loud(self):
        if not self.cache_loaded:
            self.load_loud_cache()
            self.cache_loaded = True
        return random.choice(self.loud_cache)
