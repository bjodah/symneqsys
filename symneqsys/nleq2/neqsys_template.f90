! Template for generating Fortran 90 code to wrapped using Cython for calling nleq2 from python.
! mako template variables: 

module neqsys
use types, only: dp
implicit none
! Set problem specific values:
integer, parameter :: neq=${NEQ}, nparams=${NPARAMS}

public func, jac

contains


subroutine func(neq, y)
  integer, intent(in) :: neq
  real(dp), intent(in) :: y(${NY}+${NPARAM})
  return
end subroutine

subroutine jac(neq, y)
  integer, intent(in) :: neq
  real(dp), intent(in) :: y(${NY}+${NPARAM})
  end select
end subroutine


end module
