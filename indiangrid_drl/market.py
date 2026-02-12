import numpy as np

# Core objects (from my design)

class Bus:
    def __init__(self, bus_id):
        self.id = bus_id
        self.generators = []
        self.loads = []

class Generator:
    def __init__(self, gen_id, bus, a, b, p_min, p_max):
        self.id = gen_id
        self.bus = bus
        self.a = a          # true cost coefficient
        self.b = b
        self.p_max = p_max
        self.p_min = p_min

        # reported (bid) parameters (truthful for MCP baseline)
        self.a_reported = a
        self.b_reported = b

        self.dispatch = 0.0
        self.profit = 0.0

    def marginal_cost(self, p, reported=True):
        if reported:
            return self.a_reported + 2 * self.b_reported * p
        else:
            return self.a + 2 * self.b * p
        
    def total_cost(self, p):
        return self.a * p + self.b * p**2
    
class Load:
    def __init__(self, load_id, bus, demand):
        self.id = load_id
        self.bus = bus
        self.demand = demand

class Market:
    def __init__(self, buses, generators, loads):
        self.buses = buses
        self.generators = generators
        self.loads = loads
        self.mcp = None  # Market Clearing Price

    def clear_mcp_market(self):
        """
        Copper plate market:
        - Uniform price for all generators
        - No network constraints
        """

        total_demand = sum(load.demand for load in self.loads)

        # Build supply offers:
        # For MCP we sort generators by marginal cost at p_min
        offers =[]
        for gen in self.generators:
            mc_at_min = gen.marginal_cost(gen.p_min, reported=True)
            offers.append((mc_at_min, gen))

        offers.sort(key=lambda x: x[0])  # cheapest first

        remaining_demand = total_demand
        self.mcp = None

        for mc, gen in offers:
            if remaining_demand <= 0:
                gen.dispatch = 0.0
                continue

            supply = min(gen.p_max, remaining_demand)
            gen.dispatch = supply
            gen.profit = gen.total_cost(supply)
            remaining_demand -= supply

            # The last generator that meets demand sets MCP
            self.mcp = gen.marginal_cost(gen.dispatch, reported=True)

        # Pay all generators at MCP
        for gen in self.generators:
            gen.profit = self.mcp * gen.dispatch - gen.total_cost(gen.dispatch)

        return self.mcp
    
    def clear_lmp_market(self, lines):
        """
        Very simplified LMP market:
        - Network-aware
        - Line congestion creates price separation
        """
        # 1. Total demand per bus
        bus_demand = {bus.id: 0.0 for bus in self.buses}
        for load in self.loads:
            bus_demand[load.bus.id] += load.demand

        # 2. Initialize dispatch
        for gen in self.generators:
            gen.dispatch = 0.0

        # 3. Sort generators by reported marginal cost
        gens_sorted = sorted(
            self.generators,
            key=lambda g: g.marginal_cost(g.p_min, reported=True)
        )

        # 4. Dispatch ignoring network first
        total_demand = sum(bus_demand.values())
        remaining_demand = total_demand

        for gen in gens_sorted:
            if remaining_demand <= 0:
                break
            supply = min(gen.p_max, remaining_demand)
            gen.dispatch = supply
            remaining_demand -= supply

        # 5. Compute naive flows (single-path assumption)
        # For now: we assume power flows from lowest-cost generator buses
        self.lmp = {}

        # Base price = marginal cost of last dispatched generator
        last_gen = max(gens_sorted, key=lambda g: g.dispatch)
        base_price = last_gen.marginal_cost(last_gen.dispatch, reported=True)

        # 6. Apply congestion logic
        for bus in self.buses:
            self.lmp[bus.id] = base_price

        for line in lines:
            # Simple congestion check
            line.flow = sum(
                gen.dispatch for gen in self.generators
                if gen.bus.id == line.from_bus.id
            )

            if line.flow > line.capacity:
                congestion_penalty = 10.0
                self.lmp[line.to_bus.id] += congestion_penalty

        # 7. Compute profits
        for gen in self.generators:
            revenue = self.lmp[gen.bus.id] * gen.dispatch
            cost = gen.total_cost(gen.dispatch)
            gen.profit = revenue - cost

        return self.lmp

    
class Line:
    def __init__(self, from_bus, to_bus, capacity):
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.capacity = capacity
        self.flow = 0.0