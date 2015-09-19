
import setup
import numpy
from sketch_functions import random_matrix_maker

n_agents = setup.n_agents
# number of agents in the population
# n_agents also equals the number of languages (joint distributions over signals and meanings) in the population.

# set language size
n_meanings = setup.n_meanings
n_signals = setup.n_signals

n_rounds = setup.n_rounds
# each round is composed of n interactions between a pair of agents,
# who are randomly drawn from the population

#n_interactions = setup.n_interactions
# number of random interactions that need to occur before agents decide whether 
# or not to keep their proposal distributions

#threshold = setup.threshold
# proportion successful interactions an agent needs to have to keep their proposal distribution

# initialize the prior distribution over meanings
# for starters, just randomly populate pM (no need to normalize yet)


def pM_init():
	return(numpy.random.randint(1,100,size=n_meanings))

# give each agent the same, randomly-populated joint distribution over signals and meanings
def languages():
	languages = []
	init_matrix = random_matrix_maker(n_signals,n_meanings,pM_init())
	for i in range(0,n_agents):
	    # >>> can insert different initial matrices per agent <<<    
	     languages.insert(i,init_matrix)
	return(languages)

def total_cost():
	return([0]*n_agents)

# other stuff to initialize here:
def total_cost():
	return([0]*n_agents)
# output of the cost function, per agent in the current round

def successes_per_round():
    return([0]*n_rounds)
    # for starters, total number of successes in the current round
	# summed across all agents

def signal_entropy_sums():
	return([0]*(n_rounds+1))

def meaning_entropy_sums():
	return([0]*(n_rounds+1))
