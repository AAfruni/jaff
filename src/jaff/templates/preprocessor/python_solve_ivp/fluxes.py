import numpy as np
from commons import *
from rates import get_rates


def get_fluxes(y, tgas, crate, av):
    k = get_rates(tgas, crate, av)

    flux = np.zeros_like(y)

    # PREPROCESS_FLUXES

    # PREPROCESS_END

    return flux
