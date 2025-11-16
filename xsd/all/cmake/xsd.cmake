
# Generate requested libraries:
#   - xsd


# C library
file(GLOB_RECURSE SRCS_XSD ${XSD_PATH}/xsd/*.cxx)

# cop pregenerated stuff to actual build
file(COPY ${XSD_PATH}/xsd/pregenerated/xsd DESTINATION ${XSD_PATH}/)

add_executable(xsd ${SRCS_XSD})

target_compile_definitions(xsd PRIVATE XSD_COPYRIGHT="${XSD_COPYRIGHT}")
target_include_directories(xsd PRIVATE
    ${XSD_PATH}/
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

