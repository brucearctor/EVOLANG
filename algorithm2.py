# we have a null model!  ...that always converges to near-uniform matrices,
# so we need constraints to get effective communication systems.

import numpy
import scipy, scipy.stats
import os
#os.chdir('/Users/vanferdi/Dropbox/Research/Collaborations/Tanmoy_&_David')
#import sketch_functions

################################################################################
# functions (delete these later and figure out how to import from "sketch_functions.py")
# don't read about these functions now - come back to them as they're relevant.
# start reading at line 76.

def random_matrix_maker(n_signals,n_meanings,pM_init):
    # randomly populate a matrix of meaning-signal correspondences
    # each row is a signal
    # each column is a meaning
    matrx = numpy.random.randint(1,100,size=(n_signals, n_meanings))
    matrx = matrx.astype(numpy.float64)
    
    # raise each entry to some power to make it peakier
    matrx = matrx**2
    
    # normalize each column so it sums to one
    matrx /=  matrx.sum(axis=0)[numpy.newaxis,:]
    
    # multiply each x in column y by pM_init[y]
    matrx *= pM_init  # row version: pM_init *= transpose(matrix)
    
    # normalize the matrix (so all entries sum to one)
    #print("type: "+str(type(matrx))+" "+str((numpy.sum)))
    final_matrix = matrx/numpy.sum(matrx)
    
    return final_matrix
    
def get_pM(matrix):
    # return the distribution over meanings (pM)
    # sum of columns: matrix.sum(axis=0)
    # will be the normalized version of pM_init
    pM = matrix.sum(axis=0)/numpy.sum(matrix)
    return pM

def get_pS(matrix):
    # return the distribution over signals (pS)
    # sum of rows: matrix.sum(axis=1)
    pS = matrix.sum(axis=1)/numpy.sum(matrix) 
    return pS
    
def proposal_matrix_maker(n_signals,n_meanings,old_matrix):
    # how an agent chooses a particular deviation from their current language
    # this deviation will be referred to as a "proposal distribution"
    # for starters, they change it with a uniform random delta function
    # 1) so nothing becomes negative and 2) so all entries still sum to one
    delta_max = (1.0/(n_signals*n_meanings))/10
    delta_matrix = numpy.random.uniform(0,delta_max,size=(n_signals, n_meanings))
    new_matrix = old_matrix+delta_matrix
    new_matrix /= numpy.sum(new_matrix)
    return new_matrix

def max_ent_sum(n_signals,n_meanings):
    # I'll be using a un-averaged sum of signal entropies (and meaning entropies) metric 
    # as a window into how this system is changing over time. 
    # This function calculates the maximum value that this particular metric can have.
    # When the joint probabilities are in a perfectly uniform distribution, then this metric is at its max value.
    signals_uniform = [1.0/(n_signals*n_meanings)]*n_signals
    meanings_uniform = [1.0/(n_signals*n_meanings)]*n_meanings
    signals_maxentsum = scipy.stats.entropy(signals_uniform,base=2)*n_meanings
    meanings_maxentsum = scipy.stats.entropy(meanings_uniform,base=2)*n_signals
    return signals_maxentsum, meanings_maxentsum
    

################################################################################
# initialize once:

n_agents = 5
# number of agents in the population
# n_agents also equals the number of languages (joint distributions over signals and meanings) in the population.

# set language size
n_meanings = 40
n_signals = 5

n_rounds = 1000
# each round is composed of n interactions between a pair of agents,
# who are randomly drawn from the population

n_interactions = 10 
# number of random interactions that need to occur before agents decide whether 
# or not to keep their proposal distributions

threshold = 0.5
# proportion successful interactions an agent needs to have to keep their proposal distribution

# initialize the prior distribution over meanings
# for starters, just randomly populate pM (no need to normalize yet)
pM_init = numpy.random.randint(1,100,size=n_meanings)

# give each agent the same, randomly-populated joint distribution over signals and meanings
languages = []
init_matrix = random_matrix_maker(n_signals,n_meanings,pM_init)
for i in range(0,n_agents):
    # >>> can insert different initial matrices per agent <<<    
     languages.insert(i,init_matrix)

# other stuff to initialize here:
total_cost = [0]*n_agents # output of the cost function, per agent in the current round

successes_per_round = [0]*n_rounds # for starters, total number of successes in the current round
# summed across all agents

# some preliminary things to track for visualizing what this system does:
# all this is explained further below.
signal_entropy_sums = [0]*(n_rounds+1)
meaning_entropy_sums = [0]*(n_rounds+1)

signal_entropies = [0]*n_agents
for a in range(0,n_agents):
    signal_entropies[a] = numpy.sum(scipy.stats.entropy(languages[a],base=2))  
    signal_entropy_sums[0] = numpy.sum(signal_entropies)

meaning_entropies = [0]*n_agents    
for a in range(0,n_agents):
    meaning_entropies[a] = numpy.sum(scipy.stats.entropy(numpy.matrix.transpose(languages[a]),base=2))  
    meaning_entropy_sums[0] = numpy.sum(meaning_entropies)
    

################################################################################
# MAIN LOOP

