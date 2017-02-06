
import auxo.report
import unittest

class TestReport(unittest.TestCase):
	def testResultContructor(self):
		r = auxo.report.Report('A', 'B')
		self.assertEqual(r.name, 'A')
		self.assertEqual(r.text, 'B')
	
	def testResultAddText(self):
		r = auxo.report.Report('Name')
		self.assertEqual(r.name, 'Name')
		self.assertEqual(r.text, None)
		r.addText('A')
		self.assertEqual(r.name, 'Name')
		self.assertEqual(r.text, 'A')
		r.addText('BC')
		self.assertEqual(r.name, 'Name')
		self.assertEqual(r.text, 'ABC')
		
	def testAlwaysReportDefaultsFalse(self):
		self.assertFalse(auxo.report.always_report)
		
