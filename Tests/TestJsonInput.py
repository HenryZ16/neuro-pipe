import unittest
import os

from JSONInput.JSONInput import JSONInput


class TestJSONInput(unittest.TestCase):
    def setUp(self):
        self.json_input = JSONInput("Tests/test.json")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            JSONInput("Tests/non_existent_file.json")

    def test_invalid_json(self):
        with open("Tests/invalid.json", "w") as file:
            file.write("{invalid_json}")
        with self.assertRaises(ValueError):
            JSONInput("Tests/invalid.json")
        os.remove("Tests/invalid.json")

    def test_get_item(self):
        self.assertEqual(
            self.json_input["key"], "value"
        )  # Adjust based on your test.json content
