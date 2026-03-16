import pandapower as pp
import pandapower.networks as pn

# Empty network

net = pp.create_empty_network()

bus1 = pp.create_bus(net, vn_kv=110, name="Bus 1")
bus2 = pp.create_bus(net, vn_kv=110, name="Bus 2")

pp.create_line_from_parameters(
    net,
    from_bus=bus1,
    to_bus=bus2,
    length_km=1,
    r_ohm_per_km=0.01,
    x_ohm_per_km=0.1,
    c_nf_per_km=0,
    max_i_ka=0.2, # current limit
    max_loading_percent=100 # makes it binding
)

pp.create_gen(net,
                bus=bus1,
                p_mw=0,
                min_p_mw=0,
                max_p_mw=100,
                vm_pu=1.0,
                controllable=True,
                slack=True) # modified later due to error

pp.create_gen(net,
                bus=bus2,
                p_mw=0,
                min_p_mw=0,
                max_p_mw=100,
                vm_pu=1.0,
                controllable=True)

# Genrerator cost data (linear cost function)

pp.create_poly_cost(net, element=0, et='gen', cp1_eur_per_mw=10)
pp.create_poly_cost(net, element=1, et='gen', cp1_eur_per_mw=30)

pp.create_load(net, bus=bus2, p_mw=120,
               controllable=False) # another error fix

pp.rundcopp(net)

print("Generator dispatch (MW):")
print(net.res_gen[["p_mw"]])

print("\nBus LMPs:")
print(net.res_bus[["lam_p"]])

print("\nLine loading:")
print(net.res_line[["loading_percent"]])