from market import Bus, Generator, Load, Market

# Copper plate

bus = Bus(1)

# Generators
gen1 = Generator(gen_id=1, bus=bus, a=10, b=0.01, p_min=0, p_max=100)
gen2 = Generator(gen_id=2, bus=bus, a=20, b=0.02, p_min=0, p_max=100)
gen3 = Generator(gen_id=3, bus=bus, a=15, b=0.015, p_min=0, p_max=100)

generators = [gen1, gen2, gen3]

# Load
load = Load(load_id=1, bus=bus, demand=250)
loads = [load]

# Market
market = Market(buses=[bus], generators=generators, loads=loads)

# Clear the market
mcp = market.clear_mcp_market()

print(f"Market Clearing Price (MCP): {mcp}")
for gen in generators:
    print(f"Generator {gen.id} dispatch: {gen.dispatch}, profit: {gen.profit:.2f}")