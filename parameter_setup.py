## Evaluation Criteria
## If potential many types of evaluation, include a variable here to select which evaluation function


# number of agents in the population
n_agents = 100

# n_agents also equals the number of languages (joint distributions over signals and meanings) in the population.

## NEED IT?  (in this case, we use language to refer to what each individual 'speaks')
## I wonder about after lots of iterations and divergences -- then looking at clustering similarity of individual's 'languages' into more groups of more global languages
## That might be where terminology gets tricky

# set language size
n_meanings = 10
n_signals = 10

n_rounds = 100
# each round is composed of n interactions between a pair of agents,
# who are randomly drawn from the population

n_interactions = 50
# number of random interactions that occur before agents decide whether 
# or not to keep their proposal distributions

threshold = 0.9
# proportion successful interactions an agent needs to have to keep their proposal distribution


# What sort of logging?
# for first 2 rounds and last, use:  'stuff'
logging = 'stuff'


# which propose
proposal_protocol = "pm_fixed"


# which communicate
communication_protocol = "original"

# which evaluate
evaluation_protocol = "fixed_threshold"



