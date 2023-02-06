import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import sys
import re
import pickle

# Wednesday May 22, 2019
# Animation of a state swap process
# ECE 105: Laboratory / Homework Week 8

# Dependencies: pickle, networkx

# function initialize state
# arguments: 
# G: the graph
# p: the probability that the initial state for each vertex is 0 
# (hence the initial state of a vertex is 1 with probability 1-p)
# returns: the initial state 
# (a dictionary with each vertex label as a key, and the state as value
def init_state(G, p, rand_seed = 105):
    # set random seed to 105
    random.seed(rand_seed)
    # state is a dictionary that assigns a value of 0 or 1 to each vertex
    state = {}
    for v in G.nodes(): 
        # the initial state for vertex v is randomly chosen to be 0 or 1
        state[v] = 0 if random.random() < p else 1
    return state

# function find unsatisfied vertices
# arguments:
# G: the graph
# state: the current state (a dictionary)
# threshold: vertex is unsatisfied if number of different neighbors >= threshold
# returns: the list named unsat with two sublists:
# unsat[0]: unsatisfied vertices with state value 0
# unsat[1]: unsatisfied vertices with state value 1
def find_unsatisfied_vertices(G, state, threshold):
    # initialize the list of unsatisfied vertices to be two empty "sub"-lists
    unsat = [[],[]]
    # iterate over the vertices in the graph:
    for v in G.nodes():
        # different is a list that holds all neighbors with state different from v
        different = [u for u in G.neighbors(v) if state[v] != state[u]]
        # v is unsatisfied if the number of different neighbors is >= threshold
        # if yes, then add v to the sublist of unsat corresponding to v's state
        if len(different) >= threshold: unsat[state[v]].append(v)        
    return unsat

# function dict_to_array
# arguments: 
# dict: a dictionary
# returns: 
# array
# this is a utility function to convert the state from a dictionary to an array
# the assumption is that the keys of the dictionary are positions in the array
# so, pos is a key, and pos is a tuple (x,y)
# the value dict[pos] is thus placed in the array at position [pos[0], pos[1]]
def dict_to_array(n, dict):
    array = np.zeros((n,n))
    for pos in dict: array[pos[0],pos[1]] = dict[pos]
    return array

# function state_evolution
# arguments:
# G: a graph
# state: the state dictionary
# G: the graph
# state: the current state (a dictionary)
# threshold: vertex is unsatisfied if number of different neighbors >= threshold
# Tmax: the maximum number of iterations 
def state_evolution(G, state, threshold, Tmax, rand_seed = 105):
    '''
    G: a graph (a networkx graph object)
    state: the state dictionary (dict)
    threshold: vertex is unsatisfied if number of different neighbors >= threshold (int)
    Tmax: the maximum number of iterations (int)
    rand_seed: random seed to make the result reproducible (int)
    '''
    # set random seed
    random.seed(rand_seed)
    # initialize the time index t to be zero
    t = 0
    # find the unsatisfied vertices
    unsat = find_unsatisfied_vertices(G, state, threshold)
    # finding a pair of unsatisfied vertices to swap requires 
    # there to be both an unsatisfied vertex with state 0 and one with state 1
    unsatisfied_vertex_pair_exists = len(unsat[0]) > 0 and len(unsat[1]) > 0
    # keep track of the pairs of vertices that are swapped, initially empty
    swapped_vertices = []
    
    # stopping criterion is if there are no more unsatisfied vertex pairs, or t >= Tmax
    while unsatisfied_vertex_pair_exists and t < Tmax:
        # pick a random unsatisfied vertex with state 0 
        # ====== YOUR CODE HERE ====== #
        u = random.choice(unsat[0])
        # pick a random unsatisfied vertex with state 1
        # ====== YOUR CODE HERE ====== #
        v = random.choice(unsat[1])
        # record these vertices as the ones to be swapped
        # ====== YOUR CODE HERE ====== #
        swapped_vertices.append([u,v])
        
        # swap the state of these vertices
        # ====== YOUR CODE HERE ====== #
        swap = state[u]
        state[u] = state[v]
        state[v] = swap
    
        # update the list of unsatisfied vertices using function "find_unsatisfied_vertices"
        # ====== YOUR CODE HERE ====== #
        unsat = find_unsatisfied_vertices(G, state, threshold)
        # update the indicator of whether or not a pair of unsatisfied vertices exists 
        # (update variable "unsatisfied_vertex_pair_exists")
        # ====== YOUR CODE HERE ====== #
        unsatisfied_vertex_pair_exists = True if len(unsat[0]) > 0 and len(unsat[1]) > 0 else False
        # increment the time index t
        t += 1
    # return the list of swapped vertices -- this is used in the animation
    return swapped_vertices

