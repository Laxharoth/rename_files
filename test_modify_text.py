from Classes.modify_text import (
    get_text_generators,
    generator_identity,
    generator_counter,
    generate_text,
)

import unittest


class TestGetTestGenerator(unittest.TestCase):

    def test_NoWildcard(self):
        pattern = "asdfghjklñ"
        statics, generators = get_text_generators(pattern)
        self.assertEqual(len(statics), 1)
        self.assertEqual(len(generators), 0)
        self.assertEqual(statics[0], "asdfghjklñ")

    def test_1IdentityWildcard(self):
        pattern_begining = "*asdfghjklñ"
        statics, generators = get_text_generators(pattern_begining)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "")
        self.assertEqual(statics[1], "asdfghjklñ")
        self.assertEqual(generators[0], generator_identity)
        pattern_middle = "asdfg*hjklñ"
        statics, generators = get_text_generators(pattern_middle)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "asdfg")
        self.assertEqual(statics[1], "hjklñ")
        self.assertEqual(generators[0], generator_identity)
        pattern_end = "asdfghjklñ*"
        statics, generators = get_text_generators(pattern_end)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "asdfghjklñ")
        self.assertEqual(statics[1], "")
        self.assertEqual(generators[0], generator_identity)

    def test_1CounterWildcard(self):
        pattern_begining = "{1:4}asdfghjklñ"
        statics, generators = get_text_generators(pattern_begining)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "")
        self.assertEqual(statics[1], "asdfghjklñ")
        self.assertIsInstance(generators[0], generator_counter)
        self.assertEqual(generators[0].value, -3)
        self.assertEqual(generators[0].increase, 4)
        pattern_middle = "asdfg{4:7}hjklñ"
        statics, generators = get_text_generators(pattern_middle)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "asdfg")
        self.assertEqual(statics[1], "hjklñ")
        self.assertIsInstance(generators[0], generator_counter)
        self.assertEqual(generators[0].value, -3)
        self.assertEqual(generators[0].increase, 7)
        pattern_end = "asdfghjklñ{6:9}"
        statics, generators = get_text_generators(pattern_end)
        self.assertEqual(len(statics), 2)
        self.assertEqual(len(generators), 1)
        self.assertEqual(statics[0], "asdfghjklñ")
        self.assertEqual(statics[1], "")
        self.assertIsInstance(generators[0], generator_counter)
        self.assertEqual(generators[0].value, -3)
        self.assertEqual(generators[0].increase, 9)

    def test_CombinedWildcards(self):
        pattern = "*asd*fgh{1:1}jk{1:1}lñ*"
        statics, generators = get_text_generators(pattern)
        expected_statics = ["", "asd", "fgh", "jk", "lñ", ""]
        expected_generators = [
            generator_identity,
            generator_identity,
            generator_counter,
            generator_counter,
            generator_identity,
        ]
        self.assertListEqual(statics, expected_statics)
        self.assertEqual(len(generators), len(expected_generators))
        for actual, expected in zip(generators, expected_generators):
            if expected == generator_identity:
                self.assertEqual(actual, expected)
            else:
                self.assertIsInstance(actual, expected)


class TestGenerateTest(unittest.TestCase):

    def test_NoWildcard(self):
        statics = ["asdfg"]
        generators = []
        # does not match
        original = "qwert"
        replaceinto = "ñlkkj"
        expected_result = "qwert"
        result = generate_text(original, replaceinto, statics, generators)
        
        self.assertEqual(result, expected_result)
        # matches
        original = "asdfg"
        replaceinto = "ñlkkj"
        expected_result = "ñlkkj"

        result = generate_text(original, replaceinto, statics, generators)
        
        self.assertEqual(result, expected_result)

    def test_IdentityWildcard(self):
        statics = ["asdfg", "ñlkjh"]
        generators = [generator_identity]
        
        # does not match
        original = "asdfgñlkj"
        replaceinto = "qwert $0 asdfg"
        expected_result = "asdfgñlkj"
        result = generate_text(original, replaceinto, statics, generators)
        self.assertEqual(result, expected_result)
        
        # matches
        original = "asdfgLOREMñlkjh"
        replaceinto = "qwert $0 asdfg"
        expected_result = "qwert LOREM asdfg"
        result = generate_text(original, replaceinto, statics, generators)
        
        self.assertEqual(result, expected_result)
    
    def test_CounterWildcard(self):
        statics = ["asdfg", "ñlkjh"]
        generators = [generator_counter(1, 5)]
        
        # matches
        original = "asdfgLOREMñlkjh"
        replaceinto = "qwert $0 asdfg"
        expected_result = "qwert 1 asdfg"
        # check it replaces with the counter (and counter didn't increased on fail match)
        result = generate_text(original, replaceinto, statics, generators)
        self.assertEqual(result, expected_result)
        
        # does not match
        original = "asdfgñlkj"
        replaceinto = "qwert $0 asdfg"
        expected_result = "asdfgñlkj"
        result = generate_text(original, replaceinto, statics, generators)
        self.assertEqual(result, expected_result)
        
        # matches
        # check counter increases correctly with the counter
        expected_result = "qwert 6 asdfg"
        result = generate_text(original, replaceinto, statics, generators)
        
    def test_MixedWildcard(self):
        statics = ["", "asd", "fgh", "jk", "lñ", ""]
        generators = [
            generator_identity,
            generator_identity,
            generator_counter,
            generator_counter,
            generator_identity,
        ]
        
        original_values = ""
        replace_pattern = ""
        expected_values = []

if __name__ == "__main__":
    unittest.main()
