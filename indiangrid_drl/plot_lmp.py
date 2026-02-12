import matplotlib.pyplot as plt
from market import Bus, Generator, Load, Market, Line

b1 = Bus(1)
b2 = Bus(2)

g1 = Generator(1, b1, a=10, b=0.01, p_min=0, p_max=100)
g2 = Generator(2, b2, a=30, b=0.02, p_min=0, p_max=100)

load = Load(1, b2, demand=120)

line = Line(from_bus=b1, to_bus=b2, capacity=50)

market = Market(
    buses=[b1, b2],
    generators=[g1, g2],
    loads=[load]
)

lmp = market.clear_lmp_market(lines=[line])

bus_ids = list(lmp.keys())
prices = list(lmp.values())

plt.figure()
plt.bar(bus_ids, prices, color=['blue', 'orange'])
plt.xlabel('Bus ID')
plt.ylabel('LMP')
plt.title('Locational Marginal Prices')
plt.show()

gen_ids = [gen.id for gen in market.generators]
dispatches = [gen.dispatch for gen in market.generators]

plt.figure()
plt.bar(gen_ids, dispatches, color='green')
plt.xlabel('Generator ID')
plt.ylabel('Dispatch (MW)')
plt.title('Generator Dispatch')
plt.show()