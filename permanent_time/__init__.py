import random
import numpy as np
import math
from otree.api import *

doc = """
这是一个消费者实验。
"""

# 一些列表类型的参数

SHOCK_SIG = ['无冲击','暂时冲击','永久冲击']
SHOCK_DIST = [0, 2, 2, 2, 2, 2] # 冲击类型
PARAMETERS_NONE = [[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]] # 无冲击的参数
PARAMETERS_SHORT_RUN = [[-0.2, -0.2, 0, 0, 0, 0],[-0.2, -0.2, 0, 0, 0, 0]] # 短期冲击的参数（还要加上第一二轮扣除的）
PARAMETERS_LONG_RUN = [[-0.2, -0.2, -0.2, -0.2, -0.2, -0.2],[0.2, 0.2, 0.2, 0.2, 0.2, 0.2]] # 长期冲击的参数
PARAMETERS_SHOCK = [PARAMETERS_NONE, PARAMETERS_SHORT_RUN, PARAMETERS_LONG_RUN]

POLICY_SIG = ['无政策','跨期支付政策','再分配政策']
POLICY_DIST = [0, 1, 1, 1, 1, 1] # 政策类型
PARAMETERS_NO_POLICY = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]] # 无政策
PARAMETERS_TIME = [[0.1, 0.1, 0, 0, 0, 0], [0.1, 0.1, 0, 0, 0, 0]] # 跨期支付
PARAMETERS_REDISTRIBUTION = [[0.1, 0.1, 0, 0, 0, 0], [-0.1, -0.1, 0, 0, 0, 0]] # 再分配
PARAMETERS_POLICY = [PARAMETERS_NO_POLICY, PARAMETERS_TIME, PARAMETERS_REDISTRIBUTION]

# CLASSES

class C(BaseConstants):
    NAME_IN_URL = 'permanent_time'
    PLAYERS_PER_GROUP = 6 # 每组6个人
    NUM_ROUNDS = 36 # 共36轮
    ENDOWMENT = 100 # 初始禀赋100
    NUM_PERIODS = 6 # 每个周期6个轮次
    UTILITY_PARA = 0.01 # 效用的兑换率
    NUM_BONUS = 3 # 抽取回答问题的轮次数
    PAY_FOR_ANS = 1 # 回答正确后给的钱
    SURVEY_PROFIT = 5 # 问卷的报酬
    SHOW_UP_FEE = 10 # 出场费


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    # 总消费
    total_consumption = models.FloatField(initial=0) 
    
    # 关于周期的变量
    cycle = models.IntegerField(initial=1)
    period = models.IntegerField(initial=1)


