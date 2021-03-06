
import multiprocessing

## Should more specifically import (instead of *) ??
import parameter_setup
from initialize import *
from communicate import C_C
from propose import *
from sketch_functions import *
import numpy
import scipy, scipy.stats
from evaluate import *
#from copy import deepcopy
#from KL_divergence import *
import time
t0 = time.time()

n_rounds = parameter_setup.n_rounds
n_agents = parameter_setup.n_agents
n_signals = parameter_setup.n_signals
n_meanings = parameter_setup.n_meanings
n_interactions = parameter_setup.n_interactions
initial_threshold = parameter_setup.threshold
logging = parameter_setup.logging
proposal_protocol = parameter_setup.proposal_protocol
communication_protocol = parameter_setup.communication_protocol
evaluation_protocol = parameter_setup.evaluation_protocol
"""
print("n_rounds:")
print(n_rounds)
print("n_agents:")
print(n_agents)
print("n_signals:")
print(n_signals)
print("n_meanings:")
print(n_meanings)
print("n_interactions:")
print(n_interactions)
print("initial_threshold:")
print(initial_threshold)
print("proposal_protocol:")
print(proposal_protocol)
print("communication_protocol:")
print(communication_protocol)
print("evaluation_protocol:")
print(evaluation_protocol)
"""

## THIS COULD BE A SINGLE LINE, but I think this is clearer
successes_per_round = successes_per_round(n_rounds)
total_cost = total_cost(n_agents)
signal_entropy_sums = init_signal_entropy_sums(n_rounds)
meaning_entropy_sums = init_meaning_entropy_sums(n_rounds)
languages = languages(n_signals,n_meanings,n_agents)
threshold = init_threshold(n_agents,initial_threshold)
#threshold_last_round = threshold

################################################################################
# MAIN LOOP

#final_round_number = n_rounds-1

print("")

for r in range(0,n_rounds):
    """
    #print("round: " +str(r))
    if logging == 'stuff':
        if(r == 0):
            print("")
            print("the random initial language:")
            print(languages[0])
            print("")
            print("round: " +str(r))
            print("pMs:")
            for i in range(len(languages)):
                print(get_pM(languages[i]))
            print("pSs:")
            for i in range(len(languages)):
                print(get_pS(languages[i]))
    """

    signal_entropies = init_signal_entropies(n_agents)
    meaning_entropies = init_meaning_entropy_sums(n_agents)
    # each agent makes their own proposal distribution
    
    # PROPOSE
    if proposal_protocol == "pm_fixed":
        proposals = propose_pMfixed(n_agents,n_signals,n_meanings,languages)
    elif proposal_protocol == "something_else":
        proposals = propose_someotherway(stuff)
    else:
        proposals = default

    ############################################################################
    jobs = []
    for k in range(0,n_interactions):

        if communication_protocol == "original":
            p = multiprocessing.Process(target=C_C.communication(r,proposals))
            jobs.append(p)
            p.start()

    cost = C_C.cost[r]
    interactions_per_agent = C_C.interactions_per_agent[r]
    ## Definition of success?
    ## Objective, or subjective to receiver
    ## Room for corrections?
    ## If receiver thinks they understand meaning?
    
    # EVALUATE
    languages,threshold,decision_to_keep = evaluate_fixed_threshold(n_agents,cost,interactions_per_agent,languages,threshold,proposals)
    
    # MORE PRINTING!
    """
    if(r%10==0):
        print("cost")
        print(cost)
        print("decision_to_keep")
        print(decision_to_keep)
        print("languages")
        print(languages)
    """
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

t1 = time.time()

print("total time")
print(str(t1-t0))
# plot stuff

import matplotlib.pyplot as plt

plt.plot(successes_per_round, 'grey', linewidth=2.0)
plt.plot(signal_entropy_sums, 'black', linewidth=2.0) # entropy of meanings per signal
plt.plot(meaning_entropy_sums, 'blue') # entropy of signals per meaning
#plt.plot([n_interactions*n_agents]*n_rounds, 'grey', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[0]*n_agents]*n_rounds, 'black', linestyle="--", linewidth=1)
plt.plot([max_ent_sum(n_signals,n_meanings)[1]*n_agents]*n_rounds, 'blue', linestyle="--", linewidth=1)
plt.show()




