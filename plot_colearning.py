import os
import matplotlib.pyplot as plt
from vre_learning import run_vre_colearning

CAPACITY_LABEL = "medium_flip"

SAVE_DIR = f"plots/{CAPACITY_LABEL}"
os.makedirs(SAVE_DIR, exist_ok=True)

history = run_vre_colearning(
    n_days=60,
    temperature=1.0
)

days = history["day"]

# Plot 1: Actions (Bid Multipliers)
plt.figure(figsize=(12, 8))
plt.plot(days, history["action_g0"], label="Generator 0 Action", marker='o')
plt.plot(days, history["action_g1"], label="Generator 1 Action", marker='o')
plt.xlabel("Day")
plt.ylabel("Bid Multiplier")
plt.title("Co-learning Agents' Actions Over Time")
plt.legend()
plt.grid(True)

plt.savefig(f"{SAVE_DIR}/bids_vs_time.png", dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Profits
plt.figure(figsize=(12, 8))
plt.plot(days, history["profit_g0"], label="Generator 0 Profit", marker='o')
plt.plot(days, history["profit_g1"], label="Generator 1 Profit", marker='o')
plt.xlabel("Day")
plt.ylabel("Profit")
plt.title("Co-learning Agents' Profits Over Time")
plt.legend()
plt.grid(True)

plt.savefig(f"{SAVE_DIR}/profits_vs_time.png", dpi=300, bbox_inches='tight')
plt.close()

# Plot 3: Locational Marginal Prices (LMPs)
plt.figure(figsize=(12, 8))
plt.plot(days, history["lmp_bus1"], label="Bus 1 LMP", marker='o')
plt.plot(days, history["lmp_bus2"], label="Bus 2 LMP", marker='o')
plt.xlabel("Day")
plt.ylabel("LMP")
plt.title("Co-learning Agents' LMPs Over Time")
plt.legend()
plt.grid(True)

plt.savefig(f"{SAVE_DIR}/lmps_vs_time.png", dpi=300, bbox_inches='tight')
plt.close()

print("Plots saved successfully!")