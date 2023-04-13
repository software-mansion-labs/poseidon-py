#!/bin/bash

build_for_mac_target () {
    MACARCH=$(awk -F '-' '{print $1}' <<< $1)

    pushd poseidon/sources
    sed "/CFLAGS = -Wall -O3 -fPIC/ s/$/ -target $1/" Makefile > "Makefile_$MACARCH"
    make -f "Makefile_$MACARCH" only_c
    rm *.o "Makefile_$MACARCH"
    popd

    mv poseidon/sources/lib_pos.so "$(awk -F '-' '{print $1}' <<< $1)_lib_pos.dylib"
}

echo "Building poseidon..."

command -v make >/dev/null 2>&1
if [ $? -eq 1 ]; then
    echo >&2 "Error: make not found. Make sure it is installed."
    exit 1
fi

if [[ "$OSTYPE" == *"linux"* ]]; then
    make -C poseidon/sources only_c
    mv poseidon/sources/lib_pos.so lib_pos.so
elif [[ "$OSTYPE" == "darwin"* ]]; then
    build_for_mac_target "x86_64-apple-macos11"
    build_for_mac_target "arm64-apple-macos11"
    lipo -create -output lib_pos.dylib x86_64_lib_pos.dylib arm64_lib_pos.dylib

    find . -type f -not -name lib_pos.dylib -name '*.dylib' -delete
else
    echo "$OSTYPE is not supported at the moment"
    exit 1;
fi

make -C poseidon/sources clean
