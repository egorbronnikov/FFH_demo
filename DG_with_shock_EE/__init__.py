from otree.api import *
import time
import requests
import json
import pprint
from datetime import date, datetime, timedelta
from sqlalchemy.sql import sqltypes as st
from sqlalchemy import Column as C

author = 'Bronnikov & Chapkovski'
doc = """
The rich man and Lazarus dilemma: Second-party endowment effect in the Dictator game.(Bronnikov & Chapkovski, 2021)
"""



class Constants(BaseConstants):
    name_in_url = 'DG_with_shock_EE'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'DG_with_shock_EE/instructions.html'
    # Initial amount allocated to the dictator
    endowment = cu(100)
    correct_answers = dict(
        qq1=1,
        qq2=3,
        qq3=1,
        qq4=2,
        qq5=3,
    )
    MILLISECS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=Constants.endowment,
        label="I will keep",
    )


class Player(BasePlayer):
    # shock_time = djmodels.DateTimeField(blank=True, null=True)
    # entrance_time = djmodels.DateTimeField(blank=True, null=True)
    shock_time = C(st.DateTime)

    def get_stonk(self):
        # stamp = self.shock_time_epoch()
        shock_time = (self.shock_time - timedelta(minutes=1)).replace(second=0, microsecond=0)
        stamp = int(shock_time.timestamp() * Constants.MILLISECS)
        url = f'https://www.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&startTime={stamp}&endTime={stamp}'
        r = requests.get(url)
        pprint(r.json())
        return r.json()[-1][4]  # we return closing value only


    qq1 = models.IntegerField(
        choices=[(0, "You will have Player 1's role"),
                 (1, "You will have Player 2's role"),
                 (2, "No effect will occur"),
                 (3, "There will be higher chance to get Player A's role")],
        widget = widgets.RadioSelect,
        label="Question 1: If at [time] BTC index will equal have \"2\" in the the last digit",
    )
    qq2 = models.IntegerField(
        choices=[(0, "Player 1 will earn 100 ECU, Player 2 will earn 0 ECU."),
                 (1, "Player 1 will earn 100 ECU, Player 2 will earn 100 ECU."),
                 (2, "Player 1 will earn 0 ECU, Player 2 will earn 100 ECU."),
                 (3, "Player 1 will earn 0 ECU, Player 2 will earn 200 ECU.")],
        widget=widgets.RadioSelect,
        label="Question 2: If you turn out to be Player 1, and decide to transfer 100 ECU to player 2,"
              "how much will each of you earn by the end of the experiment"
              "(without taking into account additional show-up fee)?",
    )
    qq3 = models.IntegerField(
        choices=[(0, "refuse to accept the transfer from Player 1"),
                 (1, "no way"),
                 (2, "convince Player 1 to give a certain amount through the built-in communication mechanism"),
                 (3, "affect the BTC value")],
        widget=widgets.RadioSelect,
        label="Question 3: If you turn out to be Player 2, how can you influence the decision of Player 1?",
    )
    qq4 = models.IntegerField(
        choices=[(0, "$ @[time+1]"),
                 (1, "$ @[time-1]"),
                 (2, "$ @[time]"),
                 (3, "$ @[time+2]")],
        widget=widgets.RadioSelect,
        label="Question 4: What is BTC value at [time]?",
    )
    qq5 = models.IntegerField(
        choices=[(0, "$ @[time+1]"),
                 (1, "$ @[time-3]"),
                 (2, "$ @[time-4]"),
                 (3, "$ @[time-5]")],
        widget=widgets.RadioSelect,
        label="Question 4: What is BTC value at [time-5]?",
    )


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = Constants.endowment - group.kept


class Introduction(Page):
    pass


class Information(Page):
    form_model = 'player'
    @staticmethod
    def before_next_page(self, timeout_happened):
        player.set_shock_time()
    # @staticmethod
    # def before_next_page(player, timeout_happened):
    # player.set_shock_time()


class Waiting_for_Shock(Page):
    form_model = 'player'


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class Quiz(Page):
    form_model = "player"
    form_fields = ["qq1",
                   "qq2",
                   "qq3",
                   "qq4",
                   "qq5",
                   ]


    @staticmethod
    def error_message(player, values):
        for k, v in values.items():
            if Constants.correct_answers[k] != v:
                return "Not all questions are answered correct! Try once again!"



class Waiting_Offer(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2



class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=Constants.endowment - group.kept)

# <img src="{% static "my_app/my_image.png" %}"/>

page_sequence = [
                Introduction,
                # Quiz,
                Information,
                Waiting_for_Shock,
                # Offer,
                # Waiting_Offer,
                # ResultsWaitPage,
                # Results
                ]
