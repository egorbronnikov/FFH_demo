import random

from otree.api import *

author = 'Your name here'
doc = """
 Your app description
 """


class Constants(BaseConstants):
    name_in_url = 'randomise_questions'
    players_per_group = None
    num_rounds = 3


class Player(BasePlayer):
    question_displayed_this_round = models.IntegerField()
    response_1 = models.StringField()
    response_2 = models.IntegerField()
    response_3 = models.BooleanField()


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        list_of_question_ids = [1, 2, 3]
        for player in subsession.get_players():
            temp_list = list_of_question_ids.copy()
            random.shuffle(temp_list)
            player.in_round(1).question_displayed_this_round = temp_list.pop(0)
            player.in_round(2).question_displayed_this_round = temp_list.pop(0)
            player.in_round(3).question_displayed_this_round = temp_list.pop(0)


# PAGES
class Question1(Page):
    form_model = "player"
    form_fields = ["response_1"]

    @staticmethod
    def is_displayed(player: Player):
        return player.question_displayed_this_round == 1


class Question2(Page):
    form_model = "player"
    form_fields = ["response_2"]

    @staticmethod
    def is_displayed(player: Player):
        return player.question_displayed_this_round == 2


class Question3(Page):
    form_model = "player"
    form_fields = ["response_3"]

    @staticmethod
    def is_displayed(player: Player):
        return player.question_displayed_this_round == 3


page_sequence = [Question1, Question2, Question3]
