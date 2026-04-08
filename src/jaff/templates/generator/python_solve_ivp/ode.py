import numpy as np
from commons import *
from fluxes import get_fluxes


def get_ode(y, tgas, crate, av):
    dy = np.zeros_like(y)

    flux = get_fluxes(y, tgas, crate, av)

    # $JAFF REPEAT idx, ode_expression IN ode_expressions

    dy[$idx$] = $ode_expression$

    # $JAFF END

    return dy
