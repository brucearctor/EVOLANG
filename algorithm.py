
## Should more specifically import (instead of *) ??
import parameter_setup
from initialize import *
from communicate import *
from propose import *
from sketch_functions import *
import numpy
import scipy, scipy.stats
from evaluate import *
#from copy import deepcopy
#from KL_divergence import *

n_rounds = parameter_setup.n_rounds
n_agents = parameter_setup.n_agents
n_signals = parameter_setup.n_signals
n_meanings = parameter_setup.n_meanings
n_interactions = parameter_setup.n_interactions
initial_threshold = parameter_setup.threshold
output = parameter_setup.output

## THIS COULD BE A SINGLE LINE, but I think this is clearer
successes_per_round = successes_per_round(n_rounds)
total_cost = total_cost(n_agents)
signal_entropy_sums = init_signal_entropy_sums(n_rounds)
meaning_entropy_sums = init_meaning_entropy_sums(n_rounds)
languages = languages(n_signals,n_meanings,n_agents)
threshold = init_threshold(n_agents,initial_threshold)
threshold_last_round = threshold


################################################################################
# MAIN LOOP

last_round = n_rounds-1

for r in range(0,n_rounds):
    
    #print("round: " +str(r))
    #print(threshold)
    if output == 'stuff':
        if(r==0 or r==1 or r==last_round):
            if(r==0):
                print("")
                print("the random initial language:")
                print(languages[0])
            print("")
            print("round: " +str(r))
            print("pMs:")
            for i in range(0,5):
                print(get_pM(languages[i]))
            print("pSs:")
            for i in range(0,5):
                print(get_pM(languages[i]))

    ## 4 Lines or 1 ??? -->
    ##cost = init_cost(n_agents)
    ##interactions_per_agent = init_interactions_per_agent(n_agents)
    ##signal_entropies = init_signal_entropies(n_agents)
    ##meaning_entropies = init_meaning_entropies(n_agents)
    cost, interactions_per_agent, signal_entropies, meaning_entropies = initialize_round(n_agents)

    # each agent makes their own proposal distribution
    
    # PROPOSE
    #proposals = propose(n_agents,n_signals,n_meanings,languages)
    proposals = propose_pMfixed(n_agents,n_signals,n_meanings,languages)
    
    ############################################################################
    
    for k in range(0,n_interactions):

        # NEED TO UNDERSTAND MORE ABOUT HOW MANY INTERACTIONS per pair, per person, etc.
        sender,receiver=find_sender_and_receiver(n_agents)
        
        signal_produced, meaning_intended = produce_signal(sender,proposals,n_meanings,n_signals)

        ## I WONDER WHETHER WE WANT TO INTRODUCE NOISE TO THE SIGNAL, SO LEAVE THIS OUTSIDE OF FUNCTION
        ## LIKE a function for infer signal, which could have various types of noise
        signal_received = signal_produced

        # receiver infers a meaning for that signal
        # by randomly selecting a meaning from their proposal distribution, 
        # according to their meaning weights for the signal they received.
        meaning_inferred = infer_meaning(receiver,proposals,signal_received,n_meanings)
             
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
    
    ## Definition of success?
    ## Objective, or subjective to receiver
    ## Room for corrections?
    ## If receiver thinks they understand meaning?
    
    # EVALUATE
    languages,threshold = evaluate_fixed_threshold(n_agents,cost,interactions_per_agent,languages,threshold,proposals)
    #languages,threshold_last_round = evaluate(n_agents,cost,interactions_per_agent,languages,threshold,proposals)
    #languages,threshold = evaluate_based_on_prior_round(n_agents,cost,interactions_per_agent,languages,threshold,proposals)


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
