from jaff import Codegen, Network, Preprocessor


def main(network, path_template, path_build=None):
    p = Preprocessor()
    cg = Codegen(network=network, lang="fortran")

    scommons = cg.get_commons(idx_offset=1, definition_prefix="integer,parameter::")
    rates = cg.get_rates_str()
    flux = cg.get_flux_expressions_str()
    sode = cg.get_ode_expressions_str(derivative_var="dn")

    p.preprocess(
        path_template,
        ["commons.f90", "ode.f90", "fluxes.f90", "reactions.f90"],
        [{"COMMONS": scommons}, {"ODE": sode}, {"FLUXES": flux}, {"REACTIONS": rates}],
        comment="!!",
        path_build=path_build,
    )


if __name__ == "__main__":
    net = Network("networks/test.dat")
    main(net, path_template="src/jaff/templates/preprocessor/fortran_dlsodes")
