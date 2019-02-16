import time
import unittest

import numpy as np

class CustomTest(unittest.TestCase):
    def setUp(self):
        self.test_start = time.time()
        # always use the same reandom seed
        # during tests
        print("Test: ", self.id, " started.")

    def tearDown(self):
        print("Test: ", self.id, "took ", time.time() -
              self.test_start, " seconds.")

