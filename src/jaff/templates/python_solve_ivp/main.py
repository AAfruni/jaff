from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from commons import nvars, idx_CO, idx_COj, idx_tgas
from ode import get_ode


def f(_, y, crate, av):
    tgas = y[idx_tgas]
    return get_ode(y, tgas, crate, av)


y0 = np.zeros(nvars)
y0[idx_CO] = 1e2

y0[idx_tgas] = 1e2  # Initial temperature in Kelvin

seconds_per_year = 365.0 * 24 * 3600  # seconds in a year
teval = np.logspace(2, 6, 100) * seconds_per_year

sol = solve_ivp(f, (0, teval[-1]), y0, t_eval=teval, args=(1e-17, 1e0))

if not sol.success:
    raise RuntimeError("ODE solver failed: " + sol.message)

plt.plot(sol.t / seconds_per_year, sol.y[idx_CO], label="CO")
plt.plot(sol.t / seconds_per_year, sol.y[idx_COj], label="CO+")
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()
