
# Generate requested libraries:
#   - xsd
project(xsd)

# get libxsd headers
file(GLOB_RECURSE BUILD_HDRS_LIBXSD
    "${XSD_PATH}/libxsd/xsd/*.hxx"
)

file(GLOB_RECURSE HDRS_LIBXSD
    "${XSD_PATH}/libxsd/xsd/*.txx"
    "${XSD_PATH}/libxsd/xsd/*.ixx"
)

if(BUILD_TOOLS)
        # cop pregenerated stuff to actual build
        file(COPY ${XSD_PATH}/xsd/xsd/pregenerated/xsd DESTINATION ${XSD_PATH}/xsd/)
        file(REMOVE_RECURSE ${XSD_PATH}/xsd/xsd/pregenerated/)

        # get sources to compile
        file(GLOB_RECURSE SRCS_XSD ${XSD_PATH}/xsd/*cxx)

        add_executable(xsd ${SRCS_XSD} ${BUILD_HDRS_LIBXSD})

        target_compile_definitions(xsd PRIVATE XSD_COPYRIGHT="${XSD_COPYRIGHT}")
        target_compile_definitions(xsd PRIVATE XSD_VERSION="${XSD_VERSION}")
        target_compile_definitions(xsd PRIVATE XSD_VERSION_FULL="${XSD_VERSION_FULL}")
        target_compile_definitions(xsd PRIVATE XSD_VERSION_STR="${XSD_VERSION_STR}")

        target_include_directories(xsd PRIVATE
                ${XSD_PATH}/xsd
                ${XSD_PATH}/libxsd
        )
        target_link_libraries(xsd PRIVATE
                XercesC::XercesC
                libcutl::libcutl
                libxsd-frontend::libxsd-frontend
        )

        install(TARGETS xsd
                RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
                LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
                ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        )
endif()

if(COLLECT_HEADERS)
        foreach ( file ${HDRS_LIBXSD} ${BUILD_HDRS_LIBXSD} )
        file(RELATIVE_PATH REL_PATH "${XSD_PATH}/libxsd" "${file}")# Strip the filename to get only the directory
        get_filename_component(REL_DIR "${REL_PATH}" DIRECTORY)
        install( FILES ${file} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${REL_DIR}" )
        endforeach()
endif()

