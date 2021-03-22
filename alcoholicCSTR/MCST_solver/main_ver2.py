import sys
import os
import psutil
import math
import copy
import random
import numpy as np
import AlcoholicCSTR as problem
import mytimer as timer

proble_Nz = 240
Nz = proble_Nz*2
MIN_POINT_DISTANCE = 1
SIM_TIME = 240
AVAILABLE_CHOICE_NUMBER = 0
GAMMA = 1.0
try_limit = 10
FId_Precision = None
change_temp = False

Sa_d = -1
T_d = -1

#memory control
def show_memory_info(hint):
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss/1024/1024
    print("{} memory used:{}".format(hint,memory))
    if memory >= 100 :
        import gc
        gc.collect()
        show_memory_info("after gc collect")
        input()

class State(object):
    def __init__(self):
        self.current_value = 0.0
        # For the first root node, the index is 0 and the game should start from 1
        self.current_round_index = 0
        self.cumulative_choices = [{'var':'Sa','choices':[]},{'var':'T','choices':[]}]
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

        t_num = 0
        for choices in self.cumulative_choices :
            if 't' in choices['choices'] :
                t_num += 1
        if t_num == 2 :
            is_finish = True

        switch_times = 0
        for choices in self.cumulative_choices :
            if 't' in choices['choices'] :
                switch_times += len(choices['choices']) - 1
            else:
                switch_times += len(choices['choices'])
        if switch_times >= Nz :
            is_finish = True

        if self.get_available_switch_point() == 1:
            is_finish = True
        elif self.get_available_switch_point() == 2:
            if self.available_switch_point[0]['point'] == 't' and self.available_switch_point[1]['point'] == 't' :
                is_finish = True
        
        return is_finish

    def compute_reward(self):
        Sa_choices = None
        T_choices = None
        for choices in self.cumulative_choices :
            if choices['var'] == 'Sa' :
                Sa_choices = choices['choices']
            elif choices['var'] == 'T' :
                T_choices = choices['choices']
        
        solver = problem.AlcoholicCSTR(proble_Nz)
        if change_temp :
            solver.set_jobGAMSfile("alcoholicCSTRNz"+str(proble_Nz)+"_temp.gms")
        solver.setStartDirect(Sa_d,T_d)
        FId = solver.solve_result(Sa_choices,T_choices)
        del(solver)

        if FId_Precision != None:
            return -round(math.pow(FId,2),FId_Precision)
        else:
            return -math.pow(FId,2)

    def set_available_switch_point(self):
        Sa_point = None
        T_point = None
        Sa_item = next((item for item in self.cumulative_choices if item['var'] == 'Sa'), None)
        Sa_choices = Sa_item['choices']
        T_item = next((item for item in self.cumulative_choices if item['var'] == 'T'), None)
        T_choices = T_item['choices']

        Sa_finish = False
        T_finish = False
        # deal with Sa
        if len(Sa_choices) == 0 :
            Sa_point = MIN_POINT_DISTANCE
        else:
            if Sa_choices[-1] != 't' :
                Sa_point = Sa_choices[-1]+MIN_POINT_DISTANCE
            else:
                Sa_finish = True
        # deal with T
        if len(T_choices) == 0 :
            T_point = MIN_POINT_DISTANCE
        else:
            if T_choices[-1] != 't' :
                T_point = T_choices[-1]+MIN_POINT_DISTANCE
            else:
                T_finish = True

        # decide orig_point prevent loop in tree
        if Sa_finish == True or T_finish == True :
            orig_point = SIM_TIME+1
        else:
            orig_point = max(Sa_point,T_point)
        
        if Sa_finish == False:
            if orig_point >= SIM_TIME+1  :
                Sa_available_switch_point = ['t']
            else:
                Sa_available_switch_point = list(np.arange(orig_point,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))
                Sa_available_switch_point.insert(0,'t')        
        
        if T_finish == False:
            if orig_point >= SIM_TIME+1 :
                T_available_switch_point = ['t']
            else:
                T_available_switch_point = list(np.arange(orig_point,SIM_TIME+1,MIN_POINT_DISTANCE,dtype=np.int))
                T_available_switch_point.insert(0,'t')

        total_switch_num = 0
        for p in Sa_choices :
            if p != 't':
                total_switch_num += 1
        for p in T_choices :
            if p != 't':
                total_switch_num += 1
        if total_switch_num >= Nz :
            Sa_finish = True
            T_finish = True
        
        if Sa_finish == True :
            Sa_available_switch_point = []
        if T_finish == True :
            T_available_switch_point = []

        available_switch_point = []
        available_switch_point.extend([{'var':'Sa','point':t} for t in Sa_available_switch_point])
        available_switch_point.extend([{'var':'T','point':t} for t in T_available_switch_point])
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
        var = random_choice['var']
        current_cumulative_choices = copy.deepcopy(self.cumulative_choices)
        spec_item = next((item for item in current_cumulative_choices if item['var'] == var), None)
        spec_item['choices'] = spec_item['choices'] + [random_choice['point']]
        next_state.set_cumulative_choices(current_cumulative_choices)

        return next_state

    def get_next_state_with_spec_choice(self,choice):
        print("spec choice", choice)
        next_state = State()
        next_state.set_current_value(choice)
        next_state.set_current_round_index(self.current_round_index + 1)
        var = choice['var']
        current_cumulative_choices = copy.deepcopy(self.cumulative_choices)
        spec_item = next((item for item in current_cumulative_choices if item['var'] == var), None)
        spec_item['choices'] = spec_item['choices'] + [choice['point']]
        next_state.set_cumulative_choices(current_cumulative_choices)

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
        
        self.best_reward = -10
        self.best_action_round = 1

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
        return "Node: {}, Q/N: {}/{}, ratio: {},state: {}".format(
            hash(self), self.quality_value, self.visit_times, ratio_value, self.state)


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
        current_state.get_next_state_with_spec_choice({'var':'Sa','point':'t'})
    #elif node.get_visit_times() == 1:
    #    current_state.get_next_state_with_spec_choice({'var':'T','point':'t'})
    else:    
        # Run until the game over
        while current_state.is_terminal() == False:
            # Pick one random action to play and get next state
            current_state = current_state.get_next_state_with_random_choice()
            #print("default_policy current state:",current_state)
    """
    while current_state.is_terminal() == False:
        # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice()
        #print("default_policy current state:",current_state)
    """

    final_state_reward = current_state.compute_reward()
    if round(final_state_reward,6) >= node.best_reward :
        node.best_reward = final_state_reward
        node.best_action_round = current_state.get_current_round_index()
    return final_state_reward

