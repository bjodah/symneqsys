! Template for generating Fortran 90 code to wrapped using Cython for calling nleq2
! from python. Based on main_nleq2.f example provided with NLEQ2
! mako template variables: 

module neqsys
use types, only: dp
implicit none
! Set problem specific values:
integer, parameter :: neq=${NEQ}, nparams=${NPARAMS}

public func, jac

contains

subroutine solve(x0, rtol, x)
  integer, parameter :: NX = ${NX}
  real(dp), intent(in) :: x0(NX), rtol
  real(dp), intent(out) :: x(NX)
  real(dp) :: stime, etime, cptime
  integer :: ierr, ifail
  
end subroutine

subroutine f(neq, x, fx, iflag)
  ! Function
  integer, intent(in) :: neq
  real(dp), intent(in) :: x(${NX}+${NPARAM})
  return
end subroutine

subroutine df(neq, ldjac, x, dfx, iflag)
  ! Jacobian
  integer, intent(in) :: neq
  real(dp), intent(in) :: x(${NX}+${NPARAM})
  end select
end subroutine


subroutine zibsec(cptim, ifail)
  real(dp), intent(out) :: cptim
  integer, intent(out) :: ifail
  ifail = 0
  call cpu_time(cptim)
end subroutine

end module
