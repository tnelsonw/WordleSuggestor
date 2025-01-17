import unittest
import unittest.mock
import sys
import os
import io
import suggestor

# getting the name of the directory
# where this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)


class TestSuggestor(unittest.TestCase):

    suggestor = None

    @classmethod
    def setUpClass(cls):
        cls.suggestor = suggestor.Wordle_Suggestor()

    def test_load_dictionary(self):
        self.assertEqual(["bloat", "empty", "yours"], self.suggestor.load_dictionary(5))
        self.assertEqual([], self.suggestor.load_dictionary(6))

    def test_get_init_suggestion(self):
        self.assertIn(self.suggestor.get_init_suggestion(5), suggestor.init_suggestions5)
        self.assertIn(self.suggestor.get_init_suggestion(6), suggestor.init_suggestions6)

    def test_check_duplicate(self):
        self.assertTrue(self.suggestor.check_duplicate("steel"))
        self.assertTrue(self.suggestor.check_duplicate("eerie"))
        self.assertFalse(self.suggestor.check_duplicate("false"))
        self.assertFalse(self.suggestor.check_duplicate("faces"))
        self.assertTrue(self.suggestor.check_duplicate("gamma"))

    # The following 2 unit tests are now obsolete since this program now uses a GUI
    # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    # def assert_stdout(self, guess, expected_output, mock_stdout):
    #     suggestor.print_init_guess(guess)
    #     self.assertEqual(mock_stdout.getvalue(), expected_output)

    # def test_print_init_guess(self):
    #     expected = "Try this word for your initial guess: words\nType '1' to continue. Or, for a different initial "\
    #                "suggestion, type '2'.\n"
    #     self.assert_stdout("words", expected)

    def test_load_input5(self):
        with unittest.mock.patch('sys.stdin', io.StringIO('i\ng\nr\ng\na\ng\nt\ng\ne\ng\n')), \
                unittest.mock.patch('sys.stdout', new_callable=io.StringIO):
            expected = {0: ['g', 'i'], 1: ['g', 'r'], 2: ['g', 'a'], 3: ['g', 't'], 4: ['g', 'e']}
            loaded_input = self.suggestor.load_input(suggestor.init_suggestions5, 5)
            self.assertEqual(loaded_input, expected)

    def test_load_input6(self):
        with unittest.mock.patch('sys.stdin', io.StringIO('s\ng\na\ng\nt\ng\ni\ng\nr\ng\ne\ng\n')), \
                unittest.mock.patch('sys.stdout', new_callable=io.StringIO):
            expected = {0: ['g', 's'], 1: ['g', 'a'], 2: ['g', 't'], 3: ['g', 'i'], 4: ['g', 'r'], 5: ['g', 'e']}
            loaded_input = self.suggestor.load_input(suggestor.init_suggestions6, 6)
            self.assertEqual(loaded_input, expected)

    def test_suggest_word(self):
        confirmed = {0: 'i', 1: 'r', 2: 'a', 3: 't', 4: 'e'}
        words = self.suggestor.suggest_word({}, confirmed, {}, suggestor.init_suggestions5.copy())
        self.assertEqual(words, ["irate"])

        confirmed = {0: 'r'}
        blank = {1: 'u', 2: 'm', 3: 'p', 4: 'y'}
        words = self.suggestor.suggest_word({}, confirmed, blank, suggestor.init_suggestions5.copy())
        self.assertEqual(words, ["reach", "raise"])

        confirmed = {2: 'i', 3: 's', 4: 'e'}
        find = {0: 'a', 1: 'r'}
        words = self.suggestor.suggest_word(find, confirmed, {}, suggestor.init_suggestions5.copy())
        self.assertEqual(words, ["raise"])

        # test double letters
        confirmed = {0: 'g', 1: 'a', 2: 'm'}
        blank = {3: 'e', 4: 's'}
        remaining_words = suggestor.init_suggestions5 + ["gamma", "games"]
        words = self.suggestor.suggest_word({}, confirmed, blank, remaining_words)
        self.assertEqual(words, ["gamma"])

    def test_calculate_values(self):
        w = self.suggestor.calculate_values(suggestor.init_suggestions5, [0, 1, 2, 3],
                                            {0: 'i', 1: 'r', 2: 'a'}, {4: 'e'})
        self.assertEqual(w, ['raise'])
        words = self.suggestor.suggest_word({2: 'n'}, {0: 's', 1: 'o'}, {3: 'a', 4: 'r'},
                                            suggestor.init_suggestions5.copy())
        w = self.suggestor.calculate_values(words, [2, 3, 4], {2: 'n'},
                                            {0: 's', 1: '0'})
        self.assertEqual(w, ['sound'])

    def test_find_rand_suggestion(self):
        self.assertIn(self.suggestor.find_rand_suggestion(suggestor.init_suggestions5), suggestor.init_suggestions5)
        example_list = ['sound', 'meats', 'below']
        self.assertIn(self.suggestor.find_rand_suggestion(example_list), example_list)


if __name__ == '__main__':
    # system('mypy --disallow-untyped-defs suggestor.py')
    unittest.main()
