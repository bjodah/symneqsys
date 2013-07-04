! Template for generating Fortran 90 code to wrapped using Cython for calling nleq2
! from python. Based on main_nleq2.f example provided with NLEQ2
! mako template variables: 

module neqsys
  use types, only: dp
  implicit none
  ! Set problem specific values:
  integer, parameter :: NX = ${NX} ! Number of values (>= NE)
  integer, parameter :: NE = ${NE} ! Number of equations
  integer, parameter :: NP = ${NP} ! Number of parameters

  public solve, NX

contains

  subroutine solve(x, tol, info)
    real(dp), intent(inout) :: x(NX+NP)
    real(dp), intent(in) :: tol ! 
    integer, intent(inout) :: info ! 0 improper input, 1, 2, 3 (success), others error
    integer, parameter :: lwa = 5*NX+NE
    integer :: ipvt(NX), wa(lwa)

    call lmder1(func, m, n, x, f, j, ldj, tol, info, ipvt, wa, lwa)
  end subroutine solve

  subroutine func(m, n, x, f, j, ldj, iflag)
    ! Function
    integer, intent(in) :: m, n, ldj, iflag
    real(dp), intent(in) :: x(NX+NP)
    real(dp), intent(out) :: f(m)
    real(dp), intent(out) :: j(ldj,n)

  % for cse_token, cse_expr in cse_func:
    real(dp) :: ${cse_token}
  % endfor

    if (iflag == 1) then
    % for cse_token, cse_expr in cse_func:
      ${cse_token} = ${cse_expr}
    % endfor

    % for i, expr in enumerate(f, 1):
      f(${i}) = ${expr}
    % endfor
    elseif (iflag == 2) then
    % for cse_token, cse_expr in cse_jac:
      ${cse_token} = ${cse_expr}
    % endfor
  
    % for i, expr in enumerate(jac, 1):
      dfdx(${i}) = ${expr}
    % endfor
    end if
  end subroutine func

end module neqsys

module neqsys_interface
  use iso_c_binding, only: c_double, c_int
  use neqsys, only: solve, NX
  implicit none

contains

  subroutine c_solve(x, tol, info) bind(c)
    real(c_double), intent(inout), dimension(NX) :: x
    real(c_double), intent(inout) :: tol
    real(c_int), intent(inout) :: info
    call perform(x, tol, info)
  end subroutine c_solve
end module neqsys_interface
