from owltracker.ui.notification import Notification
import unittest
from unittest.mock import patch
import time


class TestNotification(unittest.TestCase):
    def setUp(self):
        # This method is called before each test
        self.notification = Notification()
        # Set QUIET_TIME to custom values
        self.notification.QUIET_TIME_START = 20
        self.notification.QUIET_TIME_END = 8

    @patch('time.localtime')
    def test_during_custom_quiet_time_night(self, mock_localtime):
        # Simulate current time as 22:00 (during custom quiet time)
        mock_localtime.return_value = time.struct_time((0, 0, 0, 22, 0, 0, 0, 0, 0))
        self.assertTrue(self.notification.is_quiet_time())

    @patch('time.localtime')
    def test_during_custom_quiet_time_morning(self, mock_localtime):
        # Simulate current time as 07:00 (during custom quiet time)
        mock_localtime.return_value = time.struct_time((0, 0, 0, 7, 0, 0, 0, 0, 0))
        self.assertTrue(self.notification.is_quiet_time())

    @patch('time.localtime')
    def test_outside_custom_quiet_time(self, mock_localtime):
        # Simulate current time as 15:00 (outside custom quiet time)
        mock_localtime.return_value = time.struct_time((0, 0, 0, 15, 0, 0, 0, 0, 0))
        self.assertFalse(self.notification.is_quiet_time())

    @patch('time.localtime')
    def test_custom_quiet_time_start_boundary(self, mock_localtime):
        # Set QUIET_TIME to custom values for this specific test
        self.notification.QUIET_TIME_START = 22
        self.notification.QUIET_TIME_END = 9

        # Simulate current time as 22:00 (at the custom start of quiet time)
        mock_localtime.return_value = time.struct_time((0, 0, 0, 22, 0, 0, 0, 0, 0))
        self.assertTrue(self.notification.is_quiet_time())

    @patch('time.localtime')
    def test_custom_quiet_time_end_boundary(self, mock_localtime):
        # Set QUIET_TIME to custom values for this specific test
        self.notification.QUIET_TIME_START = 22
        self.notification.QUIET_TIME_END = 9

        # Simulate current time as 09:00 (at the custom end of quiet time)
        mock_localtime.return_value = time.struct_time((0, 0, 0, 9, 0, 0, 0, 0, 0))
        self.assertFalse(self.notification.is_quiet_time())

if __name__ == '__main__':
    unittest.main()
