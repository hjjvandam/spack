# CMake setup for compiling the QM/MM code
#
# The QM/MM code is pwqmmm. There are just two
# files to compile. The rest comes from:
# - The LAMMPS built with +qmmm +lib
# - The Quantum-ESPRESSO built with +couple
#
cmake_minimum_required(VERSION 3.30.5)

project(pwqmmm VERSION 1.0 HOMEPAGE_URL https://github.com/lammps/lammps/tree/develop/lib/qmmm LANGUAGES C CXX Fortran)

set(PWQMMM_LINK_LIBS)

find_package(MPI)

# Quantum-ESPRESSO requires 2 packages
# - MBD (Many-body dispersion) and
# - QE (Quantum-ESPRESSO itself)
find_package(MBD)
find_package(QE)

include_directories(${MPI_C_INCLUDE_PATH})
list(APPEND PWQMMM_LINK_LIBS ${MPI_C_LIBRARIES})

include_directories(${MBD_INCLUDE_PATH})
list(APPEND PWQMMM_LINK_LIBS ${MBD_LIBRARIES})

include_directories(${QE_INCLUDE_PATH})
list(APPEND PWQMMM_LINK_LIBS ${QE_LIBRARIES})

add_library(qmmm libqmmm.c)

add_executable(pwqmmm pwqmmm.c)

target_include_directories(pwqmmm INTERFACE $<BUILD_INTERFACE:${QE_INCLUDE_PATH}>)
target_link_libraries(pwqmmm PUBLIC qmmm ${PWQMMM_LINK_LIBS})
