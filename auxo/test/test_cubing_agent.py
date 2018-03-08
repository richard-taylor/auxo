
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.cubing_agent
import auxo.test.mocks
import unittest
        
class TestCubingAgent(unittest.TestCase):

    def testCubingAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('uk-competitions.html')
        
        a = auxo.cubing_agent.CubingAgent()
        r = a.result()
            
        comps = a.state['comps']
        self.assertEqual(len(comps), 4)
            
        found = False
            
        for key, value in comps.items():
            if value['title'] == 'ABHC 2018':
                found = True
                self.assertEqual(value['date'], 'Aug 25 - 26, 2018')
                self.assertEqual(value['location'], 'United Kingdom, Crawley')
            
        self.assertTrue(found)

