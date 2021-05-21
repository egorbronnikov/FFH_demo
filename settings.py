from os import environ


SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods', 'payment_info'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='guess_two_thirds',
    #     display_name="Guess 2/3 of the Average",
    #     app_sequence=['guess_two_thirds', 'payment_info'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='Real_Eff',
    #     display_name="Add up two numbers",
    #     app_sequence=['Real_Eff'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='game',
    #     display_name="Game",
    #     app_sequence=['game'],
    #     num_demo_participants=3,
    # ),
    # dict(
    #     name='prisonners_dilemma_simple',
    #     display_name="Prisonners Dilemma Simple",
    #     app_sequence=['prisonners_dilemma_simple'],
    #     num_demo_participants=4,
    # ),
    # dict(
    #     name='FFH_team',
    #     display_name="FFH_team",
    #     app_sequence=['FFH_team'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='FFH',
    #     display_name="FFH",
    #     app_sequence=['FFH'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='prisonners_delimma_advance',
    #     display_name="prisonners_delimma_advance",
    #     app_sequence=['prisonners_delimma_advance'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='dictator',
    #     display_name="dictator",
    #     app_sequence=['dictator'],
    #     num_demo_participants=2,
    # ),
    dict(
        name='FFH_Team_No_Info',
        display_name="FFH_Team_No_Info",
        app_sequence=['FFH_Team_No_Info'],
        num_demo_participants=2,
    ),
    dict(
        name='FFH_Team_M_M',
        display_name="FFH_Team_M_M",
        app_sequence=['FFH_Team_M_M'],
        num_demo_participants=2,
    ),
    # dict(
    #     name='display_image',
    #     display_name="display_image",
    #     app_sequence=['display_image'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='divide_number_treatment',
    #     display_name="divide_number_treatment",
    #     app_sequence=['divide_number_treatment'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='survey',
    #     display_name="survey",
    #     app_sequence=['survey'],
    #     num_demo_participants=2,
    # ),
    # dict(
    #     name='survey', app_sequence=['survey', 'payment_info'], num_demo_participants=1
    # ),
]





# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.010, participation_fee=0.5, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'ECU'

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('DO_NOT_LIE')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '4609193350107'

INSTALLED_APPS = ['otree']
