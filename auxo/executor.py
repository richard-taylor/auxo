
# this could be a lot more sophisticated.
# but it just runs the agents one at a time.

import logging
import traceback
import auxo.report

def run(agent_list):
    logging.info('Running all the agents.')
    results = []
    
    for a in agent_list:
        try:
            a.loadState()
            results.append(a.result())
            a.saveState()
            
        except Exception:
            logging.error("Exception from agent " + a.name + ": " + traceback.format_exc())
            results.append(auxo.report.Report(a.name, "Failed to complete.\n"))
        
    return results

