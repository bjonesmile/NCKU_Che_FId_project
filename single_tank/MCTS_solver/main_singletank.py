import sys
import math
import copy
import random
import numpy as np
import itertools

import SingleTank as problem
import mytimer as timer

SV_num = 1
MV_num = 1
proble_Nz = 1
Nz = proble_Nz*MV_num
constrain_N = proble_Nz
MIN_POINT_DISTANCE = 20
SIM_TIME = 800
AVAILABLE_CHOICE_NUMBER = 0
GAMMA = 1.0

direct = 1

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
        if 't' in self.cumulative_choices :
            return True

        if len(self.cumulative_choices) == constrain_N :
            is_finish = True
        elif self.get_available_switch_point() == 1:
            is_finish = True
        
        return is_finish

    def compute_Nz(self):

        nz = len(self.cumulative_choices)
        if 't' in self.cumulative_choices:
            return nz-1
        else:
            return nz

    def compute_reward(self):
        
        solver = problem.SingleTank(proble_Nz)
        solver.setStartDirect(direct)
        FId = solver.solve_result(self.cumulative_choices)
        del(solver)
        # to increase difference of the range in FId:[0,1] take square(^2)
        return -math.pow(FId,2)

    def set_available_switch_point(self,asiggn_points=None):
        # if has assign_vertex
        if asiggn_points != None :
            self.available_switch_point = asiggn_points
            self.available_switch_point_num = len(asiggn_points)
            return None

        if len(self.cumulative_choices) == 0 :
            last_point = MIN_POINT_DISTANCE
        else:
            last_point = self.cumulative_choices[-1]+MIN_POINT_DISTANCE
        
        if last_point >= SIM_TIME+1 :
            available_switch_point = ['t']
        else:
            available_switch_point = list(np.arange(last_point,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))
            available_switch_point.insert(0,'t')
            if len(self.cumulative_choices) == 0 and MIN_POINT_DISTANCE != 1:#and current round index
                available_switch_point.insert(1,1)

        if len(self.cumulative_choices) == constrain_N :
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
        print("random choice:",random_choice)

        next_state = State()
        next_state.set_current_value(random_choice)
        next_state.set_current_round_index(self.current_round_index + 1)
        next_state.set_cumulative_choices(self.cumulative_choices + [random_choice])

        return next_state

    def get_next_state_with_spec_choice(self,choice):
        print("spec choice", choice)

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
    Node of MCTS's tree structure, includind of parent and children, and function used to calculate quality(UCB)，and current state of simulation.
    """

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0
        self.best_reward = -10
        self.best_action_round = 1
        self.best_final_state = None

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
        if self.visit_times == 0:
            ratio_value = 0
        else:
            ratio_value = self.quality_value/self.visit_times
        return "Node: {}, Q/N: {}/{}, ratio: {},state: {}, best reward: {}".format(
            hash(self), self.quality_value, self.visit_times, ratio_value, self.state, self.best_reward)


def tree_policy(node):
    print("root node",node)
    # Check if the current node is the leaf node
    while node.get_state().is_terminal() == False:
        if node.is_all_expand():
            node = best_child(node, True)
        else:
            # initial consider all 1 level action and expand sub node
            sub_node = init_expand(node,len(node.children))
            return sub_node

        # Return the leaf node
        return node


def default_policy(node):
    """
    simulation step: using unform random method to expand node until the state terminal.
    """

    # Get the state of the game
    current_state = node.get_state()
    # First consider directly terminal state
    if node.get_visit_times() == 0:
        current_state.get_next_state_with_spec_choice('t')
    else:    
        # Run until the game over
        while current_state.is_terminal() == False:

            # Pick one random action to play and get next state
            current_state = current_state.get_next_state_with_random_choice()
            #print("default_policy current state:",current_state)
    
    final_state_reward = current_state.compute_reward()
    if final_state_reward > node.best_reward :
        node.best_reward = final_state_reward
        node.best_action_round = current_state.get_current_round_index()
        node.best_final_state = copy.deepcopy(current_state.get_cumulative_choices())

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
    input a node and expand from the node using uniform possibility random choose action add sub-node.
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
    use UCB alorithm，judge exploration and exploitation and select the subnode with highest value, when predicting just consider Q/N。
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
        score = left + C * math.sqrt(right) + sub_node.best_reward

        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    
    print("choose best child with score:",best_score)
    return best_sub_node

def best_child_optimal(node,gamma):
    # TODO: Use the min float value
    best_score = -sys.maxsize
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():
        print(sub_node)
        left = (1-gamma)*sub_node.get_quality_value() / sub_node.get_visit_times()
        right = gamma*(sub_node.best_reward)
        """if sub_node.best_action_round > 1 :
            right = gamma*(sub_node.best_reward+sub_node.best_reward*math.sqrt(sub_node.best_action_round/Nz))
        else:
            right = gamma*(sub_node.best_reward+sub_node.best_reward)"""
        score = left + right

        print(left,right)
        print(sub_node.get_state().get_cumulative_choices(),score)

        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    
    print("choose best child with score:",best_score)
    return best_sub_node

def backup(node, reward):
    """
    MCTS Backpropagation step: input the node need to expend，feedback to expend node and upsteam path nodes and rew new data.
    """

    reward = node.best_reward
    action_reward = node.best_action_round
    final_state = node.best_final_state

    # Update util the root node
    while node != None:
        node.best_reward = reward
        node.best_action_round = action_reward
        node.best_final_state = final_state
        # Update the visit times
        node.visit_times_add_one()

        # Update the quality value
        node.quality_value_add_n(reward)

        # Change the node to the parent node
        node = node.parent

def monte_carlo_tree_search(node,computation_budget = 1000):
    """
    MCTS contain four steps: Selection、Expansion、Simulation、Backpropagation。
    first strep and scond step: use tree policy find sub node worth to expolre.
    third srep: use default policy to choose random path until terminated and get reward.
    fourth step: Backpropagation, renew reward to all node the random path passed.
    for predicting, just according to Q value to choose exploitation node.
    """

    min_FId = -1
    min_state = None

    show_period = 100
    period_num = 1
    
    print("computation budget:",computation_budget)
    # Run as much as possible under the computation budget
    for i in range(computation_budget):
        print("compute times:",i)

        # 1. Find the best node to expand
        expand_node = tree_policy(node)
        print("selected sub node:",expand_node)
        # 2. Random run to add node and get reward
        reward = default_policy(expand_node)

        if reward >= min_FId :
            min_state = copy.deepcopy(expand_node.get_state().get_cumulative_choices())
            min_FId = reward
            print(expand_node.best_reward)
            print(expand_node.best_action_round)
            print(expand_node.best_final_state)
        print(f"now min FId: {math.sqrt(-min_FId)}, min state: {min_state}")

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)
        
        show_period -= 1
        if show_period == 0 :
            show_current_sub_node_state(node,period_num)
            show_period = 100
            period_num += 1
    # N. Get the best next node
    best_next_node = best_child_optimal(node, GAMMA)

    return best_next_node


def show_current_sub_node_state(node,period):
    tried_sub_node_states = [
        sub_node for sub_node in node.get_children()
    ]

    with open("search_subnode_history_round"+str(node.get_state().get_current_round_index()+1)+".txt",'a') as wfile :
        print(f"period: {period}",file=wfile)
        for sub_node in tried_sub_node_states :
            print(sub_node,file= wfile)
        print('\n',file=wfile)

def main():
    const_t = int(10)
    # Create the initialized state and initialized node
    init_state = State()
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node

    # Set the rounds to play
    i = 1
    while current_node.get_state().is_terminal() == False :
        if i == 1:
            global constrain_N
            constrain_N += 1*MV_num
            print(constrain_N)
            current_node.get_state().set_available_switch_point()
        else :
            current_node.get_state().set_available_switch_point()
        
        possible_action_num = current_node.get_state().get_available_switch_point()
        print("possible actions to next state",possible_action_num)
        print("simulate Nz level: {}".format(i))
        
        if current_node.get_state().compute_Nz() == Nz-1:
            computation_budget = possible_action_num
        else :
            computation_budget = possible_action_num*const_t//(len(current_node.get_state().get_cumulative_choices())+1)
        
        
        print("this level computation_budget:",computation_budget)

        current_node = monte_carlo_tree_search(current_node,computation_budget=computation_budget)
        print("Choose node: {}".format(current_node))
        const_t = const_t//2

        if i == 1:
            global direct 
            const_t = 10
            cur_state_cumulative_choices = current_node.get_state().get_cumulative_choices()
            cur_best_state = current_node.best_final_state
            if cur_state_cumulative_choices[0] == 1: 
                direct = -direct
                current_node.get_state().get_cumulative_choices().clear()
            elif check_search(cur_best_state,direct) > check_search(cur_best_state,-direct):
                direct = -direct
                current_node.get_state().get_cumulative_choices().clear()

            constrain_N -= 1*MV_num
            print(direct)
            print(current_node.best_final_state)

        print("current Choose node: {}".format(current_node))
        i += 1
        #input()


    return current_node.get_state().get_cumulative_choices()


def check_search(input_vertex,sel_d):
    solver = problem.SingleTank(proble_Nz)
    solver.setStartDirect(sel_d)
    result = solver.solve_result(input_vertex)
    return result

def exhaust_search(input_vertex):
    solver = problem.SingleTank(proble_Nz)
    solver.setStartDirect(direct)
    result = solver.solve_detail(input_vertex,MIN_POINT_DISTANCE*2)
    return result

if __name__ == "__main__":
    op_cmd = str(input("plz input op mode:"))
    print(op_cmd)

    if op_cmd == "mcts":
        round_num = 10
        round_num = int(input("plz input MCTS test round:"))

        result_list = []
        for i in range(round_num):
            timer1 = timer.MyTimer()
            MCTS_result = main()
            if MCTS_result[-1] == 't':
                MCTS_result.pop()
            print(MCTS_result)
            if MCTS_result:
                ex_result = exhaust_search(MCTS_result)
            else :
                ex_result = MCTS_result
            print("suc")
            t = timer1.getTime(kind='real')

            result_list.append({'time':i, 'using_time':t, 'start_direct':direct, 'org_vertex':MCTS_result, 'vertex':ex_result})

        for result in result_list :
            print(result)
        
    elif op_cmd == "data":
        data_Nz = int(input("plz input Nz:"))
        solver = problem.SingleTank(data_Nz)
        print(solver.jobGAMSfile)
        solver.setStartDirect(-1)
        FId = solver.getData([177,538,'t'])
    exit()

    guess_point = 200
    vertexlist = list(np.arange(guess_point+MIN_POINT_DISTANCE,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))

    solver = problem.SingleTank(1)
    solver.setStartDirect(-1)
    i = 0
    FId_sum = 0
    min_Fid = 1
    min_vertex = None
    for vertex in vertexlist :
        FId = solver.solve_result([vertex],[])
        FId_sum += -math.pow(FId,1.5)
        if FId < min_Fid :
            min_Fid = FId
            min_vertex = vertex
        i+=1
    print("total simulate:",i)
    print("avg of FId",FId_sum/i)
    print(f"min_Fid",min_Fid)
    print(f"min_vertex",min_vertex)

    exit()
