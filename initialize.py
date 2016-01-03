import numpy
from sketch_functions import random_matrix_maker


def pM_init(n_meanings):
	return(numpy.random.randint(1,100,size=n_meanings))

# give each agent the same, randomly-populated joint distribution over signals and meanings
def languages(n_signals,n_meanings,n_agents):
	languages = []
	init_matrix = random_matrix_maker(n_signals,n_meanings,pM_init(n_meanings))
	for i in range(0,n_agents):
	    # >>> can insert different initial matrices per agent <<<    
	     languages.insert(i,init_matrix)
	return(languages)



# other stuff to initialize here:
def total_cost(n_agents):
	return([0]*n_agents)
# output of the cost function, per agent in the current round

def successes_per_round(n_rounds):
    return([0]*n_rounds)
    # for starters, total number of successes in the current round
	# summed across all agents

def init_signal_entropy_sums(n_rounds):
	return([0]*(n_rounds+1))

def init_meaning_entropy_sums(n_rounds):
	return([0]*(n_rounds+1))


def init_threshold(n_agents,threshold):
	threshold_array = []
	for i in range(0,n_agents):
		threshold_array.append(threshold)
	return(threshold_array)


def init_threshold_last_round(n_agents):
	threshold_last_round_array = []
	for i in range(0,n_agents):
		threshold_last_round_array.append(0)
	return(threshold_last_round_array)




def init_cost(n_agents):
	return([0]*n_agents)
    
def init_interactions_per_agent(n_agents):
    return([0]*n_agents) 

def init_signal_entropies(n_agents):
	return([0]*n_agents)

def init_meaning_entropies(n_agents):
    return([0]*n_agents)



### PROBABLY DELETE THIS
def initialize_round(n_agents):
	return(init_cost(n_agents),init_interactions_per_agent(n_agents),init_signal_entropies(n_agents),init_meaning_entropies(n_agents))


def init_parrallel(n_agents,n_rounds):

    cost = {}
    #total_cost = {}
    interactions_per_agent = {}
    #meaning_entropies = {}
    #signal_entropies = {}

    for i in range(0,n_rounds):
		cost[i] = init_cost(n_agents)
		interactions_per_agent[i] = init_interactions_per_agent(n_agents)
		#signal_entropies[i] = init_signal_entropies(n_agents)
		#meaning_entropies[i] = init_meaning_entropy_sums(n_agents)

    return(cost,interactions_per_agent)


