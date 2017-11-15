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

    def test_retrieve_bucket_and_key(self):
        bucket, key = helpers.retrieve_bucket_and_key('/some-bucket/somefilename')

        self.assertEqual(bucket, 'some-bucket')
        self.assertEqual(key, 'somefilename')


if __name__ == '__main__':
    unittest.main()