import unittest
import numpy as np
from matplotlib import pyplot as plt
from sir import SIR  # Import the SIR class

class TestSIRPlot(unittest.TestCase):
    def test_plot(self):
        # Create an instance of the SIR class
        sir = SIR()

        # Set the necessary attributes for the SIR instance
        sir.steps = 100
        sir.n = 1000
        sir.beta = 0.2
        sir.gamma = 0.1

        # Call the plot method
        sir.plot()

        # Assert that the plot is displayed without any errors
        self.assertTrue(plt.gcf())

if __name__ == '__main__':
    unittest.main()

    #TODO: SIR Not working, need to fix