class Player(BasePlayer):

    # 关于冲击的变量
    # 冲击类型，0=无冲击；1=短期冲击；2=长期冲击
    shock_type = models.IntegerField(initial=0)
    # 关于冲击的信号，无冲击，短期冲击，长期冲击
    signal_shock = models.StringField(initial='/')
    # 冲击系数
    parameter_shock = models.FloatField(initial=0)

    # 关于政策的变量
    # 政策类型，0=无政策；1=跨期支付政策；2=再分配政策
    policy_type = models.IntegerField(initial=0)
    # 关于政策的信号，无政策，跨期支付政策，再分配政策
    signal_policy = models.StringField(initial='/')
    # 政策系数
    parameter_policy = models.FloatField(initial=0)

    # 收入返还
    income_returned = models.FloatField(initial=0)

    # 关于消费决策的变量
    # 总财富
    wealth = models.FloatField(initial=0)
    # 当期基准收入
    income_base = models.FloatField(initial=0)
    # 当期实际收入
    income = models.FloatField(initial=100)
    # 当期消费
    consumption = models.FloatField(initial=0, label='请选择消费值（允许超前消费），在本轮用于购买积分：', min=0,max=200)
    # 效用
    utility = models.FloatField(initial=0)
    # 储蓄
    saving = models.FloatField(initial=0)
    # 总收入
    total_income = models.FloatField(initial=100)
    # 总消费
    total_consume = models.FloatField(initial=0)

    # 关于信念更新的变量
    # 对下一轮收入的预测
    income_predict = models.FloatField(label='请预测下一轮收入：')
    # 对总收入的预测
    total_income_predict = models.FloatField(label='请预测本周期（6轮）的总收入：', min=100)
    # 当期回答正确的问题数
    num_of_correct_ans = models.IntegerField(initial=0)
    # 回答问题的收益
    profit_ans = models.FloatField(initial=0)

    # 周期变量
    total_income = models.FloatField(initial=0)
    total_utility = models.FloatField(initial=0)
    cycle = models.IntegerField()
    period = models.IntegerField()

    # 收益
    profit_point = models.FloatField(initial=0)
    profit_all = models.FloatField(initial=0)

    # 问卷问题
    Q1 = models.StringField(
        choices=['对', '错'],
            label='1.在每一轮，您选择的消费金额必须低于您现在所拥有的财富。',
            widget=widgets.RadioSelect,
    )
    Q2 = models.FloatField(label='2.根据消费值与积分的换算表，如果您在某一轮选择的消费值为20，在本轮您将获得的积分点数为：', min=0) 
    Q3 = models.FloatField(label='3.假设您现在处于某一周期的第3轮，在本轮开始时您所拥有的财富为150，在第2轮中您所在的组内所有被试的总消费值为300，您在本轮的收入为：', min=0)
    Q4 = models.StringField(
        choices=['120和140', '110和110','40和80','140和80'],
        label='4.假设您处于某一周期的第5轮，在本轮开始时您拥有的财富是100，您本轮获得的收入是40，且您预计在第6轮您将获得的收入为80。如果您的预测是准确的，为了最大化您的收益，那么您应该选择在本轮和下一轮分别消费：',
        widget=widgets.RadioSelect,
    )
    Q5 = models.StringField(
        choices=['对', '错'],
            label='5.理论上说，如果您对本周期内总收入的预期是准确的，那么您的最优选择应该是在每一轮平均分配消费值',
            widget=widgets.RadioSelect,
    )


# FUNCTIONS

# 添加有顺序分配label的函数
def creating_session(subsession: Subsession):
    labels = [1,3,5,7,8,10,12,14,15,17,21,22,24,27,29,31,33,38,40,61,63,65,67,69]
    for p,label in zip(subsession.get_players(),labels):
        p.participant.label = label


# 随机分组
def creating_groups(subsession):
    # 第一轮，把被试随机分配到小组
    if subsession.round_number == 1:
        subsession.group_randomly()
    # 每个周期的第一轮，在小组内打乱被试顺序
    elif subsession.round_number % C.NUM_PERIODS == 1 and subsession.round_number > 1: 
        subsession.group_like_round(subsession.round_number-1)
        matrix = subsession.get_group_matrix()
        for row in matrix:
            random.shuffle(row)
        subsession.set_group_matrix(matrix)
    # 其他轮次，不改变
    else: 
        subsession.group_like_round(subsession.round_number-1)
    # 对每个组设置周期和轮次
    groups = subsession.get_groups()
    for g in groups:
        n = 1  # 从 n=1 开始，逐步增加，直到条件满足
        while subsession.round_number > C.NUM_PERIODS * n:
            n += 1
        g.cycle = n
        g.period = subsession.round_number - C.NUM_PERIODS * (g.cycle - 1)


