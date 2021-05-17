from otree.api import *
import random

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'display_image'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_image_displayed = models.IntegerField()
    rating = models.FloatField()


# PAGES
class MyPage(Page):
    form_model = 'player'
    form_fields = ['rating']

    @staticmethod
    def vars_for_template(player: Player):
        number = random.randint(1, 2)
        player.number_image_displayed = number
        return dict(
            image_path='display_image/{}.jpeg'.format(number),
        )
# if we put "display_image/1.jpg" image No1 will be displaed,
# but if we do "display_image/{}.jpg" a random image of all stored in "static" folder will be displayed

class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
