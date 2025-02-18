from os import environ

SESSION_CONFIGS = [
    # 问卷（用于测试）
    dict(
        name='survey',
        app_sequence=['survey'],
        num_demo_participants=1,
    ),
    # 基准,    
    dict(
        name='base',
        app_sequence=['base','survey'],
        num_demo_participants=6,
    ),
    # 基准+跨期支付,    
    dict(
        name='base_time',
        app_sequence=['base_time','survey'],
        num_demo_participants=6,
    ),
    # 基准+再分配,    
    dict(
        name='base_redistribution',
        app_sequence=['base_redistribution','survey'],
        num_demo_participants=6,
    ), 
    # 暂时冲击,    
    dict(
        name='temporary',
        app_sequence=['temporary','survey'],
        num_demo_participants=6,
    ),
    # 暂时冲击+跨期支付,    
    dict(
        name='temporary_time',
        app_sequence=['temporary_time','survey'],
        num_demo_participants=6,
    ),
    # 暂时冲击+再分配,    
    dict(
        name='temporary_redistribution',
        app_sequence=['temporary_redistribution','survey'],
        num_demo_participants=6,
    ), 
    # 永久冲击,    
    dict(
        name='permanent',
        app_sequence=['permanent','survey'],
        num_demo_participants=6,
    ),
    # 永久冲击+跨期支付,    
    dict(
        name='permanent_time',
        app_sequence=['permanent_time','survey'],
        num_demo_participants=6,
    ),
    # 永久冲击+再分配,    
    dict(
        name='permanent_redistribution',
        app_sequence=['permanent_redistribution','survey'],
        num_demo_participants=6,
    ), 
    # 不确定冲击,    
    dict(
        name='incomplete',
        app_sequence=['incomplete','survey'],
        num_demo_participants=6,
    ),
    # 不确定冲击+跨期支付,    
    dict(
        name='incomplete_time',
        app_sequence=['incomplete_time','survey'],
        num_demo_participants=6,
    ),
    # 不确定冲击+再分配,    
    dict(
        name='incomplete_redistribution',
        app_sequence=['incomplete_redistribution','survey'],
        num_demo_participants=6,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=10.00, doc=""
)

PARTICIPANT_FIELDS = ['product', 'point', 'point_profit', 'answer_profit', 'final_profit']
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '3299561158827'

DEBUG = True
