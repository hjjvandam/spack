#!/bin/bash
cmake -DCMAKE_C_COMPILER=/usr/bin/gcc \
      -DCMAKE_CXX_COMPILER=/usr/bin/g++ \
      -DCMAKE_Fortran_COMPILER=/usr/bin/gfortran \
      -H. -Bbuild
