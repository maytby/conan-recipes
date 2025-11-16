cmake_minimum_required(VERSION 3.31)
project(cutl LANGUAGES C CXX)

message("Generate cutl from sources at ${LIBCUTL_PATH}")

include(${PROJECT_SOURCE_DIR}/cmake/libcutl_autotools.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/libcutl.cmake)