def improve_policy(node,t):
    """
    simulation step: using unform random method to expand node until the state terminal.
    but need to preform better reward than current best reward.
    """
    # if this node already approach to best state
    if t >= try_limit:
        return node.best_reward

    # Get the state of the game
    current_state = node.get_state()
    # First consider directly terminal state
    if node.get_visit_times() == 0:
        current_state.get_next_state_with_spec_choice({'var':'Sa','point':'t'})
    #elif node.get_visit_times() == 1:
    #    current_state.get_next_state_with_spec_choice({'var':'T','point':'t'})
    else:    
        # Run until the game over
        while current_state.is_terminal() == False:
            # Pick one random action to play and get next state
            current_state = current_state.get_next_state_with_random_choice()
            #print("default_policy current state:",current_state)
    """
    while current_state.is_terminal() == False:
        # Pick one random action to play and get next state
        current_state = current_state.get_next_state_with_random_choice()
        #print("default_policy current state:",current_state)
    """

    final_state_reward = current_state.compute_reward()
    if round(final_state_reward,6) >= node.best_reward :
        node.best_reward = final_state_reward
        node.best_action_round = current_state.get_current_round_index()
    else :
        return improve_policy(node,t+1)
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
        score = left + C * math.sqrt(right)

        if score > best_score:
            best_sub_node = sub_node
            best_score = score
    
    return best_sub_node

