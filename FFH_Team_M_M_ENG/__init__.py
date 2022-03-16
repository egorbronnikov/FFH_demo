from otree.api import *

import random

c = Currency

doc = """
Your app description
"""




class Constants(BaseConstants):
    name_in_url = 'FFH_Team_M_M'
    players_per_group = 2
    num_rounds = 1
    endowment = 100
    instructions_0 = 'FFH_Team_M_M/Instructions_0.html'
    instructions_1 = 'FFH_Team_M_M/Instructions_1.html'
    correct_answers = dict(
        qq1=1,
        qq2=0,
        qq3=0,
        qq4=2,
        # qq5=1,
    )


# cu(player.payoff).to_real_world_currency(session)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_profit = models.IntegerField()


class Player(BasePlayer):
    qq1 = models.IntegerField(
        choices=[(0, "0 ECU"), (1, "200 ECU"), (2, "250 ECU"), (3, "500 ECU")],
        widget = widgets.RadioSelect,
        label="Вопрос 1: Если Вы ввели 2 как выпавшее число, то Ваш индивидуальный выирыш в игре составит",
    )
    qq2 = models.IntegerField(
        choices=[(0, "0 ECU"), (1, "200 ECU"), (2, "300 ECU"), (3, "600 ECU")],
        widget=widgets.RadioSelect,
        label="Вопрос 2: Если Вы ввели 6 как выпавшее число, то Ваш индивидуальный выирыш в игре составит",
    )
    qq3 = models.IntegerField(
        choices=[(0, "150 ECU"), (1, "250 ECU"), (2, "350 ECU"), (3, "600 ECU")],
        widget=widgets.RadioSelect,
        label="Вопрос 3: Если Вы ввели 3 как выпавшее число, а другой игрок в Вашей паре ввёл 6, то Ваш финальный выирыш в игре составит",
    )
    qq4 = models.IntegerField(
        choices=[(0, "0 ECU"), (1, "100 ECU"), (2, "200 ECU"), (3, "400 ECU")],
        widget=widgets.RadioSelect,
        label="Вопрос 4: Если Вы ввели 6 как выпавшее число, а другой игрок в Вашей паре ввёл 4, то Ваш финальный выирыш в игре составит",
    )
    # qq5 = models.IntegerField(
    #     choices=[(0, "0 ECU"), (1, "200 ECU"), (2, "400 ECU"), (3, "600 ECU")],
    #     widget=widgets.RadioSelect,
    #     label="Вопрос 5: Если Вы ввели 6 как выпавшее число, то Ваш индивидуальный выирыш в игре составит",
    # )
    number_entered = models.IntegerField(
        min=0,
        max=6,
        label="Выпавшее число"
    )
    artists = models.StringField(
        choices=[("Пьер Ренуap", "Пьер Ренуap"),
                 ("Клод Моне", "Клод Моне")],
        widget=widgets.RadioSelect,
        label="Кого из этих двух художников Вы предпочитаете?",
    )

    belief_1 = models.IntegerField(
        label="Доля участников в группе, заявившая число 1"
    )
    belief_2 = models.IntegerField(
        label="Доля участников в группе, заявившая число 2"
    )
    belief_3 = models.IntegerField(
        label="Доля участников в группе, заявившая число 3"
    )
    belief_4 = models.IntegerField(
        label="Доля участников в группе, заявившая число 4"
    )
    belief_5 = models.IntegerField(
        label="Доля участников в группе, заявившая число 5"
    )
    belief_6 = models.IntegerField(
        label="Доля участников в группе, заявившая число 6"
    )
    #for post-experiment survey
    age = models.IntegerField(
        label='Укажите, пожалуйста, Ваш возраст',
        min=18,
        max=125)
    gender = models.StringField(
        choices=[['Мужской', 'Мужской'],
                 ['Женский', 'Женский'],
                 ['Другой вариант', 'Другой вариант']],
        label='Укажите, пожалуйста, Ваш пол',
        widget=widgets.RadioSelect,
    )
    income = models.StringField(
        choices=[['Хватает только на еду', 'Хватает только на еду'],
                 ['Хватает на еду, одежду и прочие мелкие расходы', 'Хватает на еду, одежду и прочие мелкие расходы'],
                 ['Хватает на еду, одежду, средние траты, но не на покупку автомобиля',
                  'Хватает на еду, одежду, средние траты, но не на покупку автомобиля'],
                 ['Хватает на покупку автомобиля, но не на покупку квартиры/дома',
                  'Хватает на покупку автомобиля, но не на покупку квартиры/дома'],
                 ['Хватает на покупку квартиры/дома',
                  'Хватает на покупку квартиры/дома']
                 ],
        label='Укажите, пожалуйста, Ваш пол',
        widget=widgets.RadioSelect,
    )
    BF_1 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(1): Самому себе я кажусь сдержанным.',
        widget=widgets.RadioSelect,
    )
    BF_2 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(2): Самому себе я кажусь доверчивым.',
        widget=widgets.RadioSelect,
    )
    BF_3 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(3): Самому себе я кажусь ленивым.',
        widget=widgets.RadioSelect,
    )
    BF_4 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(4): Самому себе я кажусь хорошо справляющимся со стрессом.',
        widget=widgets.RadioSelect,
    )
    BF_5 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(5): Самому себе я кажусь не сильно интересующимся искусством.',
        widget=widgets.RadioSelect,
    )
    BF_6 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(6): Самому себе я кажусь общительным.',
        widget=widgets.RadioSelect,
    )
    BF_7 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(7): Самому себе я кажусь склонным придираться к другим.',
        widget=widgets.RadioSelect,
    )
    BF_8 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(8): Самому себе я кажусь тщательно выполняющим работу.',
        widget=widgets.RadioSelect,
    )
    BF_9 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(9): Самому себе я кажусь легко начинаю нервничать.',
        widget=widgets.RadioSelect,
    )
    BF_10 = models.StringField(
        choices=[['Полностью не согласен', 'Полностью не согласен'],
                 ['Частично не согласен', 'Частично не согласен'],
                 ['Отношусь нейтрально', 'Отношусь нейтрально'],
                 ['Частично согласен', 'Частично согласен'],
                 ['Полностью согласен', 'Полностью согласен']
                 ],
        label='(10): Самому себе я кажусь человеком с богатым воображением.',
        widget=widgets.RadioSelect,
    )
    # crt_bat = models.IntegerField(
    #     label='''
    #         A bat and a ball cost 22 dollars in total.
    #         The bat costs 20 dollars more than the ball.
    #         How many dollars does the ball cost?'''
    # )
    # crt_widget = models.IntegerField(
    #     label='''
    #         "If it takes 5 machines 5 minutes to make 5 widgets,
    #         how many minutes would it take 100 machines to make 100 widgets?"
    #         '''
    # )
    # crt_lake = models.IntegerField(
    #     label='''
    #         In a lake, there is a patch of lily pads.
    #         Every day, the patch doubles in size.
    #         If it takes 48 days for the patch to cover the entire lake,
    #         how many days would it take for the patch to cover half of the lake?
    #         '''
    # )
    # free_field = models.IntegerField(
    #     label='''
    #             Ещё один вопрос (если нужно)
    #             ...
    #             ...
    #             '''
    # )
    # division_result_entered = models.FloatField(label="Result")
    #artist_prefered = models.StringField(label="Result")






