from market_dcopf import MarketDCOPF

# Truthful bidding
market = MarketDCOPF(line_capacity=0.2) 

market.build_network(reported_cost_multipliers={0: 1.0, 1: 1.0})

dispatch_truthful, lmps_truthful, profits_truthful = market.run()

print("Truthful Bidding:")
print("Generator Dispatch (MW):", dispatch_truthful)
print("Bus LMPs (EUR/MWh):", lmps_truthful)
print("Generator Profits (EUR):", profits_truthful)

# Strategic bidding
market = MarketDCOPF(line_capacity=0.2)

market.build_network(reported_cost_multipliers={
    0: 1.5, # cheap gen inflates bid
    1: 1.0})

dispatch_strategic, lmps_strategic, profits_strategic = market.run()

print("\nStrategic Bidding:")
print("Generator Dispatch (MW):", dispatch_strategic)
print("Bus LMPs (EUR/MWh):", lmps_strategic)
print("Generator Profits (EUR):", profits_strategic)
