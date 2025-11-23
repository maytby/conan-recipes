cmake_minimum_required(VERSION 3.15)
project(xsd)

# get libxsd headers
file(GLOB_RECURSE BUILD_HDRS_LIBXSD
    "${XSD_PATH}/libxsd/xsd/*.hxx"
)

file(GLOB_RECURSE HDRS_LIBXSD
    "${XSD_PATH}/libxsd/xsd/*.txx"
    "${XSD_PATH}/libxsd/xsd/*.ixx"
)


include(${PROJECT_SOURCE_DIR}/cmake/xsd_configure.cmake)
if(BUILD_TOOLS)
    include(${PROJECT_SOURCE_DIR}/cmake/xsd.cmake)
endif()

if(COLLECT_HEADERS)
        foreach ( file ${HDRS_LIBXSD} ${BUILD_HDRS_LIBXSD} )
        file(RELATIVE_PATH REL_PATH "${XSD_PATH}/libxsd" "${file}")# Strip the filename to get only the directory
        get_filename_component(REL_DIR "${REL_PATH}" DIRECTORY)
        install( FILES ${file} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${REL_DIR}" )
        endforeach()
endif()