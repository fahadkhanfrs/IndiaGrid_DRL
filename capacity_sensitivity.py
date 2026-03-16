import numpy as np
import matplotlib.pyplot as plt

from vre_learning import run_vre_colearning
from market_ieee5 import MarketIEEE5


capacities = [10, 15, 20, 25, 30, 40, 50, 60, 80,100]

final_action_g0 = []
final_action_g1 = []


for cap in capacities:

    print(f"\nRunning capacity = {cap}")

    history = run_vre_colearning(
        n_days=60,
        line_capacity=cap
    )

    final_action_g0.append(history["action_g0"][-1])
    final_action_g1.append(history["action_g1"][-1])


plt.figure()

plt.plot(capacities, final_action_g0, marker='o', label="Generator 0 strategy")
plt.plot(capacities, final_action_g1, marker='o', label="Generator 1 strategy")

plt.xlabel("Transmission Capacity")
plt.ylabel("Learned Bid Multiplier")
plt.title("Market Equilibrium vs Transmission Capacity")

plt.legend()
plt.grid(True)

plt.savefig("equilibrium_vs_capacity.png", dpi=300)

plt.show()

print("\nPlot saved as equilibrium_vs_capacity.png")