
# this is what David asked us to do on our October 2 meeting
# convert the joint distribution over signals x meanings
# into a conditional distribution (the distribution over signals PER meaning).
# input = an sxm matrix, output = an sxm matrix.

def joint_to_conditional(language_matrix):   
    matrix = deepcopy(language_matrix)
    for meaning in range(0,len(matrix[0])):
        # get the probabilities of each signal for that meaning and normalize them.
        all_signals = matrix[:,meaning]/sum(matrix[:,meaning])
        matrix[:,meaning] = all_signals
    return(matrix)
    
# example calculation of distance between two languages (i.e. signal-meaning matrices)
# KL_two_matrices(numpy.transpose(joint_to_conditional(languages[0])),numpy.transpose(joint_to_conditional(languages[1])))
