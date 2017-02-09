
# this could be a lot more sophisticated.
# but it just runs the agents one at a time.

import logging

def run(agent_list):
    logging.info('Running all the agents.')
    results = []
    
    for a in agent_list:
        a.loadState()
        results.append(a.result())
        a.saveState()
        
    return results
