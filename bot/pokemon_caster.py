import json
import requests
import re

URL = 'http://pokeapi.co/api/v2/pokemon/{}/'

teammates = ["kiera", "nicole", "jill", "malcolm", "ian"]

class PokemonCaster(object):
                 
    def i_choose_you(self, msg):
        target = msg.split()[0]
        if target in teammates:
            return "Go! {}!\n:{}:".format(target.title(), target)
        else:
            link = URL
            pkmn = link.format(target)
            try:
                response = requests.get(pkmn)
            except requests.exceptions.RequestException as e:
                return None
            else:
                pokemon = response.json()
                if 'sprites' in pokemon:
                    return "Go! {}!\n{}".format(target.title(), pokemon['sprites']['front_default'])
                