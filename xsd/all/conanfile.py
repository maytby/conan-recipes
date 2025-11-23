import os
import re

from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.files import apply_conandata_patches, copy, export_conandata_patches, get, collect_libs, replace_in_file
from conan.tools.scm import Git
from conan.tools.scm import Version  # Conan >= 2.x

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
    url = "https://github.com/maytby/conan-recipes"
    homepage = "https://codesynthesis.com/projects/xsd/"
    topics = ("xml", "c++")

    settings = "os", "arch", "compiler", "build_type"
    
    def configure(self):
        self.output.info(f"context: {self.context}")
        if self.context == "host":
            # used as simple requirement
            self.package_type = "header-library"
        elif self.context == "build":
            # e.g. via tool_requires
            self.package_type = "application"

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        # xerces should be visible, since generated code requires it
        self.requires("xerces-c/[>=3.0.0]")
        if self.package_type == "application":
            self.requires("libcutl/[>=1.11.0]", visible=False)
            self.requires("libxsd-frontend/[>=2.1.0]", visible=False)
        
    def build_requirements(self):
        self.tool_requires("cmake/[>=3.31]")

    def package_id(self):
        del self.info.settings.compiler

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 17)

    def source(self):
        src = self.conan_data["sources"][self.version]
        if "git_url" in src:
            # git checkout with tag
            git = Git(self)
            git.clone(url=src['git_url'], target=".")
            if "git_tag" in src:
                git.checkout(src['git_tag'])
        else:
            get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        cmake_layout(self, src_folder="src")
        
    def _read_copyright_text(self):
        with open(os.path.join(self.source_folder, "LICENSE"), "r") as f:
            return f.readline()            

    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["XSD_PATH"] = self.source_folder.replace("\\", "/")
        v = Version(self.version)
        for template in ["LIBXSD", "XSD"]:
            toolchain.variables[f"{template}_VERSION"] = encode_version(self.version)
            toolchain.variables[f"{template}_VERSION_STR"] = self.version
            toolchain.variables[f"{template}_VERSION_ID"] = self.version
            toolchain.variables[f"{template}_VERSION_FULL"] = self.version
            toolchain.variables[f"{template}_VERSION_MAJOR"] = v.major
            toolchain.variables[f"{template}_VERSION_MINOR"] = v.minor
            toolchain.variables[f"{template}_VERSION_PATCH"] = v.patch
            toolchain.variables[f"{template}_PRE_RELEASE"] = "false"
            toolchain.variables[f"{template}_SNAPSHOT"] = 0
            toolchain.variables[f"{template}_SNAPSHOT_ID"] = ""
        toolchain.variables["XSD_COPYRIGHT"] = self._read_copyright_text().replace("Copyright (c) ", "").replace(".","").rstrip()
        self.output.info(f"package_type: {self.package_type}")
        toolchain.cache_variables["BUILD_TOOLS"] = self.package_type == "application"
        toolchain.cache_variables["COLLECT_HEADERS"] = self.package_type == "header-library"
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
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = []
        if self.package_type == "application":
            self.cpp_info.bindirs = ["bin"]
            
        # header component
        self.cpp_info.components["libxsd"].includedirs = ["include"]
