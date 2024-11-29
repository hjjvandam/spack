# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install pwqmmm
#
# You can edit this file again by typing:
#
#     spack edit pwqmmm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import sys

from spack.package import *


#class Pwqmmm(MakefilePackage, CudaPackage, ROCmPackage, PythonExtension, Package):
#class Pwqmmm(MakefilePackage):
class Pwqmmm(CMakePackage):
    """QM/MM code combining LAMMPS and Quantum ESPRESSO

    The QM/MM code is actually a part of LAMMPS. In the LAMMPS/lib/qmmm
    directory the application wrapper code is kept. In addition the libqmmm.a
    library is provided, and LAMMPS is compiled into a library liblammps.a.
    Quantum ESPRESSO also needs to be compiled as a library. Then everything
    is linked together to provide the pwqmmm application.

    In order to make the installation work with Spack a fork of LAMMPS is
    kept at `https://github.com/hjjvandam/pwqmmm`. The **sole purpose** of this
    fork is to give Spack a pwqmmm tarball it can look for. The build
    procedure just builds in pwqmmm/lib/qmmm to pull the QE+LAMMPS
    QM/MM framework together.
    """

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/lammps/lammps/tree/develop/lib/qmmm"
    git = "https://github.com/lammps/lammps.git"
    url = "https://github.com/lammps/lammps/archive/patch_1Sep2017.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("hjjvandam")

    # FIXME: Add the SPDX identifier of the project's license below.
    # See https://spdx.org/licenses/ for a list. Upon manually verifying
    # the license, set checked_by to your Github username.
    license("GPL-2.0-only", checked_by="hjjvandam")

    # FIXME: Add proper versions here.
    version("develop", branch="develop")
    version(
        "20240829.1",
        sha256="3aea41869aa2fb8120fc4814cab645686f969e2eb7c66aa5587e500597d482dc",
        preferred=True,
    )

    patch("add_files.patch")

    # FIXME: Add dependencies if required.
    #depends_on("python")
    depends_on("quantum-espresso@develop+mpi+couple")
    depends_on("lammps+mpi+qmmm+lib")

    root_cmakelists_dir = "lib/qmmm"

    def edit(self, spec, prefix):
        # FIXME: Unknown build system
        build_path = join_path(self.build_directory,"lib","qmmm")
        with open("stupid.out","w") as fp:
            fp.write(f"build_dir = {build_path}\n")
        chdir(build_path)
        with open("Makefile","w") as fp:
            fp.write("SRC=pwqmmm.c libqmmm.c\n")
            fp.write("OBJ=$(SRC:%.c=%.o)\n\n")
            fp.write("default: pwqmmm\n\n")
            fp.write("all: libqmmm.a pwqmmm\n\n")
            fp.write("pwqmmm: pwqmmm.o $(OBJ) $(PWOBJS) $(LIBOBJS) $(LAMMPSLIB)\n")
            fp.write("	$(MPICXX) $(LDFLAGS) -o $@ $^ $(PKG_PATH) $(PKG_LIB) $(MPILIBS) $(LIBS)\n\n")
            fp.write("libqmmm.a: libqmmm.o\n")
            fp.write("	$(AR) $(ARFLAGS) $@ $^\n\n")
            
        #make()
        #make("install")
