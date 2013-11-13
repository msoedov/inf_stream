import unittest
from sequence_filter import *


class LinearSequenceTest(unittest.TestCase):
    function_under_test = None

    @classmethod
    def setUpClass(cls):
        cls.function_under_test = lambda _self, *a, **k: linear_sequence(*a, **k)

    def testCase1(self):
        """Sequence of "" in middle """
        data_inn =  ["abc", "123", "", "x", "", "", "", "", "y"]
        data_out = list(self.function_under_test(data_inn))
        data_sample = ["abc", "123", "", "x", "", "y"]
        self.assertEqual(data_out, data_sample)

    def testCase2(self):
        """Sequence of "" in tail """
        data_inn =  ["abc", "123", "", "x", "y", "", "", "", ""]
        data_out = list(self.function_under_test(data_inn))
        data_sample = ["abc", "123", "", "x", "y"]
        self.assertEqual(data_out, data_sample)

    def testCase3(self):
        """
        Sequence of "" in head
        """
        data_inn =  ["", "", "", "", "abc", "123", "", "x", "y", ""]
        data_out = list(self.function_under_test(data_inn))
        data_sample = ["abc", "123", "", "x", "y"]
        self.assertEqual(data_out, data_sample)

    def testCase4(self):
        """Empty iterable """
        data_inn =  []
        data_out = list(self.function_under_test(data_inn))
        data_sample = []
        self.assertEqual(data_out, data_sample)

    def testCase5(self):
        """All "" in iterable """
        data_inn =  [""] * 10
        data_out = list(self.function_under_test(data_inn))
        data_sample = []
        self.assertEqual(data_out, data_sample)

    def testCase6(self):
        """No one match "" """
        data_inn =  ["$"] * 10
        data_out = list(self.function_under_test(data_inn))
        data_sample = data_inn[:]
        self.assertEqual(data_out, data_sample)

    def testCase7(self):
        """Common case """
        data_inn =  ["", "", "abc", "123", "", "x", "", "", "", "", "y", "", ""]
        data_out = list(self.function_under_test(data_inn))
        data_sample = ["abc", "123", "", "x", "", "y"]
        self.assertEqual(data_out, data_sample)


class SequenceTest(LinearSequenceTest):
    @classmethod
    def setUpClass(cls):
        cls.function_under_test = lambda s, *a, **k: sequence(*a, **k)

    def testCase10(self):
        """
        Common case with existing sequence of  <= 2 of "*"
        """
        data_inn =  ["*", "abc", "123", "*", "x", "*", "*", "*", "y", "*", "*" ]
        data_out = list(self.function_under_test(data_inn, symbol="*", inbound=2))
        data_sample = ["abc", "123", "*", "x", "*", "*", "y"]
        self.assertEqual(data_out, data_sample)

    def testCase11(self):
        """
        Common case with existing sequence of  <= 3 of "*"
        """
        data_inn =  ["*", "abc", "123", "*", "x", "*", "*", "*", "*", "y", "*", "*" ]
        data_out = list(self.function_under_test(data_inn, symbol="*", inbound=3))
        data_sample = ["abc", "123", "*", "x", "*", "*", "*", "y"]
        self.assertEqual(data_out, data_sample)

    def testCase12(self):
        """
        Additional check head/tail case for sequence <=3
        """
        data_inn =  ["*", "*", "*", "abc", "123", "*", "x", "*", "*", "*", "*", "y",
                     "*", "*", "*", "*", ]
        data_out = list(self.function_under_test(data_inn, symbol="*", inbound=3))
        data_sample = ["abc", "123", "*", "x", "*", "*", "*", "y"]
        self.assertEqual(data_out, data_sample)


if __name__ == '__main__':
    doc_tests()
    unittest.main()

