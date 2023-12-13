import unittest
from unittest.mock import Mock, patch

# from owltracker.data.integrations.clickup.clickup import Clickup        
from owltracker.data.integrations.clickup.clickup import Clickup

class TestClickup(unittest.TestCase):

    @patch('owltracker.data.integrations.clickup.clickup.requests.request')
    def test_get_list_tasks(self, mock_request):
        mock_request.return_value.ok = True
        mock_request.return_value.json.return_value = {"tasks": [{"id": 1, "name": "Test Task"}]}
        
        clickup = Clickup()
        tasks = clickup.get_list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Test Task")


if __name__ == '__main__':
    unittest.main()
