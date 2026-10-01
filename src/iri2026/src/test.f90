program test_iri
  implicit none
  logical :: jf(50)
  integer, parameter :: jmag = 0
  real :: outf(20, 1000), oarr(100)

  jf = .true.
  jf(4:6) = .false.
  jf(22:23) = .false.
  jf(30) = .false.
  jf(33:35) = .false.
  jf(39:40) = .false.
  jf(47) = .false.

  call read_ig_rz
  call readapf107
  call IRI_SUB(jf, jmag, 35.0, 120.0, 2020, 101, 37.0, &
       100.0, 200.0, 20.0, outf, oarr)

  if (outf(1, 1) <= 0.0) error stop "IRI test returned invalid electron density"
  print *, "IRI2026 test passed"
end program test_iri
