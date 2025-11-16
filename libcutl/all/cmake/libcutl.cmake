
# Generate requested libraries:
#   - libcutl


file(GLOB_RECURSE LIBCUTL_SRCS ${LIBCUTL_PATH}/cutl/*.cxx)
file(GLOB_RECURSE LIBCUTL_C_SRCS ${LIBCUTL_PATH}/cutl/*.c)
file(GLOB_RECURSE LIBCUTL_MODULES 
    "${LIBCUTL_PATH}/cutl/*.i*"
)
file(GLOB_RECURSE LIBCUTL_HDRS
    "${LIBCUTL_PATH}/cutl/*.h"
    "${LIBCUTL_PATH}/cutl/*.hpp"
    "${LIBCUTL_PATH}/cutl/*.hxx"
    "${LIBCUTL_PATH}/cutl/*.txx"
 )

add_library(cutl ${LIBCUTL_SRCS} ${LIBCUTL_C_SRCS} ${LIBCUTL_HDRS})

if(BUILD_SHARED_LIBS)
    target_compile_definitions(cutl PUBLIC LIBCUTL_DYNAMIC_LIB=1)
else()
    target_compile_definitions(cutl PUBLIC LIBCUTL_STATIC_LIB=1)
endif()

target_link_libraries(cutl PUBLIC boost::boost)
target_compile_definitions(cutl PRIVATE LIBCUTL_EXTERNAL_BOOST=${LIBCUTL_EXTERNAL_BOOST})

target_link_libraries(cutl PUBLIC expat::expat)
target_compile_definitions(cutl PRIVATE LIBCUTL_EXTERNAL_EXPAT=${LIBCUTL_EXTERNAL_EXPAT})


if(NOT LIBCUTL_DISABLE_THREADS)
    target_link_libraries(cutl PUBLIC Threads::Threads)
endif()


target_include_directories(cutl PUBLIC
        ${LIBCUTL_PATH}
)

install(TARGETS cutl
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
foreach ( file ${LIBCUTL_HDRS} ${LIBCUTL_MODULES} )
    file(RELATIVE_PATH REL_PATH "${LIBCUTL_PATH}" "${file}")# Strip the filename to get only the directory
    get_filename_component(REL_DIR "${REL_PATH}" DIRECTORY)
    install( FILES ${file} DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}/${REL_DIR}" )
endforeach()
# -------------------------------
# pkg-config generation (Autotools: PKGCONFIG)
# -------------------------------
configure_file(
        ${LIBCUTL_PATH}/libcutl.pc.in
        ${CMAKE_CURRENT_BINARY_DIR}/libcutl.pc
        @ONLY
)
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/libcutl.pc DESTINATION lib/pkgconfig)

