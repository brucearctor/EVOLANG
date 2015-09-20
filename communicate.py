
"""
communicate()

    send()
    receive()
    infer()
    history()
"""


import numpy
from sketch_functions import get_pM


def find_sender_and_receiver(n_agents):
	pair = numpy.random.choice(n_agents,2,replace=False)
	sender = pair[0]
	receiver = pair[1]
	return(sender,receiver)


def produce_signal(sender,proposals,n_meanings,n_signals):
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
    ## IN THIS FUNCTION, noise would be things like freudian slips, or mis-pronounciations?  
    return(signal_produced,meaning_intended)


def infer_meaning(receiver,proposals,signal_received,n_meanings):

    # receiver infers a meaning for that signal
    # by randomly selecting a meaning from their proposal distribution, 
    # according to their meaning weights for the signal they received.
    signal_received = signal_produced
    prelim_weights = proposals[receiver][signal_received]
    weights = prelim_weights/numpy.sum(prelim_weights)
    meaning_inferred = numpy.random.choice(range(0,n_meanings),p=weights)
    return(meaning_inferred)

