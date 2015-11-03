from sketch_functions import proposal_matrix_maker
from sketch_functions import proposal_matrix_maker_pMfixed

def propose(n_agents,n_signals,n_meanings,languages):

	proposals = []
	for i in range(0,n_agents):
	    proposals.insert(i,proposal_matrix_maker(n_signals,n_meanings,languages[i]))
	return(proposals)

# this is the one to use now
# it doesn't allow agents to propose changes to the probability over meanings	
def propose_pMfixed(n_agents,n_signals,n_meanings,languages):

	proposals = []
	for i in range(0,n_agents):
	    proposals.insert(i,proposal_matrix_maker_pMfixed(n_signals,n_meanings,languages[i]))
	return(proposals)