# 最主要的函数，决定每个周期的冲击、每个轮次的收入系数、被试看到的信号、被试的收入、被试的财富
def set_environment(group: Group):
    players = group.get_players()
    if group.period > 1:
        prev_players = [p.in_round(group.round_number-1) for p in players]
        consumptions = [p.consumption for p in prev_players]
        group.total_consumption = sum(consumptions)
    for p in players:
        # 轮次变量
        p.cycle = group.cycle
        p.period = group.period

        # 冲击情况（所有人面临的冲击是共同的）
        p.shock_type = SHOCK_DIST[group.cycle-1]
        # 关于冲击的信号
        p.signal_shock = signal_shock(p.shock_type)

        # 政策情况
        p.policy_type = POLICY_DIST[group.cycle-1]
        # 关于政策的信号
        p.signal_policy = signal_policy(p.policy_type)

        # 被试的冲击参数
        if p.id_in_group <= 0.5*len(players):
            p.parameter_shock = PARAMETERS_SHOCK[p.shock_type][0][group.period-1]
        else:
            p.parameter_shock = PARAMETERS_SHOCK[p.shock_type][1][group.period-1]
        
        # 被试的政策参数
        if p.id_in_group <= 0.5*len(players):
            p.parameter_policy = PARAMETERS_POLICY[p.policy_type][0][group.period-1]
        else:
            p.parameter_policy = PARAMETERS_POLICY[p.policy_type][1][group.period-1]

        # 被试的收入返还
        p.income_returned = 0
        if group.period == C.NUM_PERIODS and p.shock_type == 1:
            prev_player11 = p.in_round(group.round_number-C.NUM_PERIODS+1) # 第一轮的自己
            prev_player12 = p.in_round(group.round_number-C.NUM_PERIODS+2) # 第二轮的自己
            p.income_returned = p.income_returned + prev_player11.income_base*(-PARAMETERS_SHORT_RUN[0][group.period-C.NUM_PERIODS]) + prev_player12.income_base*(-PARAMETERS_SHORT_RUN[0][group.period-C.NUM_PERIODS+1])
        if group.period == C.NUM_PERIODS and p.policy_type == 1:
            prev_player11 = p.in_round(group.round_number-C.NUM_PERIODS+1) # 第一轮的自己
            prev_player12 = p.in_round(group.round_number-C.NUM_PERIODS+2) # 第二轮的自己
            p.income_returned = p.income_returned + prev_player11.income_base*(-PARAMETERS_TIME[0][group.period-C.NUM_PERIODS]) + prev_player12.income_base*(-PARAMETERS_TIME[0][group.period-C.NUM_PERIODS+1])
        
        # 基准收入和实际收入
        if group.period == 1:
            p.income_base = C.ENDOWMENT # 第一轮，基准收入为100
            p.income = p.income_base*(1+p.parameter_shock+p.parameter_policy) # 第一轮，实际收入为100*(1+冲击系数+政策系数)
        else:
            p.income_base = round(group.total_consumption/C.PLAYERS_PER_GROUP, 2) # 后续轮次，基准收入为上期消费/组内被试人数
            p.income = round(p.income_base*(1+p.parameter_shock+p.parameter_policy) + p.income_returned, 2) # 后续轮次，收入为上期消费/组内被试人数*冲击系数+收入返还

        # 被试的财富        
        if group.period == 1:
            p.wealth = p.income # 第一轮，财富为100
        else:
            prev_player2 = p.in_round(group.round_number-1)
            p.wealth = round(prev_player2.wealth - prev_player2.consumption + p.income, 2) # 后续轮次，总财富为上期财富-上期消费+本期收入
        prev_player3 = p.in_rounds((group.cycle-1) * C.NUM_PERIODS + 1, group.round_number-1)
        p.total_income = round(sum(r.income for r in prev_player3),2)
        p.total_consume = round(sum(r.consumption for r in prev_player3),2)


# 设置信号返回的规则（分为完全信息、不完全信息、信息摩擦、模糊）
def signal_shock(shock_type):
    result = SHOCK_SIG[shock_type]
    return result

def signal_policy(policy_type):
    result = POLICY_SIG[policy_type]
    return result


# 设置消费的效用
def set_utility(group: Group):
    players = group.get_players()
    for p in players:
        if group.period == 6:
            p.utility = utility(p.wealth) # 最后1轮
            p.consumption = p.wealth
            p.saving = 0
            player_in_cycle = p.in_rounds(group.round_number - C.NUM_PERIODS + 1, group.round_number)
            p.total_income = 0
            p.total_consume = 0
            p.total_utility = 0
            for q in player_in_cycle:
                p.total_income += q.income
                p.total_consume += q.consumption
                p.total_utility += q.utility
        else:
            p.utility = utility(p.consumption)
            p.saving = round(p.wealth - p.consumption, 2)


def utility(consumption):
    u = 250*(1-math.exp(-0.02*consumption))
    return round(u, 2)


