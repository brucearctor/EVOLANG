from sketch_functions import proposal_matrix_maker

def propose(n_agents,n_signals,n_meanings,languages):

	proposals = []
	for i in range(0,n_agents):
	    proposals.insert(i,proposal_matrix_maker(n_signals,n_meanings,languages[i]))
	return(proposals)