import unittest

from kmatch import KmatchTestMixin


class MixinTestUsingMixin(KmatchTestMixin, unittest.TestCase):

    def test_matches(self):
        """
        Test .assertMatches() using the mixin on a true match
        """
        self.assertKmatches(['<=', 'f', 0], {'f': -1})

    def test_matches_raises_error(self):
        """
        Test .assertMatches() using the mixin on a false match
        """
        with self.assertRaises(AssertionError):
            self.assertKmatches(['<=', 'f', 0], {'f': 1})

    def test_not_matches(self):
        """
        Test .assertNotMatches() using the mixin on a false match
        """
        self.assertNotKmatches(['<=', 'f', 0], {'f': 1})

    def test_not_matches_no_key_error(self):
        """
        Test .assertNotMatches() using the mixin on a false match
        """
        self.assertNotKmatches(['<=', 'f', 0], {'g': 1})
        self.assertNotKmatches(['<=', 'f', 0], {'f': 1})

    def test_not_matches_raises_error(self):
        """
        Test .assertNotMatches() using the mixin raises an error on a match
        """
        with self.assertRaises(AssertionError):
            self.assertNotKmatches(['<=', 'f', 0], {'f': -1})
