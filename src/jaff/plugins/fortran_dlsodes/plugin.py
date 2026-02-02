import os


def main(network, path_template, path_build=None):
    from jaff.preprocessor import Preprocessor

    p = Preprocessor()

    scommons = network.get_commons(idx_offset=1, definition_prefix="integer,parameter::")
    rates = network.get_rates(language="f90")
    sflux = network.get_fluxes(language="f90")
    sode = network.get_ode(derivative_variable="dn", language="f90")

    p.preprocess(
        path_template,
        ["commons.f90", "ode.f90", "fluxes.f90", "reactions.f90"],
        [{"COMMONS": scommons}, {"ODE": sode}, {"FLUXES": sflux}, {"REACTIONS": rates}],
        comment="!!",
        path_build=path_build,
    )
