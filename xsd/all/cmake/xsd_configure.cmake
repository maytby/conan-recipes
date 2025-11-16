include(CheckCXXCompilerFlag)
include(CheckIncludeFile)
include(CheckSymbolExists)
include(TestBigEndian)


configure_file(${XSD_PATH}/xsd/version.hxx.in ${XSD_PATH}/xsd/version.hxx)