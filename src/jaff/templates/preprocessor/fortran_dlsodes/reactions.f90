module reactions
    use commons
    contains

    function get_reactions(tgas, crate, av) result(k)
        implicit none
        real*8::k(nreactions)
        real*8,intent(in)::tgas, crate, av

        k = 0d0

        !! PREPROCESS_REACTIONS

        !! PREPROCESS_END

    end function get_reactions

end module reactions