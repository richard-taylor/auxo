
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.cubing_agent
import auxo.test.mocks
import unittest
        
class TestCubingAgent(unittest.TestCase):

    def testCubingAgent(self):
        with open('europe.html', 'rb') as f:
            # read in the previously downloaded page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = auxo.test.mocks.mockHTTP(
                ({'status': '200', 'content-length': str(length)}, content))
        
            a = auxo.cubing_agent.CubingAgent()
            r = a.result()
            
            comps = a.state['comps']
            self.assertEqual(len(comps), 38)
            
            found = False
            
            for key, value in comps.items():
                if value['title'] == 'Euro 2016':
                    found = True
                    self.assertEqual(value['date'], 'Jul 15 - 17, 2016')
                    self.assertEqual(value['location'], 'Czech Republic, Prague')
            
            self.assertTrue(found)

