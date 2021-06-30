
import datetime
import re
import auxo.agent

class RunTimeAgent(auxo.agent.BaseAgent):
    '''
    An agent which reports the local time when it was executed.
    '''
    
    def __init__(self):
        super().__init__('RunTime')

    def result(self):
        report = super().result()
        report.addText(datetime.datetime.now().strftime('%H:%M %A %d-%m-%Y')  + '\n')

        return report

class ServerLogAgent(auxo.agent.BaseAgent):
    '''
    An agent which reports a summary of the web server log.
    '''

    def __init__(self, log_file_name):
        super().__init__('ServerLog')
        self.log_file_name = log_file_name

    def result(self):
        report = super().result()

        try:
            with open(self.log_file_name) as logfile:
                code_200 = 0
                code_300 = 0
                code_400 = 0
                code_500 = 0
                code_xxx = 0

                for line in logfile:
                    code_match = re.search(r'".*" (\d\d\d) ', line)
                    if code_match:
                        code = code_match.group(1)[0]
                        if code == '2':
                            code_200 += 1
                        elif code == '3':
                            code_300 += 1
                        elif code == '4':
                            code_400 += 1
                        elif code == '5':
                            code_500 += 1
                        else:
                            code_xxx += 1
                    else:
                        code_xxx += 1

                report.addText('code 2xx ' + str(code_200) + '\n')
                report.addText('code 3xx ' + str(code_300) + '\n')
                report.addText('code 4xx ' + str(code_400) + '\n')
                report.addText('code 5xx ' + str(code_500) + '\n')
                report.addText('code xxx ' + str(code_xxx) + '\n')

        except FileNotFoundError:
            report.addText('Cannot find log file ' + self.log_file_name + '\n')

        return report
