import unittest
from afdata.kmeans import kmeans

class Kmeans(unittest.TestCase):
    def test_throws_exception_when_no_k_given(self):
        with self.assertRaisesRegex(ValueError, 'Number of clusters, k, must be specified'):
            kmeans()

if __name__ == '__main__':
    unittest.main()
