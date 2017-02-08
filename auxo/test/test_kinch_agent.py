
import logging
logging.basicConfig(filename='/tmp/pyunit')

import auxo.kinch_agent
import os
import unittest

def helperRemove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass

class mockHTTP(object):
    def __init__(self, return_value):
        self.return_value = return_value
        
    def request(self, url, method):
        return self.return_value
        
class TestAgent(unittest.TestCase):

    def testKinchAgent(self):
        with open('kinch.html', 'rb') as f:
            # read in the previously downloaded page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = mockHTTP(({'status': '200', 'content-length': str(length)}, content))
            
            a = auxo.kinch_agent.KinchAgent('Kinch', 'Harry Taylor', 'all')
            r = a.result()
            
            self.assertTrue('rank' in a.state)
            self.assertTrue('score' in a.state)
            
            self.assertEqual(a.state['rank'], '61')
            self.assertEqual(a.state['score'], '22.39')

    def testMissingPerson(self):
        with open('kinch.html', 'rb') as f:
            # read in the previously downloaded page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = mockHTTP(({'status': '200', 'content-length': str(length)}, content))
            
            a = auxo.kinch_agent.KinchAgent('Kinch', 'Dr Who', 'all')
            r = a.result()
            
            self.assertEqual(r.text, 'Cannot find Dr Who on the page.\n')
                     
    def testTiedRank(self):
        with open('kinch.html', 'rb') as f:
            # read in the previously downloaded page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = mockHTTP(({'status': '200', 'content-length': str(length)}, content))
            
            a = auxo.kinch_agent.KinchAgent('Kinch', 'Joe Barsby', 'all')
            r = a.result()
            
            self.assertTrue('rank' in a.state)
            self.assertTrue('score' in a.state)
            
            self.assertEqual(a.state['rank'], '???')
            self.assertEqual(a.state['score'], '22.39')
            
