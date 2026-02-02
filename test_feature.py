import unittest
from feature import get_greeting

class TestFeature(unittest.TestCase):
    def test_get_greeting_default(self):
        self.assertEqual(get_greeting(), "Hello from the Swarm Actor-Orchestrator!")

    def test_get_greeting_custom(self):
        self.assertEqual(get_greeting("Teddy"), "Hello from the Teddy!")

if __name__ == "__main__":
    unittest.main()
