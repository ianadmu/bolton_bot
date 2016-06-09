import random

class FoodGetter(object):

    def __init__(self):
        self.edibles = [':apple:', ':banana:', ':pear:', ':peach:', ':pineapple:', ':lemon:', ':watermelon:', 
            ':grapes:', ':strawberry:', ':melon:', ':cherry:', ':tomato:', ':eggplant:', 
            ':hot_pepper:', ':corn:', ':sweet_potato:', ':fries:', ':hamburger:', ':egg:',
            ':fried_shrimp:', ':meat_on_bone:', ':poultry_leg:', ':cheese_wedge:', ':bread:',
            ':hotdog:', ':pizza:', ':spaghetti:', ':taco:', ':burrito:', ':ramen:', ':stew:', ':sushi:',
            ':bento:', ':rice_ball:', ':rice:', ':rice_cracker:', ':oden:', ':dango:', ':shaved_ice:',
            ':ice_cream:', ':icecream:', ':cake:', ':birthday:', ':candy:', ':lollipop:', ':popcorn:',
            ':chocolate_bar:', ':doughnut:', ':cookie:', ':baby_bottle:', ':beetle:', ':spider:',
            ':cow:', ':pig:', ':bug:', ':snail:', ':tropical_fish:', ':fish:', ':blowfish:', ':sheep:',
            ':pig2:', ':rat:', ':rooster:', ':mushroom:', ':green_aple:', ':poop:']

    def get_random_food(self):
        food = random.choice(self.edibles)
        return 'Here, for you {0}'.format(food)