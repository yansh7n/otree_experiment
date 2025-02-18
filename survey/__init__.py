from otree.api import *

TYPE = 1 # 实验局的类型，1=base；2=complete，3=incomplete；4=ambiguous_complete

class C(BaseConstants):
    NAME_IN_URL = 'survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SURVEY_PROFIT = 5 # 问卷的报酬
    SHOW_UP_FEE = 10 # 出场费


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    type = models.IntegerField(initial=TYPE)
    age = models.StringField(
        choices=['20岁以下', '20-22岁', '23-25岁', '25岁以上'],
        label='(1)你的年龄是几周岁?',
        widget=widgets.RadioSelect,
    )
    gender = models.StringField(
        choices=['男', '女'],
        label='(2)你的性别是?',
        widget=widgets.RadioSelect,
    )
    grade = models.StringField(
        choices=['大一', '大二', '大三', '大四', '硕士生', '博士生'],
        label='(3)你是几年级的学生?',
        widget=widgets.RadioSelect,
    )
    rural_or_urban = models.StringField(
        choices=['农村', '城镇'],
        label='(4)你来自农村还是城镇?',
        widget=widgets.RadioSelect,
    )
    is_economics = models.StringField(
        choices=['是', '否'],
        label='(5)你是否为经济类专业学生?',
        widget=widgets.RadioSelect,
    )
    is_member = models.StringField(
        choices=['是', '否'],
        label='(6)你是否为党员?',
        widget=widgets.RadioSelect,
    )
    is_cadre = models.StringField(
        choices=['是', '否'],
        label='(7)你是否为学生干部?',
        widget=widgets.RadioSelect,
    )
    annual_income = models.StringField(
        choices=['一万人民币以下', '1-5万人民币', '5-10万人民币', '10-20万人民币', '20万人民币以上'],
        label='(8)你的家庭总年收入(包括所有形式的收益)大概在?',
        widget=widgets.RadioSelect,
    )
    ever_joined = models.StringField(
        choices=['是', '否'],
        label='(9)你之前是否参加过经济学/心理学实验?',
        widget=widgets.RadioSelect,
    )
    trust_level = models.StringField(
        choices=['大多数人可以信任', '要越小心越好'],
        label='(10)一般来说，你认为大多数人是可以信任的，还是和人相处要越小心越好?',
        widget=widgets.RadioSelect,
    )
    keen_level = models.StringField(
        choices=['是乐于助人的', '是为自己谋利'],
        label='(11)一般来说，你认为大多数时候是乐于助人的，还是他们只不过是为自己谋利?',
        widget=widgets.RadioSelect,
    )
    reliability = models.StringField(
        choices=['很不值得信任', '不值得信任', '一般不值得信任', '一般值得信任', '值得信任', '很值得信任'],
        label='(12)你觉得自己是值得被别人信任的一个人吗?',
        widget=widgets.RadioSelect,
    )
    is_fair_treatment = models.StringField(
        choices=['非常同意', '同意', '不太确定', '不太同意', '不同意'],
        label='(13)在生活中，我认为我得到了公平的对待?',
        widget=widgets.RadioSelect,
    )
    feel_sympathy = models.StringField(
        choices=['非常同意', '同意', '不太确定', '不太同意', '不同意'],
        label='(14)对于弱者，我时常感到同情，并想帮助他们?',
        widget=widgets.RadioSelect,
    )
    is_hesitant = models.StringField(
        choices=['是', '否'],
        label='(15)做决定时，你时常犹豫不决?',
        widget=widgets.RadioSelect,
    )
    investment_willingness = models.StringField(
        choices=['一定赚5%', '可能亏30%，可能赚70%', '可能全部亏损，可能赚300%'],
        label='(16)假设有三种投资，你更倾向于哪一个?',
        widget=widgets.RadioSelect,
    )
    feedback1 = models.StringField(
        label='在实验的过程中您是怎么对下一期收入进行预测的？',
        initial = '',
        blank=True
    )
    feedback2 = models.StringField(
        label='在实验过程中您是怎么对本期总收入进行的预测？',
        initial = '',
        blank=True
    )
    feedback3 = models.StringField(
        label='您有没有按照预期总收入平均分配消费？如果没有，您是怎么决定自己本期的消费的？',
        initial = '',
        blank=True
    )
    feedback4 = models.StringField(
        label='您觉得实验中哪些信息对您的决策是最有用的？',
        initial = '',
        blank=True
    )
    feedback5 = models.StringField(
        label='您有什么其他对实验的改进建议吗？',
        initial = '',
        blank=True
    )
    feedback6 = models.StringField(
        label='您觉得暂时冲击对您的决策有影响吗？',
        initial = '',
        blank=True
    )
    feedback7 = models.StringField(
        label='当您在做决策的时候，您如何判断冲击更有可能是暂时冲击还是永久冲击？',
        initial = '',
        blank=True
    )
    feedback8 = models.StringField(
        label='您更担心的是永久冲击还是暂时冲击？',
        initial = '',
        blank=True
    )
    feedback9 = models.StringField(
        label='您觉得第3/4期和第5/6期您在做决策的时候有什么区别？',
        initial = '',
        blank=True
    )


# FUNCTIONS
# PAGES
class Instructions(Page):
    pass


class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'grade', 'rural_or_urban', 'is_economics', 'is_member', 'is_cadre', 'annual_income',
                   'ever_joined', 'trust_level', 'keen_level', 'reliability',
                   'is_fair_treatment', 'feel_sympathy', 'is_hesitant', 'investment_willingness']


class Feedback(Page):
    form_model = 'player'
    form_fields = ['feedback1','feedback2','feedback3','feedback4','feedback5','feedback6','feedback7','feedback8','feedback9']


class EndResults(Page):
    def vars_for_template(self):
        return {'point': self.participant.vars['point'],
                'point_profit': self.participant.vars['point_profit'],
                'answer_profit': self.participant.vars['answer_profit'],
                'final_profit': self.participant.vars['final_profit']}


page_sequence = [Instructions, Demographics, Feedback, EndResults]
