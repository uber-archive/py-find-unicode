import os.path
import unittest

import py_find_unicode


SAMPLE_PATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), 'sample_file.py'))


class TestSimple(unittest.TestCase):

    def test_sample_file(self):
        errors = py_find_unicode.check(SAMPLE_PATH)
        self.assertEqual(4, len(errors))
        self.assertEqual(errors[0].lineno, 8)
        self.assertEqual(errors[1].lineno, 11)
        self.assertEqual(errors[2].lineno, 20)
        self.assertEqual(errors[3].lineno, 23)


if __name__ == '__main__':
    unittest.main()
