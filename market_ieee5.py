import pandapower as pp
import numpy as np


class MarketIEEE5:

    def __init__(self, line_capacity=20, demand_noise=0.1):
        self.line_capacity = line_capacity
        self.demand_noise = demand_noise

        # generator true costs
        self.true_costs = {
            0: 10.0,
            1: 30.0
        }

    def build_network(self, reported_cost_multipliers):

        net = pp.create_empty_network()

        # -------------------------
        # Create buses
        # -------------------------
        buses = [pp.create_bus(net, vn_kv=110) for _ in range(5)]

        b1, b2, b3, b4, b5 = buses

        # -------------------------
        # Generators
        # -------------------------
        pp.create_gen(
            net,
            bus=b1,
            p_mw=0,
            min_p_mw=0,
            max_p_mw=100,
            slack=True
        )

        pp.create_gen(
            net,
            bus=b2,
            p_mw=0,
            min_p_mw=0,
            max_p_mw=100
        )

        # -------------------------
        # Generator cost functions
        # -------------------------
        bid_cost_0 = self.true_costs[0] * reported_cost_multipliers[0]
        bid_cost_1 = self.true_costs[1] * reported_cost_multipliers[1]

        pp.create_poly_cost(net, 0, 'gen', cp1_eur_per_mw=bid_cost_0)
        pp.create_poly_cost(net, 1, 'gen', cp1_eur_per_mw=bid_cost_1)

        # -------------------------
        # Stochastic demand
        # -------------------------
        base_load_1 = 60
        base_load_2 = 40

        d1 = base_load_1 * (1 + self.demand_noise * np.random.uniform(-1, 1))
        d2 = base_load_2 * (1 + self.demand_noise * np.random.uniform(-1, 1))

        pp.create_load(net, bus=b3, p_mw=d1, controllable=False)
        pp.create_load(net, bus=b4, p_mw=d2, controllable=False)

        # -------------------------
        # Transmission lines
        # -------------------------
        def add_line(f, t):
            pp.create_line_from_parameters(
                net,
                from_bus=f,
                to_bus=t,
                length_km=10,
                r_ohm_per_km=0.01,
                x_ohm_per_km=0.05,
                c_nf_per_km=0,
                max_i_ka=self.line_capacity
            )

        add_line(b1, b2)
        add_line(b1, b3)
        add_line(b2, b4)
        add_line(b3, b4)
        add_line(b3, b5)

        return net

    def run(self, reported_cost_multipliers):

        net = self.build_network(reported_cost_multipliers)

        pp.rundcopp(net)

        dispatch = net.res_gen["p_mw"].values
        lmps = net.res_bus["lam_p"].values

        profits = {}

        for g in range(len(dispatch)):
            gen_bus = net.gen.bus[g]
            price = lmps[gen_bus]

            true_cost = self.true_costs[g]
            q = dispatch[g]

            profits[g] = (price - true_cost) * q

        return dispatch, lmps, profits
    
line_capacity = 20

market = MarketIEEE5(line_capacity=line_capacity)

dispatch, lmps, profits = market.run({
    0: 1.0,
    1: 1.0
})

print("Dispatch:", dispatch)
print("LMPs:", lmps)
print("Profits:", profits)