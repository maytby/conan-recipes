import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd,check_max_cppstd
from conan.tools.files import apply_conandata_patches, chdir, copy, export_conandata_patches, get, rmdir
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout

from conan.tools.scm import Version  # Conan >= 2.x

required_conan_version = ">=2"

import re

def encode_version(version_str):
    # Parse version: major.minor.patch(-pre)
    match = re.match(r"(\d+)\.(\d+)\.(\d+)(?:-([ab])\.(\d+)(?:\.z)?)?", version_str)
    if not match:
        raise ValueError(f"Invalid version string: {version_str}")
    
    major, minor, patch, pre_type, pre_num = match.groups()
    major = int(major)
    minor = int(minor)
    patch = int(patch)
    pre_num = int(pre_num) if pre_num else 0
    E = 1 if version_str.endswith(".z") else 0

    # Compute DDD
    if pre_type == "a":
        DDD = 499 + pre_num + 1  # alpha
    elif pre_type == "b":
        DDD = 499 + pre_num + 1  # beta
    else:
        DDD = 0

    # Compute AAAAABBBBBCCCCC as integer
    combined = major * 10**10 + minor * 10**5 + patch
    if DDD != 0 or E != 0:
        combined -= 1

    # Format the string
    numeric_version = f"{combined:015d}{DDD:03d}{E}"
    return numeric_version

class ConanXqilla(ConanFile):
    name = "xsd"
    description = (
        "XSD is a W3C XML Schema to C++ translator. "
        "It generates vocabulary-specific, statically-typed C++ mappings (also called bindings) from XML Schema definitions. "
        "XSD supports two C++ mappings: in-memory C++/Tree and event-driven C++/Parser."
    )
    license = ("GPL-2.0", "FLOSSE")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://codesynthesis.com/projects/xsd/"
    topics = ("xml", "c++")

    package_type = "application"
    settings = "os", "arch", "compiler", "build_type"

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires("xerces-c/[>=3.0.0]")
        self.requires("libcutl/[>=1.8]")
        self.requires("libxsd-frontend/2.0.0")
        
    def build_requirements(self):
        self.tool_requires("cmake/[>3 <4]")

    def package_id(self):
        del self.info.settings.compiler

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 11)
            check_max_cppstd(self, 14)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")
        
    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["XSD_PATH"] = self.source_folder.replace("\\", "/")
        v = Version(self.version)
        toolchain.variables["XSD_VERSION"] = encode_version(self.version)
        toolchain.variables["XSD_VERSION_STR"] = self.version
        toolchain.variables["XSD_VERSION_ID"] = self.version
        toolchain.variables["XSD_VERSION_FULL"] = self.version
        toolchain.variables["XSD_VERSION_MAJOR"] = v.major
        toolchain.variables["XSD_VERSION_MINOR"] = v.minor
        toolchain.variables["XSD_VERSION_PATCH"] = v.patch
        toolchain.variables["XSD_COPYRIGHT"] = "2025"
        toolchain.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "GPLv2", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "FLOSSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.frameworkdirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.resdirs = []
        self.cpp_info.includedirs = []

        # TODO: to remove in conan v2
        bin_path = os.path.join(self.package_folder, "bin")
        self.output.info(f"Appending PATH environment variable: {bin_path}")
        self.env_info.path.append(bin_path)
