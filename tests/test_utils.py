import unittest
from owltracker.utils import time_to_formated_string


class TestUtils(unittest.TestCase):
    def test_time_to_formated_string(self):
        self.assertEqual(time_to_formated_string(3661), "01:01:01")
        self.assertEqual(time_to_formated_string(61), "01:01")
        self.assertEqual(time_to_formated_string(1), "1.0")
        self.assertEqual(time_to_formated_string(0), "0.0")
        self.assertEqual(time_to_formated_string(3600), "01:00:00")
        self.assertEqual(time_to_formated_string(60), "01:00")
        self.assertEqual(time_to_formated_string(3599), "59:59")


if __name__ == '__main__':
    unittest.main()
