import Options

b = Options.BlackScholes2(S=100, K=120, T=2.5, r=.04, sigma=.35)
print(b)

print(b.d1())
print(b.d2())

print(b.call_value())
print(b.put_value())

print(b.delta_call())
print(b.delta_put())

print(b.gamma())
print(b.vega())

print(b.rho_call())
print(b.rho_put())

print(b.theta_call())
print(b.theta_put())