#!/bin/bash

conan export libcutl/all --version=1.10.0
conan export libxsd-frontend/all --version=2.0.0

conan create xsd/all --version=4.2.0 --build=missing
