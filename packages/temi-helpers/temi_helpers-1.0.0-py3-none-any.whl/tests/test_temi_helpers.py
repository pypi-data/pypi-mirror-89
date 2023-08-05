import unittest
import warnings

from temi_helpers import encrypt, decrypt

class TestBip38(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)

    def test_keys(self):
        self.assertEqual(encrypt('5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR', 'TestingOneTwoThree'), '6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg')
        self.assertEqual(decrypt('6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg', 'TestingOneTwoThree'), '5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR')

        self.assertEqual(encrypt('5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5', 'Satoshi'), '6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq')
        self.assertEqual(decrypt('6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq', 'Satoshi'), '5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5')

if __name__ == '__main__':
    unittest.main()