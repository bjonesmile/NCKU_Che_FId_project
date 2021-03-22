import sys
import math
import random
import numpy as np
import AlcoholicCSTR as problem

proble_Nz = 15
Nz = proble_Nz*2
MIN_POINT_SISTANCE = 3
SIM_TIME = 240
AVAILABLE_CHOICE_NUMBER = 0


class State(object):
    def __init__(self):
        self.current_value = 0.0
        # For the first root node, the index is 0 and the game should start from 1
        self.current_round_index = 0
        self.cumulative_choices = []
        self.available_switch_point = None
        self.available_switch_point_num = None

    def get_current_value(self):
        return self.current_value

    def set_current_value(self, value):
        self.current_value = value

    def get_current_round_index(self):
        return self.current_round_index

    def set_current_round_index(self, turn):
        self.current_round_index = turn

    def get_cumulative_choices(self):
        return self.cumulative_choices

    def set_cumulative_choices(self, choices):
        self.cumulative_choices = choices

    def is_terminal(self):
        # The round index starts from 1 to max round number
        is_finish = False
        if 't' in self.cumulative_choices:
            is_finish = True
        elif 't' not in self.cumulative_choices and len(self.cumulative_choices) == Nz:
            is_finish = True
        elif self.get_available_switch_point() == 1:
            is_finish = True
        return is_finish

    def compute_reward(self):
        solver = problem.AlcoholicCSTR(proble_Nz)
        solver.setStartDirect(-1,-1)
        FId = solver.solve_result(self.cumulative_choices,[])
        
        return -math.pow(FId,2)

    def set_available_switch_point(self):
        if len(self.cumulative_choices) == 0 :
            last_point = MIN_POINT_SISTANCE
        else:
            last_point = self.cumulative_choices[-1]
        
        if abs(last_point+MIN_POINT_SISTANCE-SIM_TIME) < MIN_POINT_SISTANCE :
            available_switch_point = ['t']
        else:
            available_switch_point = list(np.arange(last_point+MIN_POINT_SISTANCE,SIM_TIME,MIN_POINT_SISTANCE,dtype=np.int))
            available_switch_point.insert(0,'t')

        if len(self.cumulative_choices) == Nz :
            available_switch_point = ['t']
        #print(f"available_switch_point: {available_switch_point}")
        self.available_switch_point = available_switch_point
        self.available_switch_point_num = len(available_switch_point)

    def get_available_switch_point(self):
        if self.available_switch_point_num == None :
            self.set_available_switch_point()
        return self.available_switch_point_num

    def get_next_state_with_random_choice(self):
        if self.available_switch_point_num is None :
            self.set_available_switch_point()
        random_choice = random.choice([choice for choice in self.available_switch_point])

        """solver = problem.AlcoholicCSTR(Nz)
        solver.setStartDirect(-1,-1)
        FId = solver.solve_result(self.cumulative_choices + [random_choice],[])"""

        next_state = State()
        next_state.set_current_value(random_choice)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices + [random_choice])

        return next_state

    def get_next_state_with_spec_choice(self,choice):
        print("spec choice", choice)
        solver = problem.AlcoholicCSTR(Nz)
        solver.setStartDirect(-1,-1)
        FId = solver.solve_result(self.cumulative_choices + [choice],[])
        print("init FId:",FId)
        next_state = State()
        next_state.set_current_value(choice)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices + [choice])

        return next_state

    def __repr__(self):
        return "State: {}, value: {}, round: {}, choices: {}".format(
            hash(self), self.current_value, self.current_round_index,
            self.cumulative_choices)


class Node(object):
    """
    蒙特卡罗树搜索的树结构的Node，包含了父节点和直接点等信息，还有用于计算UCB的遍历次数和quality值，还有游戏选择这个Node的State。
    """

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0

        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_children(self):
        return self.children

    def get_visit_times(self):
        return self.visit_times

    def set_visit_times(self, times):
        self.visit_times = times

    def visit_times_add_one(self):
        self.visit_times += 1

    def get_quality_value(self):
        return self.quality_value

    def set_quality_value(self, value):
        self.quality_value = value

    def quality_value_add_n(self, n):
        self.quality_value += n

    def is_all_expand(self):
        return len(self.children) == self.state.get_available_switch_point()

    def add_child(self, sub_node):
        sub_node.set_parent(self)
        self.children.append(sub_node)

    def __repr__(self):
        return "Node: {}, Q/N: {}/{}, state: {}".format(
            hash(self), self.quality_value, self.visit_times, self.state)


def tree_policy(node):
    # Check if the current node is the leaf node
    while node.get_state().is_terminal() == False:
        if node.is_all_expand():
            node = best_child(node, True)
        else:
            # initial consider all 1 level action and expand sub node
            sub_node = init_expand(node,len(node.children))
            return sub_node
        """
        else:
            # Return the new sub node
            sub_node = expand(node)
            return sub_node
        """

        # Return the leaf node
        return node


