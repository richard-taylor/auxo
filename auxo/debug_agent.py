
import datetime
import auxo.agent

class RunTimeAgent(auxo.agent.BaseAgent):
    '''
    An agent which reports the local time when it was executed.
    '''
    
    def __init__(self):
        super().__init__('RunTime')
        
    def result(self):
        report = super().result()
        report.addText(datetime.datetime.now().isoformat()  + '\n')

        return report