# FUNCTIONS


def artists_choices(player: Player):
    choices = [("Пьер Ренуap", "Пьер Ренуap"), ("Клод Моне", "Клод Моне")]
    random.shuffle(choices)
    return choices

def get_partner(player: Player):
    return player.get_others_in_group()[0]



# def set_payoffs(group: Group):
#     p1 = group.get_player_by_id(1)
#     p2 = group.get_player_by_id(2)



# PAGES
class Intro(Page):
    pass


class Intro_1(Page):
    pass


class Intro_2(Page):
    pass


class Group_formation(Page):
    form_model = "player"
    form_fields = ["artists"]


class Quiz(Page):
    form_model = "player"
    form_fields = ["qq1",
                   "qq2",
                   "qq3",
                   "qq4",
                   # "qq5",
                   ]

    @staticmethod
    def error_message(player, values):
        for k, v in values.items():
            if Constants.correct_answers[k] != v:
                return "Не на все вопросы Вы ответили правильно. Попробуйте ещё раз!"


class MyPage(Page):
    form_model = "player"
    form_fields = ["number_entered"]

    @staticmethod
    def vars_for_template(player: Player):
        p2 = player.get_others_in_group()[0]
        return {
            "p2": p2
        }

class Waiting_1(WaitPage):
    pass


class Waiting_2(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        total_profit = 0
        for player in group.get_players():
            if player.number_entered < 6:
                total_profit += player.number_entered * Constants.endowment
            else:
                total_profit += 0
        group.total_profit = total_profit


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        player.payoff = player.group.total_profit / Constants.players_per_group


class Beliefs(Page):
    form_model = 'player'
    form_fields = ['belief_1', 'belief_2', 'belief_3', 'belief_4', 'belief_5', 'belief_6']

    @staticmethod
    def vars_for_template(player: Player):
        p2 = player.get_others_in_group()[0]
        return {
            "p2": p2
        }

    @staticmethod
    def error_message(player, values):
        print('values is', values)
        if values['belief_1'] + values['belief_2'] + values['belief_3'] + values['belief_4'] + values['belief_5'] + \
                values['belief_6'] != 100:
            return 'Сумма ответов должна равняться 100!'


class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age',
                   'gender',
                   'income'
                   ]

class BFI_10(Page):
    form_model = 'player'
    form_fields = ['BF_1',
                   'BF_2',
                   'BF_3',
                   'BF_4',
                   'BF_5',
                   'BF_6',
                   'BF_7',
                   'BF_8',
                   'BF_9',
                   'BF_10'
                   ]


class Show_artists(Page):
      form_model = 'player'
      @staticmethod
      def vars_for_template(player: Player):
          p2 = player.get_others_in_group()[0]
          return {
              "p2": p2
          }
#     # names must correspond to fields in models.py
#     form_fields = ['division_result_entered']
#
#     @staticmethod
#     def vars_for_template(player):
#         player.random_number = random.randint(1, 100)
#         if player.is_treatment_1:
#             divisor = Constants.divisor_treatment_1
#         else:
#             divisor = Constants.divisor_treatment_2
#         return {
#             "divisor": divisor,
#         }


page_sequence = [
                Intro_1,
                Intro_2,
                Quiz,
                Group_formation,
                Waiting_1,
                # Show_artists,
                MyPage,
                Beliefs,
                Questionnaire,
                BFI_10,
                Waiting_2,
                Results
                ]
