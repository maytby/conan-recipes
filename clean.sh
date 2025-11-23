#!/bin/bash

conan remove "libcutl/*" -c
conan remove "libxsd-frontend/*" -c
conan remove "xsd/*" -c

conan cache clean "libcutl/*"
conan cache clean "libxsd-frontend/*"
conan cache clean "xsd/*"