import unittest
from unittest.mock import Mock, patch
from owltracker.main import Controller
from owltracker.ui.view import View

class TestController(unittest.TestCase):
    def setUp(self):
        self.controller = Controller()

    @patch('owltracker.main.Controller.start_stopwatch')
    @patch('owltracker.main.Controller.stop_stopwatch')
    def test_handle_stopwatch_event(self, mock_start_stopwatch, mock_stop_stopwatch):
        # Mock the view's clicked_stop_watch_button method to return True
        # self.view.clicked_stop_watch_button.return_value = True

        # Call the method with a 'stopwatch_button' event
        self.controller.handle_stopwatch_event(View.stopwatch_button_key)

        # Check that the start_stopwatch method was called
        self.controller.start_stopwatch.assert_called_once()

        # Set stopwatch_active to True
        self.controller.stopwatch_active = True

        # Call the method with a 'stopwatch_button' event again
        self.controller.handle_stopwatch_event(View.stopwatch_button_key)

        # Check that the stop_stopwatch method was called
        self.controller.stop_stopwatch.assert_called_once()

    @patch('owltracker.ui.view.View.create_minimized_window')
    def test_handle_minimize_event(self, mock_create_minimized_window):
        # Mock the view's clicked_minimize_button method to return True
        # self.view.clicked_minimize_button.return_value = True

        # Call the method with a 'minimize_button' event
        self.controller.handle_minimize_event(View.minimize_button_key)

        # Check that the create_minimized_window method was called
        self.controller.view.create_minimized_window.assert_called_once()

    @patch('owltracker.ui.view.View.create_main_window')
    def test_handle_main_window_event(self, mock_create_main_window):
        self.controller.view.window = Mock()
        self.controller.view.window.Title = View.minimized_title_window

        # Mock the view's is_minimized_window method to return True
        # self.view.is_minimized_window.return_value = True

        # Mock the view's cliked_go_to_main_window method to return True
        # self.view.cliked_go_to_main_window.return_value = True

        # Call the method with a 'minimized_title_window' event
        self.controller.handle_main_window_event(View.stopwatch_text_key)

        # Check that the create_main_window method was called
        self.controller.view.create_main_window.assert_called_once()
    
    @patch('owltracker.ui.view.View.create_after_idle_window')
    def test_handle_idle_window_creation(self, mock_create_after_idle_window):
        self.controller.view.window = Mock()
        self.controller.view.window.Title = f"NOT {View.idle_title_window}"

        # Mock the view's is_window_idle method to return False
        # self.view.is_window_idle.return_value = False

        # Set stopwatch_active to True
        self.controller.stopwatch_active = True

        # Set idle_time to 10
        self.controller.idle_time = 10
        self.controller.notification.LIMIT_IDLE_TIME_WITH_TASK = 9

        # Call the method
        self.controller.handle_idle_window_creation()

        # Check that the create_after_idle_window method was called
        self.controller.view.create_after_idle_window.assert_called_once()

    @patch('owltracker.ui.view.View.update_idle_text')
    def test_update_idle_text(self, mock_update_idle_text):
        self.controller.view.window = Mock()
        self.controller.view.window.Title = View.idle_title_window

        # Set idle_start_time to 0
        self.controller.idle_start_time = 0

        # Call the method
        self.controller.update_idle_text()

        # Check that the update_idle_text method was called
        self.controller.view.update_idle_text.assert_called_once()

    @patch('owltracker.ui.view.View.create_minimized_window')
    @patch('owltracker.main.time.time')
    def test_handle_remove_idle_time(self, time_mock, mock_create_minimized_window):
        # self.controller.view.update_window.return_value = Mock() # cant make it mock
        
        time_mock_value = 100
        start_time = 10
        idle_start_time = 75

        time_mock.return_value = time_mock_value
        self.controller.start_time = start_time
        self.controller.idle_start_time = idle_start_time

        # Call the method with a 'remove_idle_time' event
        self.controller.handle_idle_screen_actions(View.remove_idle_time)

        # Check that the idle_time was set to 0
        self.assertEqual(self.controller.start_time, start_time + time_mock_value - idle_start_time)
    
    # simulate clicked_consider_idle_time
    @patch('owltracker.ui.view.View.create_minimized_window')
    def test_handle_consider_idle_time(self, mock_create_minimized_window):
        start_time = 10
        self.controller.start_time = start_time
        self.controller.idle_start_time = 50

        # Call the method with a 'consider_idle_time' event
        self.controller.handle_idle_screen_actions(View.consider_idle_time)

        # Check that the idle_time was set to 0
        self.assertEqual(self.controller.start_time, start_time)


        

if __name__ == '__main__':
    unittest.main()