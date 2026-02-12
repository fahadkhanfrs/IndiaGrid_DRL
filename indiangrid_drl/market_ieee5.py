import pandapower as pp
import numpy as np

class MarketIEEE5:
    def __init__(self, line_capacity=0.3):
        self.line_capacity = line_capacity
        self.net = None

        # True marginal costs
        self.gen_costs_true = {
            0: 10.0,
            1: 25.0
        }

    def build_network(self, reported_cost_multipliers):

        net = pp.create_empty_network()
        buses = [pp.create_bus(net, vn_kv=110) for _ in range(5)]
        line_capacity = 0.4

        def add_line(f, t):

            pp.create_line_from_parameters(net,
                from_bus=f,
                to_bus=t,
                length_km=1,
                r_ohm_per_km=0.0,
                x_ohm_per_km=0.1,
                c_nf_per_km=0,
                max_i_ka=line_capacity
            )

        add_line(buses[1], buses[2])
        add_line(buses[1], buses[3])
        add_line(buses[2], buses[4])
        add_line(buses[3], buses[4])

        pp.create_line_from_parameters(
            net,
            from_bus=buses[0],
            to_bus=buses[1],
            length_km=1,
            r_ohm_per_km=0.0,
            x_ohm_per_km=0.5,   # higher reactance = weaker corridor
            c_nf_per_km=0,
            max_i_ka=0.4
        )

        # --------------------------
        # Loads (NO randomness for now)
        # --------------------------
        pp.create_load(net, bus=buses[2], p_mw=60, controllable=False)
        pp.create_load(net, bus=buses[3], p_mw=50, controllable=False)
        pp.create_load(net, bus=buses[4], p_mw=40, controllable=False)

        # --------------------------
        # Generators
        # --------------------------
        pp.create_gen(net, bus=buses[0],
                    p_mw=0,
                    min_p_mw=0,
                    max_p_mw=100,
                    slack=True,
                    controllable=True)

        pp.create_gen(net, bus=buses[1],
                    p_mw=0,
                    min_p_mw=0,
                    max_p_mw=150,
                    controllable=True)

        # --------------------------
        # Cost functions
        # --------------------------
        for gen_id in self.gen_costs_true:
            cost = self.gen_costs_true[gen_id] * reported_cost_multipliers[gen_id]
            pp.create_poly_cost(net, element=gen_id, et="gen", cp1_eur_per_mw=cost)

        self.net = net

    def run(self):

        pp.rundcopp(self.net)

        dispatch = self.net.res_gen["p_mw"].values
        lmps = self.net.res_bus["lam_p"].values

        profits = {}
        for i, p in enumerate(dispatch):
            revenue = lmps[self.net.gen.at[i, "bus"]] * p
            true_cost = self.gen_costs_true[i] * p
            profits[i] = revenue - true_cost

        return dispatch, lmps, profits