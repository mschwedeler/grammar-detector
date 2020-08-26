import unittest
from src.features.noun_set.noun.detector import detect_nouns
from src.features.noun_set.noun.model import NounFeature


class TestNounDetector(unittest.TestCase):
    def assertNounText_(self, value, expected_texts):
        result = detect_nouns(value)
        count = 0
        for expected_text in expected_texts:
            noun = result[count]
            result_text = noun.phrase
            self.assertEqual(result_text, expected_text)
            count += 1

    def assertLastNoun_(self, value, expected):
        result = detect_nouns(value)
        self.assertEqual(result[len(result)], expected)

    def test_is_defined(self):
        self.assertTrue(detect_nouns)

    def test_returns_a_list_of_nouns(self):
        result = detect_nouns("I ran to the beach.")
        self.assertIsInstance(result, list)
        [self.assertIsInstance(noun, NounFeature) for noun in result]

    def test_true_positive(self):
        expected = NounFeature()
        expected.text = "I"
        self.assertNounText_("I ran to you.", ["I", "you"])
        self.assertNounText_("You ran to her.", ["You", "her"])
        self.assertNounText_("She ran to him.", ["She", "him"])
        self.assertNounText_("He ran to me.", ["He", "me"])
        value = "The pretty, little girl played with her extravagant dollhouse that her mother bought the day before."
        expected = ["The pretty, little girl", "her extravagant dollhouse", "her mother", "the day"]
        self.assertNounText_(value, expected) 

    def test_true_negative(self):
        self.assertRaises(TypeError, detect_nouns, 100)
        self.assertRaises(TypeError, detect_nouns, True)
        self.assertRaises(TypeError, detect_nouns, ["I ran to the beach."])
        self.assertRaises(TypeError, detect_nouns, None)
        self.assertRaises(ValueError, detect_nouns, "")
