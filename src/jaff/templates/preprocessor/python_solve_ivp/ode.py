import numpy as np
from commons import *
from fluxes import get_fluxes


def get_ode(y, tgas, crate, av):
    dy = np.zeros_like(y)

    flux = get_fluxes(y, tgas, crate, av)

    # PREPROCESS_ODE

    # PREPROCESS_END

    return dy
