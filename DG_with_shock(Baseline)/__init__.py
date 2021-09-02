from otree.api import *
c = Currency  # old name for currency; you can delete this.



author = 'Bronnikov & Chapkovski'
doc = """
The rich man and Lazarus dilemma: Second-party endowment effect in the Dictator game.(Bronnikov & Chapkovski, 2021)
"""



class Constants(BaseConstants):
    name_in_url = 'DG_with_shock(Baseline)'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'DG_with_shock(Baseline)/instructions.html'
    # Initial amount allocated to the dictator
    endowment = cu(100)


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
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = Constants.endowment - group.kept


# PAGES
class Introduction(Page):
    pass

class Quiz(Page):
    pass

class Information(Page):
    pass


class Waiting_for_Shock(Page):
    pass

class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


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
                Offer,
                Waiting_Offer,
                ResultsWaitPage,
                Results
                ]
