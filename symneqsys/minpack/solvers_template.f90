! ${_warning_in_the_generated_file_not_to_edit}

! Template (mako) for generating Fortran 90 code to wrapped.
! MINPACK calling routine, wrapped by neqsys_wrapper.pyx
! NOTE: If the F77 version seems complex, look at:
! http://people.sc.fsu.edu/~jburkardt/f_src/minpack/minpack.f90

module neqsys
  use iso_c_binding, only: c_double, c_int
  implicit none
  ! Set problem specific values:
  integer, parameter :: NX = ${NX} ! Number of values (>= NE)
  integer, parameter :: NE = ${NE} ! Number of equations
  integer, parameter :: NP = ${NPARAMS} ! Number of parameters
  integer(c_int) :: NFEV, NJEV, NIT
  public lm_solve, func, get_nfev, get_njev, get_ne, get_nx

contains

  subroutine lm_solve(x, tol, info) bind(c)
    real(c_double), intent(inout) :: x(NX+NP)
    real(c_double), intent(in) :: tol ! relative error in sum of squares or in residuals
    integer(c_int), intent(inout) :: info ! 0 improper input, 1, 2, 3 (success), others error
    integer, parameter :: lwa = (5*NX+NE)*2 ! TODO: the last factor two seems to be need not to segault?
    integer, parameter :: ldfjac = NE ! leading dimension of jacobian
    integer, parameter :: m = NE
    integer, parameter :: n = NX
    integer :: ipvt(NX), wa(lwa)
    real(c_double) :: fvec(NE), fjac(NE, NX)
    wa = 0
    NFEV = 0
    NJEV = 0
    write(6,*) 'about to call lmder1!'
    flush(6)
    call lmder1(func, NE, NX, x, fvec, fjac, ldfjac, tol, info, ipvt, wa, lwa)
    write(6,*) 'back from lmder1!'
    flush(6)
  end subroutine lm_solve

  subroutine func(m, n, x, fvec, fjac, ldfjac, iflag) bind(c)
    ! Function
    integer(c_int), intent(in) :: m, n, ldfjac, iflag
    real(c_double), intent(in) :: x(NX+NP)
    real(c_double), intent(out) :: fvec(m)
    real(c_double), intent(out) :: fjac(m,n)

  % for cse_token, cse_expr in max(func_cse_defs, jac_cse_defs, key=len):
    real(c_double) :: ${cse_token}
  % endfor

    if (iflag == 1) then
       ! Function evaluation
       NFEV = NFEV + 1
    % for cse_token, cse_expr in func_cse_defs:
       ${cse_token} = ${cse_expr}
    % endfor
    % for i, expr in enumerate(func_new_code, 1):
       fvec(${i}) = ${expr}
    % endfor
    elseif (iflag == 2) then
       ! Jacobian evaluation
       NJEV = NJEV + 1
    % for cse_token, cse_expr in jac_cse_defs:
       ${cse_token} = ${cse_expr}
    % endfor
  
    % for i, expr in enumerate(jac_new_code):
       fjac(${(i // NX) + 1}, ${(i % NX) + 1}) = ${expr}
    % endfor
    end if
  end subroutine func

  subroutine get_nfev(nfev_) bind(c)
    integer(c_int), intent(inout) :: nfev_
    nfev_ = NFEV
  end subroutine get_nfev

  subroutine get_njev(njev_) bind(c)
    integer(c_int), intent(inout) :: njev_
    njev_ = NJEV
  end subroutine get_njev

  subroutine get_ne(ne_) bind(c)
    ! Returns the number of equations in the problem
    integer(c_int), intent(inout) :: ne_
    ne_ = NE
  end subroutine get_ne
  
  subroutine get_nx(nx_) bind(c)
    ! Returns the number of independent variables in problem
    integer(c_int), intent(inout) :: nx_
    nx_ = NE
  end subroutine get_nx
  

end module neqsys

