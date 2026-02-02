#ifndef actual_rhs_H
#define actual_rhs_H

#include <AMReX_REAL.H>
#include <AMReX_Array.H>

#include <extern_parameters.H>
#include <actual_network.H>
#include <burn_type.H>
#include <jacobian_utilities.H>
#include <extern_parameters.H>

using namespace amrex;
using namespace ArrayUtil;
using namespace network_rp;



AMREX_GPU_HOST_DEVICE AMREX_INLINE
void rhs_specie(const burn_t& state,
             Array1D<Real, 1, neqs>& ydot,
             const Array1D<Real, 0, NumSpec-1>& X,
             Real const crate, Real const av,
             Real const d2g, Real const chi,
             Real const Tdust) {

    using namespace Rates;

    // PREPROCESS_TEMP_VARS
    // PREPROCESS_END

    // PREPROCESS_ODE
    // PREPROCESS_END


}


AMREX_GPU_HOST_DEVICE AMREX_INLINE
Real rhs_eint(const burn_t& state,
             const Array1D<Real, 0, NumSpec-1>& X,
             Real const crate, Real const av,
             Real const d2g, Real const chi) 
             {

    using namespace Rates;
    
    // PREPROCESS_TEMP_VARS
    // PREPROCESS_END
    
    // PREPROCESS_DEDT
    // PREPROCESS_END
    
}


AMREX_GPU_HOST_DEVICE AMREX_INLINE
void actual_rhs (burn_t& state, Array1D<Real, 1, neqs>& ydot)
{

    Real crate = network_rp::crate;
    Real av = network_rp::Av;
    Real d2g = network_rp::dust2gas_ratio;
    Real chi = network_rp::chi;
    
    Real Tdust = 10;  //10 Kelvin

    Array1D<Real, 0, NumSpec-1> X;
    for (int i = 0; i < NumSpec; ++i) {
           X(i) = state.xn[i];
    }
    // YDOTS

    rhs_specie(state, ydot, X, crate, av, d2g, chi, Tdust);

    // Edot

    Real edot = rhs_eint(state, X, crate, av, d2g, chi);

    // Append the energy equation (this is erg/g/s)

    ydot(net_ienuc) = edot;

}


template<class MatrixType>
AMREX_GPU_HOST_DEVICE AMREX_INLINE
void jac_nuc(const burn_t& state,
             MatrixType& jac,
             const Array1D<Real, 0, NumSpec-1>& X,
             Real const crate, Real const av,
             Real const d2g, Real const chi,
             Real const Tdust) {
             
    // PREPROCESS_TEMP_VARS
    // PREPROCESS_END

    // PREPROCESS_JACOBIAN
    // PREPROCESS_END

}

template<class MatrixType>
AMREX_GPU_HOST_DEVICE AMREX_INLINE
void actual_jac(const burn_t& state, MatrixType& jac)
{
    Real crate = network_rp::crate;
    Real av = network_rp::Av;
    Real d2g = network_rp::dust2gas_ratio;
    Real chi = network_rp::chi;
    
    Real Tdust = 10;  //10 Kelvin

    Array1D<Real, 0, NumSpec-1> X;
    for (int i = 0; i < NumSpec; ++i) {
        X(i) = state.xn[i];
    }
    // Species Jacobian elements with respect to other species

    jac_nuc(state, jac, X, crate, av, d2g, chi, Tdust);

}


AMREX_INLINE
void actual_rhs_init () {


}


#endif
