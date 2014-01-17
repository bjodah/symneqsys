! ${_warning_in_the_generated_file_not_to_edit}
<%doc>
! Template for generating Fortran 90 code to wrapped using Cython for calling nleq2
! from python. Based on main_nleq2.f example provided with NLEQ2
</%doc>

module neqsys
  use types, only: dp
  implicit none
  ! Set problem specific values:
  integer, parameter :: NX = ${NX}

  public solve, NX

contains

  subroutine solve(x, rtol)
    real(dp), intent(inout) :: x(NX)
    real(dp), intent(inout) ::   rtol ! final achieved rtol returned, set to -1.0 if ierr > 0
    real(dp) :: xscal(NX) ! User scaling
    real(dp) :: stime, etime, cptime
    integer :: iopt(50) ! run-time options
    integer :: ierr
    ! Workspace parameters of NLEQ2
    integer, parameter :: liwk = NX+52 ! req. minimum
    integer :: iwk(liwk)
    integer, parameter :: NBROY = 0 ! Broyden steps disabled, if IOPT(32)=1: MAX(NX,10)
    integer, parameter :: lrwk = (NX+NBROY+15)*NX + 61 - NX ! dim of real workspace
    real(dp) :: rwk(lrwk)
    iopt = 0 ! Default values
    iopt(3) = 1 ! JACGEN: User supplied subroutine jac
    rwk = 0  ! Default values

    xscal = 1
    call nleq2(NX, func, jac, x, xscal, rtol, iopt, ierr, liwk, iwk, lrwk, rwk)

    if (ierr > 0) then
       rtol = -ierr 
       ! -10 == insuficient work space
       ! -2 == maximum iterations
       ! -3 == small damping factor
       ! -1 == stationary point, rank deficient jacobian
    end if
  end subroutine solve

  subroutine func(n, x, f, ifail)
    ! Function
    integer, intent(in) :: n
    real(dp), intent(in) :: x(n)
    real(dp), intent(out) :: f(n)
    integer, intent(out) :: ifail ! set to e.g. 1 for more damping, see doc
  % for cse_token, cse_expr in cse_func:
    real(dp) :: ${cse_token}
  % endfor

  % for cse_token, cse_expr in cse_func:
    ${cse_token} = ${cse_expr}
  % endfor

  % for i, expr in enumerate(f, 1):
    f(${i}) = ${expr}
  % endfor
  end subroutine func

  subroutine jac(n, ldjac, x, dfdx, ifail)
    ! Jacobian matrix
    integer, intent(in) :: n
    integer, intent(in) :: ldjac ! leading dimension
    real(dp), intent(in) :: x(n) ! vector of unknowns
    integer, intent(in) :: ifail ! set to negative to terminate nleq2
  % for cse_token, cse_expr in cse_jac:
    real(dp) :: ${cse_token}
  % endfor

  % for cse_token, cse_expr in cse_jac:
    ${cse_token} = ${cse_expr}
  % endfor

  % for i, expr in enumerate(jac, 1):
    dfdx(${i}) = ${expr}
  % endfor
  end subroutine jac


  subroutine zibsec(cptim, ifail)
    real(dp), intent(out) :: cptim
    integer, intent(out) :: ifail
    ifail = 0
    call cpu_time(cptim)
  end subroutine zibsec

  subroutine zibconst(epmach, small)
    real(dp), intent(out) :: epmach = ${np.finfo(np.float64).eps}
    real(dp), intent(out) :: small = ${np.finfo(np.float64).min}
  end subroutine zibconst
end module

module neqsys_interface
  use iso_c_binding, only: c_double, c_int
  use neqsys, only: solve, NX
  implicit none

contains

  subroutine c_solve(x, rtol) bind(c)
    real(c_double), intent(inout), dimension(NX) :: x
    real(c_double), intent(inout) :: rtol
    call perform(x, rtol)
  end subroutine c_solve
end module neqsys_interface
