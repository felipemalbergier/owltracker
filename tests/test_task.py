import unittest
from owltracker.data.integrations.task import LocalTask, Task

class TestLocalTask(unittest.TestCase):
    def test_local_task(self):
        local_task = LocalTask('Test Task')
        self.assertEqual(local_task.title, 'Test Task')
        self.assertEqual(local_task.id, None)
        self.assertEqual(local_task.source, None) # This is here because in model.py we assume that the source is None for local tasks

if __name__ == '__main__':
    unittest.main()