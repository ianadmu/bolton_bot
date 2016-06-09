import os.path
import random

class LoudManager(object):
	def __init__(self):
		self.loud_file = open("louds.txt",'a+')
		self.loud_cache = list()
		self.cache_loaded = False

	def write_loud_to_file(self,loudMessage):
		self.loud_file.write(loudMessage.replace("\n"," ")+"\n")
		self.loud_cache.append(loudMessage)

	def load_loud_cache(self):
		for line in self.loud_file.read().splitlines():
			self.loud_cache.append(line)

	def get_random_loud(self):
		if not self.cache_loaded:
			self.load_loud_cache()
			self.cache_loaded = True

		return random.choice(self.loud_cache)
