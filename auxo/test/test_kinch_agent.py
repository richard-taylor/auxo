
import logging
logging.basicConfig(filename='/tmp/unittest')

import auxo.kinch_agent
import auxo.test.mocks
import unittest
        
class TestKinchAgent(unittest.TestCase):

    def testKinchAgent(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('kinch.html')
            
        a = auxo.kinch_agent.KinchAgent('Kinch', 'Harry Taylor', 'all')
        r = a.result()
            
        self.assertTrue('rank' in a.state)
        self.assertTrue('score' in a.state)
            
        self.assertEqual(a.state['rank'], '61')
        self.assertEqual(a.state['score'], '22.39')

        self.assertTrue('New rank: 61' in r.text)
        self.assertTrue('New score: 22.39' in r.text)

    def testChange(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('kinch.html')
            
        a = auxo.kinch_agent.KinchAgent('Kinch', 'Harry Taylor', 'all')
        a.state['rank'] = '65'
        a.state['score'] = '21.21'
        r = a.result()
            
        self.assertTrue('Changed rank: 61 (was 65)' in r.text)
        self.assertTrue('Changed score: 22.39 (was 21.21)' in r.text)
            
        self.assertEqual(a.state['rank'], '61')
        self.assertEqual(a.state['score'], '22.39')

    def testMissingPerson(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('kinch.html')
            
        a = auxo.kinch_agent.KinchAgent('Kinch', 'Dr Who', 'all')
        r = a.result()
            
        self.assertEqual(r.text, 'Cannot find Dr Who on the page.\n')
                     
    def testTiedRank(self):
        auxo.agent.http = auxo.test.mocks.mockHttpFile('kinch.html')
            
        a = auxo.kinch_agent.KinchAgent('Kinch', 'Joe Barsby', 'all')
        r = a.result()
            
        self.assertTrue('rank' in a.state)
        self.assertTrue('score' in a.state)
            
        self.assertEqual(a.state['rank'], '???')
        self.assertEqual(a.state['score'], '22.39')
 
