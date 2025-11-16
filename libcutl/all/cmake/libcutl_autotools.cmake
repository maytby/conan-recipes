include(CheckCXXCompilerFlag)
include(CheckIncludeFile)
include(CheckSymbolExists)
include(TestBigEndian)

check_include_file("dlfcn.h" HAVE_DLFCN_H)
check_include_file("inttypes.h" HAVE_INTTYPES_H)
check_include_file("memory.h" HAVE_MEMORY_H)
check_include_file("stdint.h" HAVE_STDINT_H)
check_include_file("stdlib.h" HAVE_STDLIB_H)
check_include_file("strings.h" HAVE_STRINGS_H)
check_include_file("string.h" HAVE_STRING_H)
check_include_file("sys/stat.h" HAVE_SYS_STAT_H)
check_include_file("sys/types.h" HAVE_SYS_TYPES_H)
check_include_file("unistd.h" HAVE_UNISTD_H)

set(ANSI_C_HEADERS
        stdlib.h
        stdio.h
        string.h
        stddef.h
        limits.h
        float.h
        errno.h
        time.h
)
set(STDC_HEADERS 1)
# Check each header
foreach(hdr IN LISTS ANSI_C_HEADERS)
    check_include_file("${hdr}" HEADER_EXISTS)
    if(NOT HEADER_EXISTS)
        unset(STDC_HEADERS)
    endif()
endforeach()

file(REMOVE_RECURSE "${LIBCUTL_PATH}/cutl/details/boost")
file(REMOVE_RECURSE "${LIBCUTL_PATH}/cutl/details/expat")
file(REMOVE "${LIBCUTL_PATH}/version")

# -------------------------------
# Thread detection (only if not using external Boost)
# -------------------------------
find_package(Threads QUIET)

if(Threads_FOUND)
    set(HAVE_PTHREAD 1)
endif()

set(LIBCUTL_BYTEORDER 1234)

# -------------------------------
# Generate config headers (Autotools: AC_CONFIG_HEADERS)
# -------------------------------
file(GLOB_RECURSE TEMPLATES ${LIBCUTL_PATH}/cutl/*.h.in)

foreach(in_file ${TEMPLATES})
    # Remove ".in" extension
    get_filename_component(filename ${in_file} NAME_WE)

    # Compute output directory (mirroring the source folder)
    file(RELATIVE_PATH rel_path ${CMAKE_CURRENT_SOURCE_DIR} ${in_file})
    get_filename_component(rel_dir ${rel_path} DIRECTORY)

    set(out_file "${LIBCUTL_PATH}/../${rel_dir}/${filename}.h")

    message("templating - ${in_file} -> ${out_file}")
    configure_file(${in_file} ${out_file})
endforeach ()

include_directories(${CMAKE_CURRENT_BINARY_DIR})
