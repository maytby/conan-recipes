import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd, check_max_cppstd
from conan.tools.files import apply_conandata_patches, chdir, copy, export_conandata_patches, get, rmdir, collect_libs
from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout

required_conan_version = ">=1.52.0"


class ConanLibCutl(ConanFile):
    name = "libxsd-frontend"
    description = (
        "libxsd-frontend is a compiler frontend for the W3C XML Schema definition language. It includes a parser, semantic graph types and a traversal mechanism."
    )
    license = ("GPLv2")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.codesynthesis.com/projects/libxsd-frontend/"
    topics = ("xml", "c++")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": False}

    def export_sources(self):
        export_conandata_patches(self)
        copy(self, "CMakeLists.txt", self.recipe_folder, self.export_sources_folder)
        copy(self, "cmake/*.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires("xerces-c/[>=3.0.0]")
        self.requires("libcutl/[>=1.8]")
        
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
        toolchain.variables["LIBXSD_FRONTEND_PATH"] = self.source_folder.replace("\\", "/")
        toolchain.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=os.path.join(self.source_folder, os.pardir))
        cmake.build()

    def package(self):
        copy(self, "GPLv2", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
