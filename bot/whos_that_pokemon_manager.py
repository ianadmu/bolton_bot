import random
import requests

from common import ResourceManager


URL = 'http://pokeapi.co/api/v2/pokemon/{}/'


class WhosThatPokemonManager(object):
    def __init__(self):
        self.correct_answer = None
        self.pos_response_manager = ResourceManager('pokemon_correct.txt')
        self.neg_response_manager = ResourceManager('pokemon_incorrect.txt')

    def whos_that_pkmn(self):
        if self.correct_answer is None:
            return self.get_random_pokemon()
        else:
            answer = self.reveal_answer()
            return '{} Guess you aren\'t a Pokemon Master.'.format(answer)

    def get_random_pokemon(self):
        num = random.randint(1, 721)
        link = URL
        target = link.format(num)
        try:
            response = requests.get(target)
        except requests.exceptions.RequestException:
            return 'Sorry, today is a day of Digimon. No Pokemons for you.'
        else:
            pokemon = response.json()
            sprite = pokemon['sprites']['front_default']
            self.correct_answer = pokemon['name']
            return 'Who\'s that Pokemon? {}'.format(sprite)

    def check_response(self, user_id, msg):
        if self.correct_answer is None:
            return None
        else:
            tokens = msg.split()
            if self.correct_answer in tokens:
                return self.guessed_correctly(user_id)
            else:
                result = '<@{}> {}'.format(
                    user_id, self.neg_response_manager.get_response()
                )
                return result

    def guessed_correctly(self, user_id):
        random_response = self.pos_response_manager.get_response()
        revealed_name = self.reveal_answer()
        result = '{} {} You go <@{}>!'.format(
            random_response, revealed_name, user_id
        )
        return result

    def reveal_answer(self):
        answer = self.correct_answer.title()
        self.correct_answer = None
        return 'It was {}.'.format(answer)
