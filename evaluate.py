

def evaluate(n_agents,cost,interactions_per_agent,languages,threshold,proposals):
    decision_to_keep = [0]*n_agents # true = keep proposal, false = revert
    for i in range(0,n_agents):
        if cost[i] > 0: # to prevent divisions by zero.
            if cost[i]/float(interactions_per_agent[i]) >= threshold:
                decision_to_keep[i] = "true"
            else:
                decision_to_keep[i] = "false"
        else:
            decision_to_keep[i] = "false"

    update_language(n_agents,decision_to_keep,languages,proposals)
    return(languages)


def update_language(n_agents,decision_to_keep,languages,proposals):                    
    # update agents' languages
    for i in range(0,n_agents):
        if decision_to_keep[i] == "true":
            languages[i] = proposals[i]