def run_experiment(n, rand_seed = 105):
    # function init
    # this is used by the FuncAnimation to initialize the figure
    def init(): 
        plt.gca().set_aspect('equal')
        plt.axis('off')
        plt.title('0/{}'.format(size))
        return [im]

    # function update
    # arguments:
    # i: the frame index
    def update(i): 
        # get the image array
        a=im.get_array()
        # get the pair of swapped vertices in frame i
        u,v = swapped_vertices[i]
        # update the image array
        a[u[0],u[1]] = 1 
        a[v[0],v[1]] = 0 
        # set the image array
        im.set_array(a)
        # update the title to show the frame index
        plt.title('{}/{}'.format(i+1,size))
        # return the image
        return [im]
    # parameters for a 2d grid graph
    # n: the side length
    n = 20
    # create an n x n 2d grid graph
    G=nx.grid_2d_graph(n,n)
    # set the positions of the vertices
    pos = dict((n, n) for n in G.nodes())

    # parameters for dynamics 
    p = 1/2 # probability used to determine random initial state
    threshold = 3 # unsatisfied if number of different neighbors >= threshold
    Tmax = 1000 # maximum number of frames

    # initialize variables
    # initialize the state 
    initState = init_state(G, p, rand_seed)
    # convert the state from a dictionary to an array to print the image
    initArray = dict_to_array(n, initState)
    # call state_evolution, and obtain the list of swapped vertices in each instant
    swapped_vertices = state_evolution(G, initState, threshold, Tmax, rand_seed)
    # size is the actual number of frames (guaranteed to be <= Tmax)
    size = len(swapped_vertices)

    # create the figure animation
    fig = plt.figure()
    # this is a custom color map with the RGB colors of red and blue
    cmap_red_blue = LinearSegmentedColormap.from_list('my_cmap', [(1, 0, 0), (0, 0, 1)] , N=2)
    # draw the image using plt.imshow, with the initArray as the initial state
    im = plt.imshow(initArray, cmap=cmap_red_blue)
    # animate the image using the update function
    ani = FuncAnimation(fig, update, frames=range(size), init_func=init, interval=1, blit=True, repeat=False)
    # show the animation
    plt.show()
    return swapped_vertices

def run_test(test_case_index, student_result):
    try:
        with open ('test_case.pkl', 'rb') as fp:
            GT = pickle.load(fp)
    except:
        print("""
        !!!! Please download "test_case.pkl" file from BBLEARN
        and put "test_case.pkl" in the same folder as this python script.
        """)
        return False
        
    true = GT[test_case_index]
    if len(true) != len(student_result):
        return False
    for i in range(len(true)):
        if true[i][0] != student_result[i][0] or true[i][1] != student_result[i][1]:
            return False
    return True      

def main():
    try:
        student_id = sys.argv[0].split('/')[-1].split('.')[0]
        if not re.match('([a-z]+\d+)*_8', student_id):
            print("PLEASE CHANGE YOUR FILE NAME!")
            student_id = 'Anonymous'
    except:
        student_id = 'Anonymous'
    
    c = 0
    
    test_case_1 = run_experiment(5, 105)
    if run_test(0, test_case_1):
        c += 5
    test_case_2 = run_experiment(10, 8)
    if run_test(1, test_case_2):
        c += 5
    test_case_3 = run_experiment(30, 23)
    if run_test(2, test_case_3):
        c += 10
    
    print('======== Summary ========')
    print('Student_ID: ', student_id, '\nTotal Grade: ', str(c) + '/20')
    
if __name__ == "__main__":
    main()