
n_agents = 5
# number of agents in the population
# n_agents also equals the number of languages (joint distributions over signals and meanings) in the population.


# set language size
n_meanings = 6
n_signals = 10

n_rounds = 1000
# each round is composed of n interactions between a pair of agents,
# who are randomly drawn from the population

n_interactions = 10 
# number of random interactions that need to occur before agents decide whether 
# or not to keep their proposal distributions

threshold = 0.9
# proportion successful interactions an agent needs to have to keep their proposal distribution

