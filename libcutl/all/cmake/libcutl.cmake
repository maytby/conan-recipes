file(GLOB_RECURSE LIBCUTL_SRCS ${LIBCUTL_PATH}/libcutl/*.cxx)
file(GLOB_RECURSE LIBCUTL_C_SRCS ${LIBCUTL_PATH}/libcutl/*.c)
file(GLOB_RECURSE LIBCUTL_MODULES 
    "${LIBCUTL_PATH}/libcutl/*.i*"
)
file(GLOB_RECURSE LIBCUTL_HDRS
    "${LIBCUTL_PATH}/libcutl/*.h"
    "${LIBCUTL_PATH}/libcutl/*.hpp"
    "${LIBCUTL_PATH}/libcutl/*.hxx"
    "${LIBCUTL_PATH}/libcutl/*.txx"
 )

add_library(cutl ${LIBCUTL_SRCS} ${LIBCUTL_C_SRCS} ${LIBCUTL_HDRS})

if(BUILD_SHARED_LIBS)
    target_compile_definitions(cutl PRIVATE LIBCUTL_SHARED_BUILD=1)
else()
    target_compile_definitions(cutl PRIVATE LIBCUTL_STATIC_BUILD=1)
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