def default_policy(node):
    """
    蒙特卡罗树搜索的Simulation阶段，输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。
    基本策略是随机选择Action。
    """

    # Get the state of the game
    current_state = node.get_state()
    # Run until the game over
    while current_state.is_terminal() == False:

        # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice()
        #print("default_policy current state:",current_state)
    
    final_state_reward = current_state.compute_reward()
    return final_state_reward

def init_expand(node,action_index):
    """
    first search all possible action from root node and expand it 
    """
    possible_action = node.get_state().available_switch_point[action_index]
    new_state = node.get_state().get_next_state_with_spec_choice(possible_action)

    sub_node = Node()
    sub_node.set_state(new_state)
    node.add_child(sub_node)
    print("init expand",sub_node)

    return sub_node

def expand(node):
    """
    输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点。注意，需要保证新增的节点与其他节点Action不同。
    """

    tried_sub_node_states = [
        sub_node.get_state().get_cumulative_choices() for sub_node in node.get_children()
    ]

    new_state = node.get_state().get_next_state_with_random_choice()

    # Check until get the new state which has the different action from others
    while new_state.get_cumulative_choices() in tried_sub_node_states:
        new_state = node.get_state().get_next_state_with_random_choice()

    sub_node = Node()
    sub_node.set_state(new_state)
    node.add_child(sub_node)
    print("expand",sub_node)
    return sub_node


def best_child(node, is_exploration):
    """
    使用UCB算法，权衡exploration和exploitation后选择得分最高的子节点，注意如果是预测阶段直接选择当前Q值得分最高的。
    """

    # TODO: Use the min float value
    best_score = -sys.maxsize
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

        # Ignore exploration for inference
        if is_exploration:
            C = 1 / math.sqrt(2.0)
        else:
            C = 0.0

        # UCB = quality / times + C * sqrt(2 * ln(total_times) / times)
        left = sub_node.get_quality_value() / sub_node.get_visit_times()
        right = 2.0 * math.log(node.get_visit_times()) / sub_node.get_visit_times()
        score = left + C * math.sqrt(right)

        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    
    return best_sub_node


def backup(node, reward):
    """
    蒙特卡洛树搜索的Backpropagation阶段，输入前面获取需要expend的节点和新执行Action的reward，反馈给expend节点和上游所有节点并更新对应数据。
    """

    # Update util the root node
    while node != None:
        # Update the visit times
        node.visit_times_add_one()

        # Update the quality value
        node.quality_value_add_n(reward)

        # Change the node to the parent node
        node = node.parent


def monte_carlo_tree_search(node):
    """
    实现蒙特卡洛树搜索算法，传入一个根节点，在有限的时间内根据之前已经探索过的树结构expand新节点和更新数据，然后返回只要exploitation最高的子节点。
    蒙特卡洛树搜索包含四个步骤，Selection、Expansion、Simulation、Backpropagation。
    前两步使用tree policy找到值得探索的节点。
    第三步使用default policy也就是在选中的节点上随机算法选一个子节点并计算reward。
    最后一步使用backup也就是把reward更新到所有经过的选中节点的节点上。
    进行预测时，只需要根据Q值选择exploitation最大的节点即可，找到下一个最优的节点。
    """

    computation_budget = 600
    show_period = 29-1
    # Run as much as possible under the computation budget
    for i in range(computation_budget):
        print("compute times:",i)

        # 1. Find the best node to expand
        expand_node = tree_policy(node)
        print("selected sub node:",expand_node)
        # 2. Random run to add node and get reward
        reward = default_policy(expand_node)

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)
        
        if i%show_period == 0 :
            show_current_sub_node_state(node)
    # N. Get the best next node
    best_next_node = best_child(node, False)

    return best_next_node


def show_current_sub_node_state(node):
    tried_sub_node_states = [
        sub_node for sub_node in node.get_children()
    ]

    print(f"current sub_node state; sub_node number: {len(tried_sub_node_states)}")
    for sub_node in tried_sub_node_states :
        print(sub_node)


def main():
    # Create the initialized state and initialized node
    init_state = State()
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node

    # Set the rounds to play
    i = 1
    while current_node.get_state().is_terminal() == False :
        current_node.get_state().set_available_switch_point()
        print("possible actions to next state",current_node.get_state().get_available_switch_point())
        print("simulate Nz level: {}".format(i))
        current_node = monte_carlo_tree_search(current_node)
        print("Choose node: {}".format(current_node))

    return current_node.get_state().get_cumulative_choices()


if __name__ == "__main__":
    """MCTS_result = main()
    print("suc")
    exit()"""
    guess_point = 174
    vertexlist = list(np.arange(guess_point+MIN_POINT_SISTANCE,SIM_TIME,MIN_POINT_SISTANCE,dtype=np.int))
    vertexlist.clear()
    vertexlist.insert(0,'t')
    solver = problem.AlcoholicCSTR(2)
    solver.setStartDirect(-1,-1)
    i = 0
    FId_sum = 0
    for vertex in vertexlist :
        FId = solver.solve_result([guess_point]+[vertex],[])
        FId_sum += -math.pow(FId,1.5)
        i+=1
    print("total simulate:",i)
    print("avg of FId",FId_sum/i)

    FId = solver.solve_result([237],[])

    exit()
