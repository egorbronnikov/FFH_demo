from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'FFH_team'
    players_per_group = 2
    num_rounds = 1
    endowment = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_profit = models.IntegerField()


class Player(BasePlayer):
    number_entered = models.IntegerField(
        min=0,
        max=6,
        label="Number that occur on the dice"
    )


# PAGES


class Intro(Page):
    form_model = "player"


class MyPage(Page):
    form_model = "player"
    form_fields = [
        "number_entered"]


class Waiting(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        total_profit = 0
        for player in group.get_players():
            if player.number_entered < 6:
                total_profit += player.number_entered * Constants.endowment
            else:
                total_profit = 0
        group.total_profit = total_profit


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.payoff = player.group.total_profit / Constants.players_per_group


page_sequence = [Intro, MyPage, Waiting, Results]