# 判断回答问题的收益
def question_profit(group: Group):
    players = group.get_players()
    consumptions = [p.consumption for p in players]
    group.total_consumption = sum(consumptions)
    for p in players:
        bonus_rounds1 = sample_bonus_rounds(C.NUM_ROUNDS, C.NUM_BONUS)
        for round in bonus_rounds1:
            p_round = p.in_round(round)
            p_next_round = p.in_round(round+1)
            if abs(p_round.income_predict - p_next_round.income) <= 5:    
                p.num_of_correct_ans += 1
        bonus_rounds2 = sample_bonus_rounds(C.NUM_ROUNDS, C.NUM_BONUS)
        for round in bonus_rounds2:
            p_round = p.in_round(round)
            player_in_cycle = p.in_rounds(((round-0.01) // (C.NUM_PERIODS)) * C.NUM_PERIODS + 1, ((round-0.01) // (C.NUM_PERIODS) + 1) * C.NUM_PERIODS)
            incomes = [q.income for q in player_in_cycle]
            sum_of_income = sum(incomes)
            if abs(p_round.total_income_predict - sum_of_income) <= 10:
                p.num_of_correct_ans += 1
        p.profit_ans = p.num_of_correct_ans * C.PAY_FOR_ANS


# 抽取固定的轮次（从1到N，排除6的倍数）
def sample_bonus_rounds(N, count):
    # 构建一个不包含 6 的倍数的整数列表
    candidates = [i for i in range(1, N + 1) if i % 6 != 0]
    # 随机抽取指定数量的数字
    return random.sample(candidates, count)


# 收益计算函数
def set_profit(subsession: Subsession):
    if subsession.round_number == C.NUM_ROUNDS:
        players = subsession.get_players()
        for p in players:
            all_rounds_data = p.in_all_rounds()
            # 所抽取轮次的回答正确数量
            p.participant.vars['answer_profit'] = p.profit_ans
            # 计算之前所有轮的效用总和，乘效用兑换率，并保留两位小数为收益
            p.participant.vars['point'] = round(sum(player.utility for player in all_rounds_data), 2)
            p.profit_point = round((sum(player.utility for player in all_rounds_data)-3000) * C.UTILITY_PARA, 2)
            p.participant.vars['point_profit'] = p.profit_point
            # 总收益
            p.profit_all = round(p.profit_ans + p.profit_point, 2)
            if p.round_number == C.NUM_ROUNDS:
                p.profit_all += C.SURVEY_PROFIT # 问卷收益
                p.profit_all += C.SHOW_UP_FEE # 出场费
            p.participant.vars['final_profit'] = p.profit_all
    else:
        pass


# PAGES
class Instruction(Page):
    def is_displayed(player: Player):
        return player.round_number == 1


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(Q1='错', Q2=82.42, Q3=50, Q4='110和110', Q5='对')
        errors = {name: '错误' for name in solutions if values[name] != solutions[name]}
        if errors:
            return errors


class ResultsWaitPage1(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = creating_groups


class Information(Page):
    def is_displayed(player: Player):
        return player.round_number % C.NUM_PERIODS == 1


class ResultsWaitPage2(WaitPage):
    after_all_players_arrive = set_environment


class Consumption1(Page):
    form_model = 'player'
    form_fields = ['income_predict', 'total_income_predict']
    @staticmethod
    def vars_for_template(player):
        return dict(cycle_data = player.in_rounds((player.cycle - 1) * C.NUM_PERIODS + 1, player.round_number - 1))
    @staticmethod
    def live_method(player, consumption):
        player.consumption = consumption
    
    def is_displayed(player: Player):
        return player.round_number % C.NUM_PERIODS != 0


class Consumption2(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(cycle_data = player.in_rounds((player.cycle - 1) * C.NUM_PERIODS + 1, player.round_number))
    
    def is_displayed(player: Player):
        return player.round_number % C.NUM_PERIODS == 0


class ResultsWaitPage3(WaitPage):
    after_all_players_arrive = set_utility


class ResultsWaitPage4(WaitPage):
    after_all_players_arrive = question_profit

    # 最后1轮结算每个被试的任务收益
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class ResultsWaitPage5(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = set_profit

    # 最后1轮结算每个被试的任务收益
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    

page_sequence = [Instruction, Comprehension, ResultsWaitPage1, Information, ResultsWaitPage2, Consumption1, ResultsWaitPage3, Consumption2, ResultsWaitPage4, ResultsWaitPage5]
