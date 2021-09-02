from otree.api import *
import random

c = Currency  # old name for currency; you can delete this.


author = 'Egor Bronnikov'
doc = """
Indefinite Prisoners Dilemma Game: Repeated  Prisoners Dilemma Game with a probability to turn to the next round
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner_repeated'
    players_per_group = 2
    # the threshold probability
    probab_to_continue = 0.9
    num_rounds = 10
    instructions_template = 'prisoner_repeated/instructions.html'
    # payoff if 1 player defects and the other cooperates
    betray_payoff = cu(20)
    betrayed_payoff = cu(-5)
    # payoff if both players cooperate or both defect
    both_cooperate_payoff = cu(10)
    both_defect_payoff = cu(0)
    # min_num_rounds (if needed)
    num_rounds_with_certainty = 1
    # to implement an automatically reassuring mechanism
    # that guaranteeing 'num_rounds_with_certainty' equals at least 1
    assert num_rounds_with_certainty > 0, 'Set min rounds to at least 1!'




class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    for k in subsession.get_groups():
        k.i = round(random.random(), 3)
        if k.round_number <= Constants.num_rounds_with_certainty:
            k.working_round = True
        else:
            if not k.in_round(k.round_number - 1).working_round:
                k.working_round = False
            else:
                k.working_round = k.i < Constants.probab_to_continue

class Group(BaseGroup):
    i = models.FloatField()
    working_round = models.BooleanField()
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=[['Action1', 'Action1'], ['Action2', 'Action2']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    cum_payoff = models.CurrencyField()




# FUNCTIONS
def set_payoffs(group):
    for p in group.get_players():
        set_payoff(p)
        p.cum_payoff = sum([i.payoff for i in p.in_all_rounds()])


def other_player(player):
    return player.get_others_in_group()[0]


def set_payoff(player):
    payoff_matrix = dict(
        Action1=dict(
            Action1=Constants.both_cooperate_payoff, Action2=Constants.betrayed_payoff
        ),
        Action2=dict(
            Action1=Constants.betray_payoff, Action2=Constants.both_defect_payoff
        ),
    )
    player.payoff = payoff_matrix[player.decision][other_player(player).decision]




def filtering_dp(player):
    return player.group.working_round



# PAGES
class Introduction(Page):
    is_displayed = filtering_dp
    timeout_seconds = 100


class Decision(Page):
    is_displayed = filtering_dp
    form_model = 'player'
    form_fields = ['decision']


class ResultsWaitPage(WaitPage):
    is_displayed = filtering_dp
    after_all_players_arrive = set_payoffs


class Results(Page):
    is_displayed = filtering_dp
    @staticmethod
    def vars_for_template(player: Player):
        me = player
        opponent = other_player(me)
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
        )


page_sequence = [
                 Introduction,
                 Decision,
                 ResultsWaitPage,
                 Results
                 ]
