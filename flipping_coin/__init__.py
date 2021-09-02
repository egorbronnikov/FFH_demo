from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'flipping_coin'
    players_per_group = None
    instructions_template = 'flipping_coin/instructions.html'
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    heads_number = models.FloatField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=6,
        label="Number of \'Heads\' out of 6 tosses",
    )


# PAGES
class Introduction(Page):
    pass


class MyPage(Page):
    form_model = 'player'
    form_fields = ['heads_number']


# class ResultsWaitPage(WaitPage):
#     pass


class Results(Page):
    pass


page_sequence = [
                Introduction,
                MyPage,
                # ResultsWaitPage,
                Results
                ]
