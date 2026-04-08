module fluxes
    use commons
    use reactions
    contains

    function get_fluxes(y, tgas, crate, av) result(flux)
        implicit none
        real*8::flux(nreactions)
        real*8,intent(in)::y(nspecs), tgas, crate, av
        real*8::k(nreactions)

        k = get_reactions(tgas, crate, av)

        !! PREPROCESS_FLUXES

        !! PREPROCESS_END

    end function get_fluxes

end module fluxes