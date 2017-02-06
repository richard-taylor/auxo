
import logging
logging.basicConfig(filename='/tmp/pyunit')

import auxo.agent
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

    def testBaseAgent(self):
        a = auxo.agent.BaseAgent('foo')
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.state['load-state-error'], 'loadState not called')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        self.assertEqual(a.state['load-state-error'], "[Errno 2] No such file or directory: '/tmp/foo.json'")
        a.saveState()
        a.loadState()
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, None)
        
    def testWebAgent(self):
        auxo.agent.http = mockHTTP(({'status': '200', 'content-length': '4'}, b'1234'))
            
        a = auxo.agent.WebAgent('foo', 'http://example.com/')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        a.saveState()
        a.loadState()
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.url, 'http://example.com/')
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(a.state['http-status'], '200')
        self.assertEqual(a.state['content-length'], '4')
        self.assertEqual(a.content, b'1234')
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, None)
    
    def testHashWebAgent(self):
        auxo.agent.http = mockHTTP(({'status': '200', 'content-length': '5'}, b'12345'))
            
        a = auxo.agent.HashWebAgent('foo', 'http://example.com/')
        
        helperRemove('/tmp/foo.json')
        a.loadState()
        a.saveState()
        a.loadState()
        self.assertEqual(a.name, 'foo')
        self.assertEqual(a.url, 'http://example.com/')
        self.assertEqual(a.state['load-state-error'], '')
        
        r = a.result()
        self.assertEqual(a.state['http-status'], '200')
        self.assertEqual(a.state['content-length'], '5')
        self.assertEqual(a.state['content-hash'], '8cb2237d0679ca88db6464eac60da96345513964')
        self.assertEqual(a.content, b'12345')
        self.assertEqual(r.name, 'foo')
        self.assertEqual(r.text, 'The page has changed: http://example.com/\n')
        
    def testGLiveAgent(self):
        with open('events.html', 'rb') as f:
            # read in the sample HTML page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = mockHTTP(({'status': '200', 'content-length': str(length)}, content))
            
            a = auxo.agent.GLiveAgent()
            self.assertTrue('events' in a.state)
            
            r = a.result()
            # print(r.text)
            
            e = a.state['events']
            self.assertNotEqual(len(e), 0)
            
            gala = e['2A28F917-2710-4F2C-BBAE-5DA2471BAA53']
            self.assertEqual(gala['description'], 'Johann Strauss Gala')
            self.assertEqual(gala['start date'], 'Wednesday 30 Dec 2015 at 7:30pm')
            self.assertEqual(gala['end date'], '')
            self.assertEqual(gala['min price'], '£29.50')
            self.assertEqual(gala['max price'], '£38.50')
            
            
    def testCubingAgent(self):
        with open('europe.html', 'rb') as f:
            # read in the previously downloaded page
            content = f.read()
            length = len(content)
            self.assertTrue(length > 0)
            
            auxo.agent.http = mockHTTP(({'status': '200', 'content-length': str(length)}, content))
        
            a = auxo.agent.CubingAgent()
            self.assertTrue('events' in a.state)
        
            r = a.result()
            # print(r.text)
            
            e = a.state['events']
            self.assertEqual(len(e), 39)

