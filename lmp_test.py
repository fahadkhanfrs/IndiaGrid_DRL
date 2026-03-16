from market import Bus, Generator, Load, Market, Line

b1 = Bus(1)
b2 = Bus(2)

g1 = Generator(1, b1, a=10, b=0.01, p_min=0, p_max=100)
g2 = Generator(2, b2, a=20, b=0.02, p_min=0, p_max=100)

# Load at bus 2
load = Load(1, b2, demand=150)

# Line with limited capacity
line = Line(from_bus=b1, to_bus=b2, capacity=50)

market = Market(
    buses=[b1, b2],
    generators=[g1, g2],
    loads=[load]
)

lmp = market.clear_lmp_market(lines=[line])

print(f"Locational Marginal Prices (LMPs): {lmp}")
for gen in market.generators:
    print(f"Generator {gen.id} dispatch: {gen.dispatch}, profit: {gen.profit:.2f}")