from PyObjCTools.TestSupport import TestCase, min_os_level
import Intents


class TestINConditionalOperator(TestCase):
    @min_os_level("10.12")
    def testConstants(self):
        self.assertEqual(Intents.INConditionalOperatorAll, 0)
        self.assertEqual(Intents.INConditionalOperatorAny, 1)
        self.assertEqual(Intents.INConditionalOperatorNone, 2)
