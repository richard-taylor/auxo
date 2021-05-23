
import auxo.debug_agent
import unittest
        
class TestDebugAgent(unittest.TestCase):

    def testRunTimeAgent(self):
        a = auxo.debug_agent.RunTimeAgent()
        r = a.result()
        self.assertTrue('T' in r.text)
