import unittest
from test.tests import SearchAlgorithmTests
from ui.GUI import GUI

# Create an instance of the test class and execute the test methods
test_suite = unittest.TestLoader().loadTestsFromTestCase(SearchAlgorithmTests)
unittest.TextTestRunner(verbosity=2).run(test_suite)

# Starts the interactive user interface
GUI().run()


