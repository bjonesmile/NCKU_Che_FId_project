import sys
import math
import copy
import random
import numpy as np
import DoubleTank as problem
import mytimer as timer

proble_Nz = 1
Nz = proble_Nz*1
constrain_N = proble_Nz
MIN_POINT_DISTANCE = 10
SIM_TIME = 800
AVAILABLE_CHOICE_NUMBER = 0
GAMMA = 0.9

direct = -1

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

    def compute_reward(self):
        
        solver = problem.DoubleTank(proble_Nz)
        solver.setStartDirect(direct)
        FId = solver.solve_result(self.cumulative_choices)
        
        return -math.pow(FId,2)

    def set_available_switch_point(self):
        if len(self.cumulative_choices) == 0 :
            last_point = MIN_POINT_DISTANCE
        else:
            last_point = self.cumulative_choices[-1]+MIN_POINT_DISTANCE
        
        if last_point >= SIM_TIME+1 :
            available_switch_point = ['t']
        else:
            available_switch_point = list(np.arange(last_point,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))
            available_switch_point.insert(0,'t')

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
    Node of MCTS's tree structure, incluinf of parent and children, and function used to calculate quality(UCB)，and current state of simulation.
    """

    def __init__(self):
        self.parent = None
        self.children = []

        self.visit_times = 0
        self.quality_value = 0.0
        self.best_reward = -1
        self.best_action_round = None

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
        score = left + C * math.sqrt(right)# + sub_node.best_reward

        """if is_exploration == False :
            score = sub_node.best_reward
            print("sub-node:",sub_node)
            print("left",left)
            print("rught",right)
            print("score",score)"""

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

        left = (1-gamma)*sub_node.get_quality_value() / sub_node.get_visit_times()
        if sub_node.best_action_round > 1 :
            right = gamma*(sub_node.best_reward+sub_node.best_reward*math.sqrt(sub_node.best_action_round/Nz))
        else:
            right = gamma*(sub_node.best_reward+sub_node.best_reward)
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

    # Update util the root node
    while node != None:
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
        print(f"now min FId: {math.sqrt(-min_FId)}, min state: {min_state}")

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)
        
        show_period -= 1
        if show_period == 0 :
            show_current_sub_node_state(node,period_num)
            show_period = 100
            period_num += 1
    # N. Get the best next node
    best_next_node = best_child_optimal(node,GAMMA)
    #best_next_node = best_child(node, False)

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
    const_t = int(2)
    # Create the initialized state and initialized node
    init_state = State()
    init_node = Node()
    init_node.set_state(init_state)
    current_node = init_node

    # Set the rounds to play
    i = 1
    while current_node.get_state().is_terminal() == False :
        current_node.get_state().set_available_switch_point()
        possible_action_num = current_node.get_state().get_available_switch_point()
        print("possible actions to next state",possible_action_num)
        print("simulate Nz level: {}".format(i))
        computation_budget = possible_action_num*const_t
        print("this level computation_budget:",computation_budget)
        current_node = monte_carlo_tree_search(current_node,computation_budget=computation_budget)
        print("Choose node: {}".format(current_node))
        #input()


    return current_node.get_state().get_cumulative_choices()


if __name__ == "__main__":

    result_list = []
    for i in range(10):
        timer1 = timer.MyTimer()
        MCTS_result = main()
        print("suc")
        t = timer1.getTime(kind='real')

        """solver = problem.DoubleTank(proble_Nz)
        solver.setStartDirect(direct)
        FId = solver.getData(MCTS_result)"""

        result_list.append({'time':i, 'using_time':t, 'vertex':MCTS_result})

    for result in result_list :
        print(result)
    exit()
    
    solver = problem.DoubleTank(2)
    print(solver.jobGAMSfile)
    solver.setStartDirect(direct)
    FId = solver.getData([])
    exit()

    guess_point = 200
    vertexlist = list(np.arange(guess_point+MIN_POINT_DISTANCE,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))

    solver = problem.DoubleTank(1)
    solver.setStartDirect(-1)
    i = 0
    FId_sum = 0
    min_Fid = 1
    min_vertex = None
    for vertex in vertexlist :
        FId = solver.solve_result([vertex])
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
