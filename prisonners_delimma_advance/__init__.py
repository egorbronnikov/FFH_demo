import numpy as np
from otree.api import *

author = 'Your name here'
doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'prisonners_dilemma_advance'
    players_per_group = 2
    num_rounds = 1
    payoff_both_cooperate = -1
    payoff_both_defect = -3
    payoff_cooperate_defect_high = 0
    payoff_cooperate_defect_low = -4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    defect = models.BooleanField(
        label="Please Choose if you want to cooperate or defect",
        choices=[
            [True, "Defect"],
            [False, "Cooperate"],
        ],
    )


# FUNCTIONS


# PAGES
class MyPage(Page):
    form_model = 'player'
    # names must correspond to fields in models.py
    form_fields = ['defect']


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        player_list = group.get_players()
        player1 = player_list[0]
        player2 = player_list[1]
        if player1.defect:
            if player2.defect:
                player1.payoff = Constants.payoff_both_defect
                player2.payoff = Constants.payoff_both_defect
            else:
                player1.payoff = Constants.payoff_cooperate_defect_high
                player2.payoff = Constants.payoff_cooperate_defect_low
        else:
            if player2.defect:
                player2.payoff = Constants.payoff_cooperate_defect_high
                player1.payoff = Constants.payoff_cooperate_defect_low
            else:
                player1.payoff = Constants.payoff_both_cooperate
                player2.payoff = Constants.payoff_both_cooperate


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        list_of_decisions = [player.defect, player.get_others_in_group()[0].defect]
        return {
            "list_of_decisions": list_of_decisions,
        }


# the order in which pages are displayed
page_sequence = [MyPage,
                 ResultsWaitPage,
                 Results
                 ]
