import unittest
from cloudr.utils import change_path_prefix


class TestUtils(unittest.TestCase):

    def test_change_path_prefix(self):
        self.assertEqual(change_path_prefix('/123', '/', '/'), '/123')
        self.assertEqual(change_path_prefix('/123/234', '/123', '/123'), '/123/234')
        self.assertEqual(change_path_prefix('/123', '/', '/234'), '/234/123')
        self.assertEqual(change_path_prefix('/123', '/', '/123'), '/123/123')
        self.assertEqual(change_path_prefix('/123/345', '/123', '/'), '/345')
        self.assertEqual(change_path_prefix('/123/234/345', '/123/234', '/456'), '/456/345')
        self.assertEqual(change_path_prefix('/123/345', '/123', '/234/456'), '/234/456/345')


if __name__ == "__main__":
    unittest.main()
