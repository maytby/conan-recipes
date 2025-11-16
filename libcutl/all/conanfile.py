import os

from conan import ConanFile, Version
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd,check_max_cppstd
from conan.tools.files import apply_conandata_patches, chdir, copy, export_conandata_patches, get, rmdir, collect_libs
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools.scm import Git
import re

required_conan_version = ">=1.52.0"

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

class ConanLibCutl(ConanFile):
    name = "libcutl"
    description = (
        "libcutl is a C++ utility library. It contains a collection of generic and independent components such as meta-programming tests, smart pointers, containers, compiler building blocks, etc."
    )
    license = ("MIT")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.codesynthesis.com/projects/libcutl/"
    topics = ("xml", "c++")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": False}

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.recipe_folder, self.export_sources_folder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def requirements(self):
        pass
        
    def build_requirements(self):
        self.tool_requires("cmake/[>3.31 <4]")

    def package_id(self):
        del self.info.settings.compiler

    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, 14)

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
        
    def generate(self):
        toolchain = CMakeToolchain(self)
        toolchain.variables["LIBCUTL_PATH"] = self.source_folder.replace("\\", "/")
        v = Version(self.version)
        toolchain.variables["LIBCUTL_VERSION"] = encode_version(self.version)
        toolchain.variables["LIBCUTL_VERSION_STR"] = self.version
        toolchain.variables["LIBCUTL_VERSION_ID"] = self.version
        toolchain.variables["LIBCUTL_VERSION_MAJOR"] = v.major
        toolchain.variables["LIBCUTL_VERSION_MINOR"] = v.minor
        toolchain.variables["LIBCUTL_VERSION_PATCH"] = v.patch
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
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        if self.options.shared:
            self.cpp_info.defines.append("LIBCUTL_SHARED=1")
        else:
            self.cpp_info.defines.append("LIBCUTL_STATIC=1")
        self.cpp_info.libs = collect_libs(self)
