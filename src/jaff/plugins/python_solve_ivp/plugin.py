import os


def main(network, path_template, path_build=None):
    from jaff.preprocessor import Preprocessor

    p = Preprocessor()

    scommons = network.get_commons()
    rates = network.get_rates()
    sflux = network.get_fluxes()
    sode = network.get_ode()

    p.preprocess(
        path_template,
        ["commons.py", "rates.py", "fluxes.py", "ode.py"],
        [{"COMMONS": scommons}, {"RATES": rates}, {"FLUXES": sflux}, {"ODE": sode}],
        comment="#",
        path_build=path_build,
    )
