import parameter_setup
from initialize import init_parrallel
import initialize 
from communicate import find_sender_and_receiver
from communicate import produce_signal
from communicate import infer_meaning

"""
n_agents = parameter_setup.n_agents
#interactions_per_agent = parameter_setup.interactions_per_agent
n_meanings = parameter_setup.n_meanings
n_signals = parameter_setup.n_signals
"""



class A():

	n_agents = parameter_setup.n_agents
	n_rounds = parameter_setup.n_rounds
	n_meanings = parameter_setup.n_meanings
	n_signals = parameter_setup.n_signals


	cost,interactions_per_agent = init_parrallel(n_agents,n_rounds)

	@classmethod
	def communication(self,round,proposals,n_agents=n_agents,n_rounds=n_rounds,n_meanings=n_meanings,n_signals=n_signals):

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
	    self.interactions_per_agent[round][sender] += 1
	    self.interactions_per_agent[round][receiver] += 1
	    
	    if meaning_intended == meaning_inferred:
	        self.cost[round][sender] += 1
	        self.cost[round][receiver] += 1
	        #self.total_cost[round][sender] += 1
	        #self.total_cost[round][receiver] += 1

	    #return()









	    """
	    STUFF!!!
	    """


	    """

	    initialize all of the blank variables needed (with an added dimension of round)

	    pass in round and any other needed information

	    Outside of this, call the needed variables, based upon the round...

	    """

