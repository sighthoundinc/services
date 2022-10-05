# ---------------------------------------------------------------
# Copyright (C) 2022 Sighthound, Inc. All rights reserved.
#
# The information and source code contained herein is the
# exclusive property of Sighthound, Inc. No part of this software
# may be used, reproduced, stored or distributed in any form,
# without explicit written authorization from Sighthound, Inc.
# ---------------------------------------------------------------
from conans import ConanFile
import glob
import os

class WheelConan(ConanFile):
    python_requires = "conan-helper/1.0.13+c575aaab@sighthound/master"
    python_requires_extend = "conan-helper.SighthoundBase"

    scm = {"type": "git", "url": "auto", "revision": "auto"}

    license = "Proprietary"
    url = "https://github.com/sighthoundinc/services"
    description = "Sighthound services package"

    def build(self):
        pass

    def package(self):
        ignore = open('.conanignore', 'r').readlines()
        # Copy services
        services = [fn for fn in glob.glob(self.source_folder + "/*") if os.path.basename(fn) not in ignore]
        for service in services:
            print(f"Adding {service}")
            self.run(f"cp -r {service} {self.package_folder}")

    def package_info(self):
        pass