from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import numpy as np
import time
#from ._builtin import Page, WaitPage, Bot
from otree.api import Currency as c, currency_range
# from .models import Constants
import random
# from . import pages
# from .models import Constants


doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'pdg_nice'
    players_per_group = 2
    conversion_rate = 1/150 # $0.006 for every point scored in Dal Bo and Frechette AER 2011

    instructions_template = 'pdg_nice/instructions.html'

    time_limit = False
    time_limit_seconds = 3600 # time limit for session (in seconds) since first round of first match (3600 in Dal Bo and Frechette AER 2011)

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = 50
    betrayed_payoff = 12

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = 32 # one of two treatments in Dal Bo & Frechette AER 2011; values: 32, 40, 48
    both_defect_payoff = 25

    delta = 0.50 # one of two treatments in Dal Bo & Frechette AER 2011; values: 0.50, 0.75
    num_matches = 1 # set to high number (e.g., 50) if time_limit == True
    match_duration = np.random.geometric(p=(1-delta), size=num_matches)  # the first argument here is the probability the match ends after each round (i.e., 1 - \delta); the second argument is the number of matches. For documentation, see: https://docs.scipy.org/doc/numpy-1.14.1/reference/generated/numpy.random.geometric.html
    num_rounds = np.sum(match_duration)
    last_rounds = np.cumsum(match_duration)
    last_round = last_rounds[-1]
    first_rounds = [1]
    for k in range(1, len(match_duration)):
        first_rounds.append(int(last_rounds[k - 1] + 1))


class Subsession(BaseSubsession):

    match_number = models.IntegerField()
    round_in_match_number = models.IntegerField()

    def creating_session(self):

        if self.round_number == 1:
            self.session.vars['start_time'] = time.time()
            self.session.vars['alive'] = True

        k = 0
        while k < len(Constants.last_rounds):
            if self.round_number <= Constants.last_rounds[k]:
                self.match_number = k + 1
                k = len(Constants.last_rounds)
            else:
                k += 1

        self.round_in_match_number = self.round_number - Constants.first_rounds[self.match_number-1] + 1

        if self.round_number in Constants.first_rounds:
            self.group_randomly()
        else:
            self.group_like_round(self.round_number-1)

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=['Action 1', 'Action 2'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Action 1':
                {
                    'Action 1': Constants.both_cooperate_payoff,
                    'Action 2': Constants.betrayed_payoff
                },
            'Action 2':
                {
                    'Action 1': Constants.betray_payoff,
                    'Action 2': Constants.both_defect_payoff
                }
        }

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]


class PlayerBot(Bot):
    def play_round(self):
        if self.subsession.round_number == 1:
            yield (pages.Instructions_1)
            yield (pages.Instructions_2)
            yield (pages.Instructions_3)
            if random.uniform(0, 1) > 0.5:
                yield (pages.Decision, {"decision": 'Action 1'})
                yield (pages.Results)
                yield (pages.EndRound)
            else:
                yield (pages.Decision, {"decision": 'Action 2'})
                yield (pages.Results)
                yield (pages.EndRound)

        else:
            if random.uniform(0, 1) > 0.5:
                yield (pages.Decision, {"decision": 'Action 1'})
                yield (pages.Results)
                yield (pages.EndRound)
            else:
                yield (pages.Decision, {"decision": 'Action 2'})
                yield (pages.Results)
                yield (pages.EndRound)



class Introduction(Page):
    timeout_seconds = 100

class Instructions_1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_2(Page):

    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        return dict(continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance+1,)

    def is_displayed(self):
        return self.subsession.round_number == 1

class Instructions_3(Page):
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        return dict(continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance+1,)

    def is_displayed(self):
        return self.subsession.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self):
        me = self.player
        opponent = me.other_player()
        return {
            'my_decision': me.decision,
            'opponent_decision': opponent.decision,
            'same_choice': me.decision == opponent.decision,
            'both_cooperate': me.decision == "Action 1" and opponent.decision == "Action 1",
            'both_defect': me.decision == "Action 2" and opponent.decision == "Action 2",
            'i_cooperate_he_defects':me.decision == "Action 1" and opponent.decision == "Action 2",
            'i_defect_he_cooperates':me.decision == "Action 2" and opponent.decision == "Action 1",
        }

class EndRound(Page):
    timeout_seconds = 100
    def vars_for_template(self):
        continuation_chance = int(round(Constants.delta * 100))
        if self.subsession.round_number in Constants.last_rounds:
            dieroll = random.randint(continuation_chance+1, 100)
        else:
            dieroll =  random.randint(1, continuation_chance)
        return dict(dieroll=dieroll, continuation_chance=continuation_chance, die_threshold_plus_one=continuation_chance+1,)

    def after_all_players_arrive(self):
        elapsed_time = time.time() - self.session.vars['start_time']
        if Constants.time_limit == True and elapsed_time > Constants.time_limit_seconds and self.subsession.round_number in Constants.last_rounds:
            self.session.vars['alive'] = False

class End(Page):
    def is_displayed(self):
        return self.session.vars['alive'] == False or self.subsession.round_number == Constants.last_round

page_sequence = [
    #Introduction,
    Instructions_1,
    Instructions_2,
    Instructions_3,
    Decision,
    ResultsWaitPage,
    Results,
    EndRound,
    End
]