for r in range(0,n_rounds):
    
    print("round: " +str(r))
    
    ############################################################################
    # stuff to initialize at start of each round of interactions:

    cost = [0]*n_agents
    interactions_per_agent = [0]*n_agents
    signal_entropies = [0]*n_agents
    meaning_entropies = [0]*n_agents

    # each agent makes their own proposal distribution
    # see comment on function proposal_matrix_maker() above.
    proposals = []
    for i in range(0,n_agents):
        proposals.insert(i,proposal_matrix_maker(n_signals,n_meanings,languages[i]))
        
    ############################################################################
    
    for k in range(0,n_interactions):

        # choose two agents at random to speak with one another
        # one will be the sender and the other will be the receiver.
        pair = numpy.random.choice(n_agents,2,replace=False)
        sender = pair[0]
        receiver = pair[1]
        
        # sender chooses a signal-meaning pair from their proposal distribution.
        # for starters, it's chosen randomly, weighted by the joint probability over all signal-meanings pairs
        # (couldn't figure out how to do a random sample from a 2D array, so did this in two steps)
        # 1) choose meaning first:
        weights = get_pM(proposals[sender])
        meaning_intended = numpy.random.choice(range(0,n_meanings),p=weights)
        # 2) then choose a signal for this meaning:
        prelim_weights = proposals[sender][:,meaning_intended]
        weights = prelim_weights/numpy.sum(prelim_weights)
        signal_produced = numpy.random.choice(range(0,n_signals),p=weights)
        # >>> option: there could be noise so that the signal received isn't necessarily the signal produced.
        
        # receiver infers a meaning for that signal
        # by randomly selecting a meaning from their proposal distribution, 
        # according to their meaning weights for the signal they received.
        signal_received = signal_produced
        prelim_weights = proposals[receiver][signal_received]
        weights = prelim_weights/numpy.sum(prelim_weights)
        meaning_inferred = numpy.random.choice(range(0,n_meanings),p=weights)
             
        # update success rating
        # for starters, the cost function is just tally of successful interactions,
        # but it'll probably be some negative cost later
        interactions_per_agent[sender] += 1
        interactions_per_agent[receiver] += 1
        
        if meaning_intended == meaning_inferred:
            cost[sender] += 1
            cost[receiver] += 1
            total_cost[sender] += 1
            total_cost[receiver] += 1
         
            
                  
        # end of interactions loop
     
        
              
    # use success rating to determine what agents do with their proposal distributions
    # for starters, if >= x% of an agents interactions were successful, they keep the proposal distribution,
    # and if < x% were successful, they don't adopt the proposal distribution (they revert back to their previous language instead).
    decision_to_keep = [0]*n_agents # true = keep proposal, false = revert
    for i in range(0,n_agents):
        if cost[i] > 0: # to prevent divisions by zero.
            if cost[i]/float(interactions_per_agent[i]) >= threshold:
                decision_to_keep[i] = "true"
            else:
                decision_to_keep[i] = "false"
        else:
            decision_to_keep[i] = "false"
                        
    # update agents' languages
    for i in range(0,n_agents):
        if decision_to_keep[i] == "true":
            languages[i] = proposals[i]
    

    ############################################################################
    # analyses per round
    
    # the raw tally of successes by round, summed over all agents.
    # the max number of successes per round can be as high as n_interactions*n_agents.
    successes_per_round[r] = numpy.sum(cost)
    
    # now here's the weird thermometer I've made to track changes to the languages:

    # raw sum of signal entropies across all languages
    for a in range(0,n_agents):
        # get entropy of all signals per meaning: scipy.stats.entropy(languages[meaning],base=2)
        # then sum them so there's one value per language
        signal_entropies[a] = numpy.sum(scipy.stats.entropy(languages[a],base=2)) 
    # then sum the values for all of the languages in use at that particular round
    signal_entropy_sums[r+1] = numpy.sum(signal_entropies)
    
    # raw sum of meaning entropies across all languages
    for a in range(0,n_agents):
        # get entropy of meanings per signal: scipy.stats.entropy(numpy.matrix.transpose(languages[signal]),base=2)
        # then sum them so there's one value per language
        meaning_entropies[a] = numpy.sum(scipy.stats.entropy(numpy.matrix.transpose(languages[a]),base=2))  
    # then sum the values for all of the languages in use at that particular round
    meaning_entropy_sums[r+1] = numpy.sum(meaning_entropies)
    
    # also, see the max_ent_sum() function above.  It computes the ceiling for this raw sum for any parameter combo.
    
    ############################################################################
        
    # end of rounds loop

# end of simulation

################################################################################
# final analyses

print("signal_entropy_sums: "+str(signal_entropy_sums))
print("meaning_entropy_sums: "+str(meaning_entropy_sums))
print("successes per round: "+str(successes_per_round))

################################################################################


# plot stuff
import matplotlib.pyplot as plt

plt.plot(successes_per_round, 'grey', linewidth=2.0)
plt.plot(signal_entropy_sums, 'black', linewidth=2.0)
plt.plot(meaning_entropy_sums, 'blue')
#plt.plot([n_interactions*n_agents]*n_rounds, 'grey', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[0]*n_agents]*n_rounds, 'black', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[1]*n_agents]*n_rounds, 'blue', linestyle="--", linewidth=1)
plt.show()
