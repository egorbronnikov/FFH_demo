from otree.api import *

c = Currency

doc = """
FFH
"""


class Constants(BaseConstants):
    name_in_url = 'FFH'
    players_per_group = None
    num_rounds = 1
    endowment = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    number_entered = models.IntegerField(
        min=0,
        max=6,
    )
    # number_entered = models.IntegerField(choices=[1, 2, 3, 4, 5, 6]) #creates a list of choice


# PAGES
class Intro(Page):
    form_model = "player"
    # form_fields = [
    #     "number_entered"]  # here we enter the list of all elements we want to be displayed on the page =["...", "...", ...]


class MyPage(Page):
    form_model = "player"
    form_fields = [
        "number_entered"]  # here we enter the list of all elements we want to be displayed on the page =["...", "...", ...]


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        if player.number_entered < 6:
            result = Constants.endowment * player.number_entered
        else:
            result = 0
        return {
            "result": result
        }


page_sequence = [Intro, MyPage, Results]
