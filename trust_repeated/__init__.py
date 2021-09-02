from otree.api import *
import random

doc = """
Indefinite Trust Game: Repeated Trust Game with a probability to turn to the next round (Berg, et al., 1995)
"""

c = Currency  # old name for currency; you can delete this.


class Constants(BaseConstants):
    name_in_url = 'trust_repeated'
    players_per_group = 2
    probab_to_continue = 0.9  # the threshold probability
    num_rounds = 20
    instructions_template = 'trust_repeated/instructions.html'
    endowment = cu(100)  # initial amount allocated to each player
    multiplier = 3
    num_rounds_with_certainty = 1  # min_num_rounds
    # to implement an automatically reassuring mechanism that guaranteeing 'num_rounds_with_certainty' equals at least 1
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
    sent_amount = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        doc="""Amount sent by P1""",
        label="Please enter an amount from 0 to 100:",
    )
    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        min=cu(0)
    )



class Player(BasePlayer):
    cum_payoff = models.CurrencyField()
    pass


# FUNCTIONS


def sent_back_amount_max(group):
    return group.sent_amount * Constants.multiplier




def filtering_dp(player):
    return player.group.working_round



def set_payoffs(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = Constants.endowment - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * Constants.multiplier - group.sent_back_amount
    for p in group.get_players():
        p.cum_payoff = sum([i.payoff for i in p.in_all_rounds()])


# PAGES

# class GenPage(Page):
#     is_displayed = filtering_dp
#
#
# class GenWPage(WaitPage):
#     is_displayed = filtering_dp



class Introduction(Page):
    is_displayed = filtering_dp
    pass

class Send(Page):
    # page for player 1 only
    form_model = 'group'
    form_fields = ['sent_amount']

    @staticmethod
    def is_displayed(player):
        return filtering_dp(player) and player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    is_displayed = filtering_dp
    pass

class SendBack(Page):
    # page for player 2 only
    form_model = 'group'
    form_fields = ['sent_back_amount']

    @staticmethod
    def is_displayed(player):
        return filtering_dp(player) and player.id_in_group == 2

    @staticmethod
    def vars_for_template(player):
        group = player.group

        tripled_amount = group.sent_amount * Constants.multiplier
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    is_displayed = filtering_dp
    after_all_players_arrive = set_payoffs


class Results(Page):
    is_displayed = filtering_dp
    # page for each player
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount=group.sent_amount * Constants.multiplier)


page_sequence = [
                Introduction,
                Send,
                SendBackWaitPage,
                SendBack,
                ResultsWaitPage,
                Results,
                ]
