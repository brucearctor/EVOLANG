def evaluate_based_on_prior_round(n_agents,cost,interactions_per_agent,languages,threshold,proposals):
    decision_to_keep = [0]*n_agents # true = keep proposal, false = revert
    for i in range(0,n_agents):
        if cost[i] > 0: # to prevent divisions by zero.
            if cost[i]/float(interactions_per_agent[i]) >= threshold[i]:
                decision_to_keep[i] = "true"
            else:
                decision_to_keep[i] = "false"
        else:
            decision_to_keep[i] = "false"
        
        if cost[i] == 0.0:
            threshold[i] = 0.0
        else: 
            threshold[i] = cost[i]/float(interactions_per_agent[i])

    languages = update_language(n_agents,decision_to_keep,languages,proposals)
    return(languages,threshold)


def evaluate(n_agents,cost,interactions_per_agent,languages,threshold,proposals):
    decision_to_keep = [0]*n_agents # true = keep proposal, false = revert
    for i in range(0,n_agents):
        if cost[i] > 0: # to prevent divisions by zero.
            if cost[i]/float(interactions_per_agent[i]) >= threshold[i]:
                decision_to_keep[i] = "true"
                threshold[i] = cost[i]/float(interactions_per_agent[i])
            else:
                decision_to_keep[i] = "false"
        else:
            decision_to_keep[i] = "false"

    languages = update_language(n_agents,decision_to_keep,languages,proposals)
    return(languages,threshold)

# this is the original evaluate function
def evaluate_fixed_threshold(n_agents,cost,interactions_per_agent,languages,threshold,proposals):
    decision_to_keep = [0]*n_agents # true = keep proposal, false = revert
    for i in range(0,n_agents):
        if cost[i] > 0: # to prevent divisions by zero.
            if cost[i]/float(interactions_per_agent[i]) >= threshold[i]:
                decision_to_keep[i] = "true"
            else:
                decision_to_keep[i] = "false"
        else:
            decision_to_keep[i] = "false"

    languages = update_language(n_agents,decision_to_keep,languages,proposals)
    return(languages,threshold,decision_to_keep)


def update_language(n_agents,decision_to_keep,languages,proposals):                    
    # update agents' languages
    for i in range(0,n_agents):
        if decision_to_keep[i] == "true":
            languages[i] = proposals[i]
    return languages
