from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'game'
    players_per_group = None
    num_rounds = 1
    factor = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_entered = models.FloatField()


# PAGES
class Intro(Page):
    form_model = "player"

class MyPage(Page):
    form_model = "player"
    form_fields = ["number_entered"] #here we enter the list of all elements we want to be displayed on the page =["...", "...", ...]


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        result = player.number_entered * Constants.factor
        return {
            "result": result
        }


page_sequence = [Intro, MyPage, Results]
