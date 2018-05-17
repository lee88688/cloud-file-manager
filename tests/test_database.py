import unittest
from cloudr import create_app

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def test_app_exsits(self):
        self.assertFalse(self.app is None)


if __name__ == "__main__":
    unittest.main()