program iri_driver

use, intrinsic:: iso_fortran_env, only: stderr=>error_unit

implicit none

logical :: jf(50)
integer, parameter :: jmag = 0
integer :: iyyyy, mmdd, nalt
real :: glat, glon, dhour
integer :: ymdhms(6)
real :: alt_km_range(3)
real :: oarr(100), outf(20,1000)
real :: tecbo, tecto
real, allocatable :: altkm(:)
character(1024) :: argv
integer :: i

! Keep the IRI-recommended switches used by the iri2020 Python interface.
jf = .true.
jf(4:6) = .false.
jf(22:23) = .false.
jf(30) = .false.
jf(33) = .false.
jf(34:35) = .false.
jf(39:40) = .false.
jf(47) = .false.

if (command_argument_count() /= 11) then
  write(stderr,*) 'need input parameters: year month day hour minute second glat glon min_alt_km max_alt_km step_alt_km'
  error stop 1
endif

do i = 1, 6
  call get_command_argument(i, argv)
  read(argv,*) ymdhms(i)
enddo
call get_command_argument(7, argv)
read(argv,*) glat
call get_command_argument(8, argv)
read(argv,*) glon
do i = 1, 3
  call get_command_argument(8+i, argv)
  read(argv,*) alt_km_range(i)
enddo

nalt = int((alt_km_range(2) - alt_km_range(1)) / alt_km_range(3)) + 1
if (nalt < 1 .or. nalt > size(outf, 2)) error stop 'invalid altitude range'
allocate(altkm(nalt))
altkm(1) = alt_km_range(1)
do i = 2, nalt
  altkm(i) = altkm(i-1) + alt_km_range(3)
enddo

iyyyy = ymdhms(1)
mmdd = ymdhms(2) * 100 + ymdhms(3)
dhour = ymdhms(4) + ymdhms(5) / 60. + ymdhms(6) / 3600.

call read_ig_rz
call readapf107
call IRI_SUB(JF, JMAG, glat, glon, IYYYY, MMDD, DHOUR+25., &
     alt_km_range(1), alt_km_range(2), alt_km_range(3), OUTF, OARR)
call IRITEC(glat, glon, jmag, jf, iyyyy, mmdd, dhour+25., &
            0., alt_km_range(2), 0.1, OARR, tecbo, tecto)
oarr(37) = tecbo + tecto
if (oarr(37) /= 0.) oarr(38) = tecto / oarr(37) * 100.

do i = 1, nalt
  print '(F10.3, 11ES16.8)', altkm(i), outf(:11,i)
enddo
print '(/,100ES16.8)', oarr

end program
