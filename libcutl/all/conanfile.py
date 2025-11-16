import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd,check_max_cppstd
from conan.tools.files import apply_conandata_patches, chdir, copy, export_conandata_patches, get, rmdir, collect_libs
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout

required_conan_version = ">=1.52.0"


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
        self.requires("boost/1.89.0")
        self.requires("expat/2.7.3")
        
    def build_requirements(self):
        self.tool_requires("cmake/[>3.31 <4]")

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
        toolchain.variables["LIBCUTL_PATH"] = self.source_folder.replace("\\", "/")
        toolchain.variables["LIBCUTL_VERSION"] = self.version
        toolchain.variables["PACKAGE"] = self.name
        toolchain.variables["PACKAGE_BUGREPORT"] = f"{self.name}-users@codesynthesis.com"
        toolchain.variables["PACKAGE_NAME"] = self.name
        toolchain.variables["PACKAGE_STRING"] = f"{self.name} {self.version}"
        toolchain.variables["PACKAGE_TARNAME"] = self.name
        toolchain.variables["PACKAGE_VERSION"] = self.version
        toolchain.variables["VERSION"] = self.version
        toolchain.variables["LIBCUTL_EXTERNAL_BOOST"] = 1
        toolchain.variables["LIBCUTL_EXTERNAL_EXPAT"] = 1
        if not self.options.shared:
            toolchain.variables["LIBCUTL_STATIC_LIB"] = 1         
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
        if not self.options.shared:
            self.cpp_info.defines.append("LIBCUTL_STATIC_LIB=1")

        self.cpp_info.libs = collect_libs(self)
