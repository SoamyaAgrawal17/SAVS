import unittest


class Test_TestEventService(unittest.TestCase):
    def setUp(self):
        self.x = None

    def tearDown(self):
        self.x = None

    def test_sample(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()