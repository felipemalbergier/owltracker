import unittest

from owltracker.data.integrations.clickup.task_clickup import ClickupTask


class TestClickupTask(unittest.TestCase):
    def setUp(self):
        self.task_data = {"id": 1, "name": "Test Task"}
        self.task = ClickupTask(self.task_data)

    def test_init(self):
        self.assertEqual(self.task.id, self.task_data['id'])
        self.assertEqual(self.task.title, self.task_data['name'])
        self.assertEqual(self.task.source, 'clickup')
        self.assertEqual(self.task.original_data, self.task_data)

if __name__ == '__main__':
    unittest.main()