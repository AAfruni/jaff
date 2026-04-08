module ode
    use commons
    use fluxes
    contains

    subroutine fex(t, dn, n)
        implicit none
        real*8::t
        real*8::n(nspecs+1), y(nspecs)
        real*8::dn(nspecs+1), tgas, flux(nreactions)

        y = n(1:nspecs)
        tgas = n(idx_tgas)

        flux = get_fluxes(y, tgas, common_crate, common_av)

        !! PREPROCESS_ODE

        !! PREPROCESS_END

    end subroutine fex

end module
