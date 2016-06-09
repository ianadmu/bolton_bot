import random
import os.path
import xml.etree.ElementTree as ET   

HOUSES = ['GRYFFINDOR','RAVENCLAW','SLYTHERIN','HUFFLEPUFF']
NUM_DESCRIPTIONS = 6

class HogwartsHouseSorter(object):

	def get_house(self, msg):
		msg = msg.upper();
		index = int(random.random()*len(HOUSES))
		for num in range(len(HOUSES)):
			if HOUSES[index] in msg.upper():
				return HOUSES[index]
			else:
				index = (index+1)%len(HOUSES)
		return random.choice(HOUSES)

	def get_house_description(self, house):
		tree = ET.parse(os.path.join('./resources', 'house_descriptions.xml'))
		root = tree.getroot()
		random_Number = int(random.random()*NUM_DESCRIPTIONS)
		return root[HOUSES.index(house)][random_Number].text

	def sort_into_house(self, msg):
		house = self.get_house(msg)	
		description = self.get_house_description(house)
		return "You have been sorted into: " + house + "!\n" + description

