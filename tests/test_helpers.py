import unittest
from s3bash import helpers


class TestHelpers(unittest.TestCase):

    def test_list_without_empty_elements(self):
        list_with_emtpy_element = [ 'this', 'has', 'an', 'empty', '']
        retrieved_list = helpers.get_list_without_emtpy_elements(list_with_emtpy_element)

        self.assertTrue(len(retrieved_list) == 4)

    def test_has_at_least_one_argument_true(self):
        result = helpers.has_at_least_one_argument(['argument'])

        self.assertTrue(result)

    def test_has_at_least_one_argument_false(self):
        result = helpers.has_at_least_one_argument([])

        self.assertFalse(result)

    def test_retrieve_bucket_and_key_forward_slash(self):
        bucket, key = helpers.retrieve_bucket_and_key('/some-bucket/somefilename')

        self.assertEqual(bucket, 'some-bucket')
        self.assertEqual(key, 'somefilename')

    def test_retrieve_bucket_and_key_no_forward_slash(self):
        bucket, key = helpers.retrieve_bucket_and_key('some-bucket/somefilename')

        self.assertEqual(bucket, 'some-bucket')
        self.assertEqual(key, 'somefilename')

    def test_get_without_forward_slash_one_element(self):
        result = helpers.get_without_leading_forward_slash(['somefile'])

        self.assertTrue(len(result) == 1)
        self.assertEqual(result[0], 'somefile')

    def test_get_without_forward_slash_multiple(self):
        result = helpers.get_without_leading_forward_slash(['', 'somedir', 'somefile'])

        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], 'somedir')
        self.assertEqual(result[1], 'somefile')


if __name__ == '__main__':
    unittest.main()