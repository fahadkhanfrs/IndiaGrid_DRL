from market_ieee5 import MarketIEEE5

market = MarketIEEE5(line_capacity=0.4)

market.build_network({
    0: 1.0,
    1: 1.0
})

dispatch, lmps, profits = market.run()

print("Generator Dispatch (MW):", dispatch)
print("Bus LMPs (EUR/MWh):", lmps)
print("Generator Profits (EUR):", profits)