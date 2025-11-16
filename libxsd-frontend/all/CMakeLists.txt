cmake_minimum_required(VERSION 3.15)
project(libxsd_frontend)

find_package(XercesC CONFIG REQUIRED)
find_package(libcutl CONFIG REQUIRED)

message("Generate libxsd-frontend from sources at ${LIBXSD_FRONTEND_PATH}")

include(${PROJECT_SOURCE_DIR}/cmake/libxsd-frontend.cmake)