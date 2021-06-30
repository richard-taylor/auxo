
import auxo.debug_agent
import unittest
        
class TestDebugAgent(unittest.TestCase):

    def testRunTimeAgent(self):
        a = auxo.debug_agent.RunTimeAgent()
        r = a.result()
        self.assertTrue('day' in r.text and '2021' in r.text)

    def testServerLogAgent(self):
        a = auxo.debug_agent.ServerLogAgent('access-log.txt')
        r = a.result()
        self.assertTrue('code 2xx 2' in r.text)
        self.assertTrue('code 3xx 0' in r.text)
        self.assertTrue('code 4xx 1' in r.text)
        self.assertTrue('code 5xx 1' in r.text)
        self.assertTrue('code xxx 0' in r.text)

    def testServerLogAgentMissingFile(self):
        a = auxo.debug_agent.ServerLogAgent('missing-log.txt')
        r = a.result()
        self.assertTrue('Cannot find log file missing-log.txt' in r.text)
