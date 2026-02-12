import pandapower as pp
import numpy as np

# Demand uncertainty is a market/environment feature, not an agent feature.

class MarketDCOPF:
    def __init__(self, line_capacity):
        self.line_capacity = line_capacity
        self.net = None
        self.gen_costs_true = {}
        self.gen_costs_reported = {}

    def build_network(self, reported_cost_multipliers):
        """
        reported_cost_multipliers: dict mapping generator indices to cost multipliers
        {gen_id: multiplier}
        """

        net = pp.create_empty_network()

        b1 = pp.create_bus(net, vn_kv=110, name="Bus 1")
        b2 = pp.create_bus(net, vn_kv=110, name="Bus 2")

        pp.create_line_from_parameters(
            net,
            from_bus=b1,
            to_bus=b2,
            length_km=1,
            r_ohm_per_km=0.01,
            x_ohm_per_km=0.1,
            c_nf_per_km=0,
            max_i_ka=0.35, # current limit
            max_loading_percent=100 # makes it binding
        )

        pp.create_gen(net,
                        bus=b2,
                        p_mw=0,
                        min_p_mw=0,
                        max_p_mw=100,
                        vm_pu=1.0,
                        controllable=True,
                        slack=True)

        pp.create_gen(net,
                        bus=b1,
                        p_mw=0,
                        min_p_mw=0,
                        max_p_mw=100,
                        vm_pu=1.0,
                        controllable=True)

        self.gen_costs_true = {
            0: 10,  # True cost for gen at bus 1
            1: 30  # True cost for gen at bus 2
        }

        self.gen_costs_reported = {
            i: self.gen_costs_true[i] * reported_cost_multipliers[i]
            for i in self.gen_costs_true
        }

        for gen_id, cost in self.gen_costs_reported.items():
            pp.create_poly_cost(
                net, element=gen_id, et="gen",
                cp1_eur_per_mw=cost
            )
        
        # Adding stochastic load to create demand uncertainty
        base_demand = 100
        noice_level = 0.1

        demand = base_demand * (1 + noice_level * np.random.uniform(-1,1)) # +/-10% noise
        pp.create_load(net, bus=b2,
                       p_mw=demand,
                       controllable=False)

        self.net = net

    def run(self):
        pp.rundcopp(self.net)

        dispatch = self.net.res_gen["p_mw"].values
        lmps = self.net.res_bus["lam_p"].values

        profits = {}
        for i, p in enumerate(dispatch):
            revenue = lmps[self.net.gen.at[i, "bus"]] * p
            cost = self.gen_costs_true[i] * p
            profits[i] = revenue - cost

        return dispatch, lmps, profits