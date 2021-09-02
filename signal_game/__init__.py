from otree.api import *
import random

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'signal_game'
    players_per_group = 2
    num_rounds = 3
    probab_to_continue = 0.95  # the threshold probability
    both_cooperate_good_signal_probab = 0.7  # P{signal will be positive} when both plrs choose 'orange' strategy
    any_defect_good_signal_probab = 0.1  # P{signal will be positive} when at least one plr choose 'purple' strategy
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
    random_number = models.FloatField()
    decision = models.StringField(
        choices=[['Action1', 'Action1'], ['Action2', 'Action2']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )
    cum_payoff = models.CurrencyField()
    # random_number_X = models.FloatField()
    # random_number_Y = models.FloatField()


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
class Decision(Page):
    is_displayed = filtering_dp
    form_model = 'player'
    form_fields = ['decision']



# class RandomNumber(Page):
#     is_displayed = filtering_dp
#     form_model = 'group'
#
#
#
#     @staticmethod
#     def vars_for_template(group):
#         random_number_X = round(random.random(), 3)
#         # random_number_X = k.i
#         me = group.get_player_by_id(1)
#         opponent = group.get_player_by_id(2)
#         return dict(
#             random_number_X=random_number_X,
#             my_decision=me.decision,
#             opponent_decision=opponent.decision,
#             same_choice=me.decision == opponent.decision,
#         )

    # @staticmethod
    # def vars_for_template(player):
    #     player2 = player.get_others_in_group()[0]
    #     return {
    #         "player2": player2
    #     }
    #
    # @staticmethod
    # def vars_for_template(player):
    #     random_number_X = round(random.random(), 3)
    #     return dict(random_number_X=random_number_X)



class Wait(WaitPage):
    is_displayed = filtering_dp

class ResultsWaitPage(WaitPage):
    is_displayed = filtering_dp
    after_all_players_arrive = set_payoffs

#
# class Signals(Page):
#     is_displayed = filtering_dp
#     timeout_seconds = 10
#
#
#     @staticmethod
#     def vars_for_template(player):
#         random_number_X = round(random.random(), 3)
#         random_number_Y = round(random.random(), 3)
#         me = player
#         opponent = other_player(me)
#         if me.decision=='Action1' and opponent.decision=='Action1':
#             if random_number_Y < Constants.both_cooperate_good_signal_probab:
#                 # both_cooperate_good_signal_probab = 0.7
#                 # P{signal will be positive} when both plrs choose 'orange' strategy
#                 return dict(
#                     random_number_X=random_number_X,
#                     random_number_Y=random_number_Y,
#                     my_decision=me.decision,
#                     opponent_decision=opponent.decision,
#                     same_choice=me.decision == opponent.decision,
#                     signal='Good signal',
#                 )
#             else:
#                 return dict(
#                     random_number_X=random_number_X,
#                     random_number_Y=random_number_Y,
#                     my_decision=me.decision,
#                     opponent_decision=opponent.decision,
#                     same_choice=me.decision == opponent.decision,
#                     signal='Bad signal',
#                 )
#         else:
#             if random_number_Y < Constants.any_defect_good_signal_probab:
#                 # any_defect_good_signal_probab = 0.1
#                 # P{signal will be positive} when at least one plr choose 'purple' strategy
#                 return dict(
#                     random_number_X=random_number_X,
#                     random_number_Y=random_number_Y,
#                     my_decision=me.decision,
#                     opponent_decision=opponent.decision,
#                     same_choice=me.decision == opponent.decision,
#                     signal='Good signal',
#                 )
#             else:
#                 return dict(
#                     random_number_X=random_number_X,
#                     random_number_Y=random_number_Y,
#                     my_decision=me.decision,
#                     opponent_decision=opponent.decision,
#                     same_choice=me.decision == opponent.decision,
#                     signal='Bad signal',
#                 )



class new(Page):
    is_displayed = filtering_dp
    timeout_seconds = 10


    @staticmethod
    def vars_for_template(player):
        random_number_X = round(random.random(), 3)
        random_number_Y = round(random.random(), 3)
        me = player
        opponent = other_player(me)
        if me.decision=='Action1' and opponent.decision=='Action1':
            if random_number_Y < Constants.both_cooperate_good_signal_probab:
                # both_cooperate_good_signal_probab = 0.7
                # P{signal will be positive} when both plrs choose 'orange' strategy
                return dict(
                    random_number_X=random_number_X,
                    random_number_Y=random_number_Y,
                    my_decision=me.decision,
                    opponent_decision=opponent.decision,
                    same_choice=me.decision == opponent.decision,
                    signal='Good signal',
                )
            else:
                return dict(
                    random_number_X=random_number_X,
                    random_number_Y=random_number_Y,
                    my_decision=me.decision,
                    opponent_decision=opponent.decision,
                    same_choice=me.decision == opponent.decision,
                    signal='Bad signal',
                )
        else:
            if random_number_Y < Constants.any_defect_good_signal_probab:
                # any_defect_good_signal_probab = 0.1
                # P{signal will be positive} when at least one plr choose 'purple' strategy
                return dict(
                    random_number_X=random_number_X,
                    random_number_Y=random_number_Y,
                    my_decision=me.decision,
                    opponent_decision=opponent.decision,
                    same_choice=me.decision == opponent.decision,
                    signal='Good signal',
                )
            else:
                return dict(
                    random_number_X=random_number_X,
                    random_number_Y=random_number_Y,
                    my_decision=me.decision,
                    opponent_decision=opponent.decision,
                    same_choice=me.decision == opponent.decision,
                    signal='Bad signal',
                )




class Results(Page):
    is_displayed = filtering_dp


    @staticmethod
    def vars_for_template(player):
        random_number_X = round(random.random(), 3)
        me = player
        opponent = other_player(me)
        return dict(
            random_number_X=random_number_X,
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
        )




page_sequence = [
                Decision,
                Wait,
                # RandomNumber,
                new,
                # Signals,
                ResultsWaitPage,
                Results
                ]
