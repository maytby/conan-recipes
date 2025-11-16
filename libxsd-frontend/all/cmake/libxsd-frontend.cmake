
# Generate requested libraries:
#   - xsd


# C library
file(GLOB_RECURSE SRCS_LIBXSD_FRONTEND ${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.cxx)
file(GLOB_RECURSE LIBXSD_FRONTEND_HDRS
    "${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.h"
    "${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.hpp"
    "${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.hxx"
    "${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.txx"
    "${LIBXSD_FRONTEND_PATH}/xsd-frontend/*.ixx"
 )

add_library(libxsd_frontend ${SRCS_LIBXSD_FRONTEND})

target_include_directories(libxsd_frontend PRIVATE
    ${LIBXSD_FRONTEND_PATH}/
)
target_link_libraries(libxsd_frontend PRIVATE
    XercesC::XercesC
    libcutl::libcutl
)

install(TARGETS libxsd_frontend
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
            ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
foreach ( file ${LIBXSD_FRONTEND_HDRS} )
    file(RELATIVE_PATH REL_PATH "${LIBXSD_FRONTEND_PATH}" "${file}")# Strip the filename to get only the directory
    get_filename_component(REL_DIR "${REL_PATH}" DIRECTORY)
    install( FILES ${file} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${REL_DIR}" )
endforeach()