def best_child_optimal(node,gamma):
    # TODO: Use the min float value
    best_score = -sys.maxsize
    best_sub_node = None

    # Travel all sub nodes to find the best one
    for sub_node in node.get_children():

        left = (1-gamma)*sub_node.get_quality_value() / sub_node.get_visit_times()
        right = gamma*(sub_node.best_reward)
        """if sub_node.best_action_round > 1 :
            print(f"sub_node.best_action_round :{sub_node.best_action_round}, Nz :{Nz}")
            print(sub_node.best_reward,sub_node.best_reward*math.sqrt(sub_node.best_action_round/Nz))
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

    show_period = 1000
    period_num = 1
    print("computation budget:",computation_budget)
    show_memory_info("mcts initial")
    # Run as much as possible under the computation budget
    for i in range(computation_budget):
        print("compute times:",i)

        # 1. Find the best node to expand
        expand_node = tree_policy(node)
        print("selected sub node:",expand_node)
        # 2. Random run to add node and get reward
        reward = default_policy(expand_node)
        # reward = improve_policy(expand_node,0)

        if reward >= min_FId :
            min_state = copy.deepcopy(expand_node.get_state().get_cumulative_choices())
            min_FId = reward
        print(f"now min FId: {math.sqrt(-min_FId)}, min state: {min_state}")

        # 3. Update all passing nodes with reward
        backup(expand_node, reward)
        
        show_period -= 1
        if show_period == 0 :
            #show_current_sub_node_state(node,period_num)
            show_memory_info("mcts loop"+str(period_num))
            show_period = 1000
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
    #init_state.set_cumulative_choices([{'var':'Sa','choices':[176]},{'var':'T','choices':[]}])
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
        # consider depth i
        # computation_budget = int(possible_action_num*const_t//i)
        computation_budget = int(possible_action_num*const_t)
        print("this level computation_budget:",computation_budget)
        current_node = monte_carlo_tree_search(current_node,computation_budget=computation_budget)
        print("Choose node: {}".format(current_node))
        i += 1
        #input()


    return current_node.get_state().get_cumulative_choices()

def exhaust_search(vertex_Sa,vertex_T):
    if 't' in vertex_Sa :
        vertex_Sa.pop()
    if 't' in vertex_T :
        vertex_T.pop()
    solver = problem.AlcoholicCSTR(proble_Nz)
    if change_temp :
        solver.set_jobGAMSfile("alcoholicCSTRNz"+str(proble_Nz)+"_temp.gms")
    solver.setStartDirect(Sa_d,T_d)
    print("exhaust search init vertex\n",vertex_Sa,vertex_T)
    result = solver.solve_detail(vertex_Sa,vertex_T,20)
    return result

def output_EX_search(vertex_Sa,vertex_T):
    Sa_start_p = 225
    Sa_end_p = 232
    T_start_p = 225
    T_end_p = 232
    Sa_list = np.arange(Sa_start_p,Sa_end_p,dtype=np.int)
    T_list = np.arange(T_start_p,T_end_p,dtype=np.int)
    print(Sa_list)
    print(T_list)

    solver = problem.AlcoholicCSTR(proble_Nz)
    if change_temp :
        solver.set_jobGAMSfile("alcoholicCSTRNz"+str(proble_Nz)+"_temp.gms")
    solver.setStartDirect(Sa_d,T_d)
    x = []
    y = []
    f = []
    minFId = 10
    min_i = -1

    Sa = []
    T = []
    v_i = 0
    for Sa_p in Sa_list:
        for T_p in T_list :
            Sa.append(Sa_p)
            Sa.extend(vertex_Sa)
            T.append(T_p)
            T.extend(vertex_T)
            
            FId = solver.solve_result(Sa,T)
            x.append(Sa[0])
            y.append(T[0])
            f.append(1/FId)
            
            if FId < minFId :
                minFId = FId
                min_i = v_i
            v_i += 1
            Sa.clear()
            T.clear()
            print(x[-1],y[-1],f[-1])

    print("search finished")
    print(minFId,min_i)
    import matplotlib.pyplot as plt
    import csv
    with open('EXresultNz'+str(proble_Nz)+'.csv','w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(x)) :
            writer.writerow([x[i],y[i],f[i]])

    plt.scatter(x, y, marker='.',c=f)
    plt.title("ex full region plot")
    plt.gray()
    plt.show()

if __name__ == "__main__":
    #Nz2 174, step_d=1, const_t=2, [(176,189),(214,)] 0.5934720839707792
    #Nz3 [(202,),()] [(202,238)]
    #Nz4 225 [(215,239),(,)]
    #Nz5 [(225,238),(,)]
    #Nz6  [{'var': 'Sa', 'choices': [227, 232, 237, 238]}, {'var': 'T', 'choices': [234]}]
    #Nz8 const_t=1 [{'var': 'Sa', 'choices': [238]}, {'var': 'T', 'choices': []}]
    #Nz10 const_t=1 [{'var': 'Sa', 'choices': [238]}, {'var': 'T', 'choices': []}]
    #Nz20 const_t=0.5 [{'var': 'Sa', 'choices': [238]}, {'var': 'T', 'choices': []}]
    
    #output_EX_search([],[])

    op_cmd = sys.argv[1]
    print(op_cmd)
    
    if op_cmd == "test":
        solver = problem.AlcoholicCSTR(proble_Nz)
        solver.setStartDirect(Sa_d,T_d)
        FId = solver.solve_result([238,'t'],['t'])
    elif op_cmd == "data":
        solver = problem.AlcoholicCSTR(proble_Nz)
        solver.setStartDirect(Sa_d,T_d)
        FId = solver.get_data([238,'t'],['t'],save=True)
    elif op_cmd == "ex":
        ex_result = exhaust_search([237,240,'t'],['t'])
        solver = problem.AlcoholicCSTR(proble_Nz)
        if change_temp :
            solver.set_jobGAMSfile("alcoholicCSTRNz"+str(proble_Nz)+"_temp.gms")
        solver.setStartDirect(Sa_d,T_d)
        solver.get_data(ex_result[0],ex_result[1])
    elif op_cmd == "mcts":
        timer1 = timer.MyTimer()
        MCTS_result = main()
        print("suc")
        print(MCTS_result)

        for choices in MCTS_result :
            if choices['var'] == 'Sa' :
                Sa_choices = choices['choices']
            elif choices['var'] == 'T' :
                T_choices = choices['choices']
            
        solver = problem.AlcoholicCSTR(proble_Nz)
        if change_temp :
            solver.set_jobGAMSfile("alcoholicCSTRNz"+str(proble_Nz)+"_temp.gms")
        solver.setStartDirect(Sa_d,T_d)
        FId = solver.solve_result(Sa_choices,T_choices)
        ex_result = exhaust_search(Sa_choices,T_choices)
        print("===mcts result===")
        print(MCTS_result,FId)
        print("===final result===")
        print(ex_result)
        solver.get_data(ex_result[0],ex_result[1],False)
        t = timer1.getTime(kind='real')
    exit()