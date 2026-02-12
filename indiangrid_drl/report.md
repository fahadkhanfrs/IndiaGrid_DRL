Sensitivity Analysis: Impact of Transmission Capacity on Strategic Learning

To examine the robustness of the learning outcomes and to isolate the role of network constraints, a sensitivity analysis was conducted by systematically varying the transmission line capacity between the two buses. The learning algorithm, action space, and market-clearing mechanism were held fixed across all experiments. Only the line capacity was altered to explore different congestion regimes.

Experimental Setup

Three transmission capacity regimes were considered:

Low capacity (strong congestion)

Medium capacity (moderate congestion)

High capacity (weak or no congestion)

For each regime, both generators employed Variant Roth–Erev learning to adaptively select bid multipliers over repeated market sessions. The resulting bid trajectories, profits, and locational marginal prices (LMPs) were recorded and analyzed.

Low Capacity Regime: Strong Congestion

Under low transmission capacity, the network exhibits persistent congestion, leading to strong locational price separation. In this regime, learning converges to an asymmetric equilibrium. One generator consistently adopts a higher bid multiplier and captures substantial congestion rents, while the other settles at a lower bid as a best response.

This outcome reflects locational market power induced by network constraints. The learning dynamics stabilize quickly, and no persistent cycling is observed. The results indicate that when congestion is severe, structural position in the network dominates strategic outcomes, even under symmetric learning rules.

Medium Capacity Regime: Moderate Congestion

When transmission capacity is increased, congestion effects are partially alleviated but not eliminated. In this regime, asymmetric behavior persists, although the disparity in profits between the two generators is reduced. The disadvantaged generator captures a larger share of surplus relative to the low-capacity case, while the dominant generator retains pricing power.

The persistence of asymmetry under moderate congestion demonstrates that strategic dominance is robust to partial relaxation of network constraints. However, the faster convergence and reduced rent gap suggest a gradual redistribution of market power as the transmission bottleneck weakens.

High Capacity Regime: Weak or No Congestion

At high transmission capacity, congestion is effectively removed, resulting in uniform prices across buses. In this regime, the learning dynamics qualitatively change. Both generators learn to inflate bids simultaneously, leading to high uniform LMPs and sustained profits for both participants.

This behavior corresponds to tacit collusion in a uniform-price market. Since bid increases by either generator raise the market-clearing price for all, mutual incentives emerge to maintain elevated bids. The learning process converges to a symmetric, high-price equilibrium without explicit coordination.

Summary of Sensitivity Results

The sensitivity analysis reveals a clear relationship between transmission capacity and strategic learning outcomes:

Strong congestion leads to asymmetric equilibria driven by locational advantages.

Moderate congestion preserves asymmetry but weakens dominance.

Weak or absent congestion shifts market power from locational to system-wide, enabling tacit collusion.

These results demonstrate that the confirmatory learning behavior observed in the model is not an artifact of algorithmic design but is fundamentally shaped by network structure. Transmission constraints play a decisive role in determining whether market power manifests as locational dominance or coordinated price elevation.

Key Insight

Strategic outcomes in learning-based electricity markets are governed more by network structure than by the specific learning algorithm. As congestion is relaxed, market power transitions from nodal dominance to system-wide collusion.

### Sensitivity Analysis: Generator Location

To isolate the role of network position, generator locations were swapped while keeping costs, capacities, and learning parameters unchanged. Under stochastic demand, the identity of the dominant generator reversed relative to the baseline case. The generator relocated to the structurally pivotal bus consistently captured large scarcity rents during high-demand realizations, while the other generator frequently earned zero profit.

The resulting price dynamics exhibited regime switching between low-price competitive outcomes and high-price scarcity events. These findings confirm that market dominance arises from network position rather than intrinsic agent characteristics, and that learning mechanisms adapt to, rather than mitigate, structural asymmetries in the transmission network.

## Conclusion

This study investigated strategic bidding behavior in a simplified electricity market using agent-based learning and DC optimal power flow. By progressively introducing learning, co-learning, transmission constraints, stochastic demand, and structural perturbations, the analysis demonstrates that market outcomes are primarily governed by network structure rather than the specific learning algorithm.

Under strong transmission constraints, learning converges to asymmetric equilibria characterized by locational dominance. As constraints are relaxed, market power shifts toward system-wide tacit collusion with uniform prices. Introducing stochastic demand increases profit volatility but does not fundamentally alter strategic equilibria. Swapping generator locations reverses dominance, confirming that pricing power arises from network position rather than agent identity.

Overall, the results highlight that learning mechanisms adapt to structural incentives embedded in electricity markets and amplify, rather than neutralize, existing sources of market power.

