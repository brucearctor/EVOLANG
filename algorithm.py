# changes from last version:
# p(M) is fixed now: agents do not propose changes to the meaning space

# to do next:
# agents compare the proposal language to their last language and only accept it if it performs better

import setup
import initialize
from initialize import *
#from initialize import successes_per_round
from propose import propose
from sketch_functions import *
import numpy
import scipy, scipy.stats

n_rounds = setup.n_rounds
n_agents = setup.n_agents
n_signals = setup.n_signals
n_meanings = setup.n_meanings
n_interactions = setup.n_interactions
threshold = setup.threshold

## THIS COULD BE A SINGLE LINE, but I think this is clearer
successes_per_round = successes_per_round(n_rounds)
total_cost = total_cost(n_agents)
signal_entropy_sums = init_signal_entropy_sums(n_rounds)
meaning_entropy_sums = init_meaning_entropy_sums(n_rounds)
languages = languages(n_signals,n_meanings,n_agents)


################################################################################
# MAIN LOOP

for r in range(0,n_rounds):
    
    #print("round: " +str(r))
    print(get_pM(languages[1]))
    print(get_pM(languages[2]))
    print(get_pM(languages[3]))
    print(get_pM(languages[4]))
    print(get_pM(languages[0]))
    
    cost = init_cost(n_agents)
    interactions_per_agent = init_interactions_per_agent(n_agents)
    signal_entropies = init_signal_entropies(n_agents)
    meaning_entropies = init_meaning_entropies(n_agents)

    ## Could also do -->
    #cost, interactions_per_agent, signal_entropies, meaning_entropies = initalize_round(n_agents)
    ## But, I think the above is clearer


    # each agent makes their own proposal distribution
    # see comment on function proposal_matrix_maker() above.

    proposals = propose(n_agents,n_signals,n_meanings,languages)
    
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
    meaning_entropy_sums[r+1] = numpy.sum([meaning_entropies])
    
    # also, see the max_ent_sum() function above.  It computes the ceiling for this raw sum for any parameter combo.
    
    ############################################################################
        
    # end of rounds loop

# end of simulation

################################################################################
# final analyses

#print("signal_entropy_sums: "+str(signal_entropy_sums))
#print("meaning_entropy_sums: "+str(meaning_entropy_sums))
#print("successes per round: "+str(successes_per_round))

################################################################################


# plot stuff
import matplotlib.pyplot as plt

plt.plot(successes_per_round, 'grey', linewidth=2.0)
plt.plot(signal_entropy_sums, 'black', linewidth=2.0) # entropy of meanings per signal
plt.plot(meaning_entropy_sums, 'blue') # entropy of signals per meaning
#plt.plot([n_interactions*n_agents]*n_rounds, 'grey', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[0]*n_agents]*n_rounds, 'black', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[1]*n_agents]*n_rounds, 'blue', linestyle="--", linewidth=1)
plt.show()
