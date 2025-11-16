cmake_minimum_required(VERSION 3.15)
project(xsd)

find_package(XercesC CONFIG REQUIRED)
find_package(libcutl CONFIG REQUIRED)
find_package(libxsd-frontend CONFIG REQUIRED)

message("Generate xsd from sources at ${XSD_PATH}")

include(${PROJECT_SOURCE_DIR}/cmake/xsd_configure.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/xsd.cmake)