import random
import os.path
import re
import xml.etree.ElementTree as ET

from common import get_target


SORT_FLAG = re.compile('sort me[a-z]* ')

HOUSES = ['GRYFFINDOR', 'RAVENCLAW', 'SLYTHERIN', 'HUFFLEPUFF']
NUM_DESCRIPTIONS = 6


class HogwartsHouseSorter(object):

    def get_house(self, msg_text):
        options = []
        target = get_target(SORT_FLAG, msg_text).lower()
        if 'not' in target:
            for house in HOUSES:
                if house.lower() not in target:
                    options.append(house)
            if len(options) == 0:
                return ""
            return random.choice(options)
        else:
            for house in HOUSES:
                if house.lower() in target:
                    options.append(house)
            if len(options) == 0:
                options = list(HOUSES)
            return random.choice(options)

    def get_house_description(self, house):
        tree = ET.parse(os.path.join('./resources', 'house_descriptions.xml'))
        root = tree.getroot()
        random_Number = int(random.random()*NUM_DESCRIPTIONS)
        return root[HOUSES.index(house)][random_Number].text

    def sort_into_house(self, msg):
        house = self.get_house(msg)
        if house != "":
            description = self.get_house_description(house)
            return "You have been sorted into: " + house + "!\n" + description
        return "Sorry, you seem to be a muggle in disguise"
