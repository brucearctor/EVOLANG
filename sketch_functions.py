import numpy
import scipy, scipy.stats

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

def proposal_matrix_maker_pMfixed(n_signals,n_meanings,old_matrix):
    # how an agent chooses a particular deviation from their current language
    # this deviation will be referred to as a "proposal distribution"
    # for starters, they change it with a uniform random delta function
    # 1) so nothing becomes negative
    # 2) so all entries still sum to one 
    # 3) and pM remains the same
    delta_max = (1.0/(n_signals*n_meanings))/10
    delta_matrix = numpy.random.uniform(0,delta_max,size=(n_signals, n_meanings))
    # normalize the columns
    delta_matrix /=  delta_matrix.sum(axis=0)[numpy.newaxis,:]
    # multiply each cell by the desired sum (which is pM, so that pM stays the same)
    delta_matrix *= get_pM(old_matrix)
    # add the delta matrix and normalize so whole matrix sums to one
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
    