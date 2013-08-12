! Template (mako) for generating Fortran 90 code to wrapped.

module neqsys
  use iso_c_binding, only: c_double, c_int
  implicit none
  ! Set problem specific values:
  integer, parameter :: NX = ${NX} ! Number of values (>= NE)
  integer, parameter :: NE = ${NE} ! Number of equations
  integer, parameter :: NP = ${NP} ! Number of parameters
  integer(c_int) :: NFEV, NJEV, NIT
  public lm_solve, func, get_nfev, get_njev

contains

  subroutine lm_solve(x, tol, info) bind(c)
    real(c_double), intent(inout) :: x(NX+NP)
    real(c_double), intent(in) :: tol ! 
    integer(c_int), intent(inout) :: info ! 0 improper input, 1, 2, 3 (success), others error
    integer, parameter :: lwa = 5*NX+NE
    integer :: ipvt(NX), wa(lwa)
    NFEV = 0
    NJEV = 0
    call lmder1(func, m, n, x, f, j, ldj, tol, info, ipvt, wa, lwa)
  end subroutine solve

  subroutine func(m, n, x, f, j, ldj, iflag) bind(c)
    ! Function
    integer(c_int), intent(in) :: m, n, ldj, iflag
    real(c_double), intent(in) :: x(NX+NP)
    real(c_double), intent(out) :: f(m)
    real(c_double), intent(out) :: j(ldj,n)

  % for cse_token, cse_expr in cse_func:
    real(c_double) :: ${cse_token}
  % endfor

    if (iflag == 1) then
      NFEV = NFEV + 1
    % for cse_token, cse_expr in cse_func:
      ${cse_token} = ${cse_expr}
    % endfor
    % for i, expr in enumerate(f, 1):
      f(${i}) = ${expr}
    % endfor
    elseif (iflag == 2) then
      NJEV = NJEV + 1
    % for cse_token, cse_expr in cse_jac:
      ${cse_token} = ${cse_expr}
    % endfor
  
    % for i, expr in enumerate(jac, 1):
      dfdx(${i}) = ${expr}
    % endfor
    end if
  end subroutine func

  subroutine get_nfev(nfev_) bind(c)
    integer(c_int), intent(inout) :: nfev_
    nfev_ = NFEV
  end subroutine

  subroutine get_njev(njev_) bind(c)
    integer(c_int), intent(inout) :: njev_
    njev_ = NJEV
  end subroutine

end module neqsys

! module neqsys_interface
!   use neqsys, only: solve, NX
!   implicit none

! contains

!   subroutine c_solve(x, tol, info) bind(c)
!     real(c_double), intent(inout), dimension(NX) :: x
!     real(c_double), intent(inout) :: tol
!     real(c_int), intent(inout) :: info
!     call perform(x, tol, info)
!   end subroutine c_solve
! end module neqsys_interface
