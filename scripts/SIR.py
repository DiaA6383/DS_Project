from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


def deriv(y, t, N, beta, gamma):
    """
    Calculate the derivatives of the SIR model.

    Parameters:
    - y (tuple): Tuple containing the current values of S, I, and R.
    - t (float): Current time.
    - N (int): Total population.
    - beta (float): Contact rate.
    - gamma (float): Recovery rate.

    Returns:
    - tuple: Tuple containing the derivatives of S, I, and R.
    """
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


@dataclass
class SIRDiagram:
    """
    Class representing the SIR diagram.

    Attributes:
    - n (int): Total population.
    - i (int): Initial number of infected individuals.
    - r (int): Initial number of recovered individuals.
    - beta (float): Contact rate.
    - gamma (float): Recovery rate.
    - steps (int): Number of simulation steps.

    Methods:
    - s(): Calculate the number of susceptible individuals.
    - plot(): Plot the SIR diagram.
    """
    n: int = 1000
    i: int = 1
    r: int = 0
    beta: float = 0.2
    gamma: float = 1.0 / 10
    steps: int = 160

    def s(self) -> int:
        """
        Calculate the number of susceptible individuals.

        Returns:
        - int: Number of susceptible individuals.
        """
        return self.n - self.i - self.r

    def plot(self):
        """
        Plot the SIR diagram.
        """
        t = np.linspace(0, self.steps, self.steps)
        y0 = self.s(), self.i, self.r
        N, beta, gamma = self.n, self.beta, self.gamma
        ret = odeint(deriv, y0, t, args=(N, beta, gamma))
        S, I, R = ret.T

        fig = plt.figure(facecolor="w")
        ax = fig.add_subplot(111, facecolor="#dddddd", axisbelow=True)
        ax.plot(t, S / 1000, "b", alpha=0.5, lw=2, label="Potential Customer")
        ax.plot(t, I / 1000, "r", alpha=0.5, lw=2, label="Infected")
        ax.plot(t, R / 1000, "g", alpha=0.5, lw=2, label="Non Buyer")

        ax.set_xlabel("Time /days")
        ax.set_ylabel("Number (1000s)")
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(which="major", c="w", lw=2, ls="-")
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ("top", "right", "bottom", "left"):
            ax.spines[spine].set_visible(False)

        plt.title("SIR Infection by Zip Code")
        plt.show()


def main():
    """
    Main function to run the SIR diagram simulation.
    """
    diagram = SIRDiagram()
    diagram.plot()


if __name__ == "__main__":
    main()