import unittest
from unittest.mock import patch
from owltracker.data.integrations.clickup import Clickup

class TestClickup(unittest.TestCase):
    def setUp(self):
        self.clickup = Clickup()

    @patch('requests.get')
    def test_get_list_tasks(self, mock_get):
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = {"tasks": [{"id": 1, "name": "Test Task"}]}
        
        tasks = self.clickup.get_list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[0].title, "Test Task")

if __name__ == '__main__':
    unittest.main()