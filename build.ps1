#!/bin/bash

echo "Building poseidon..."

make -C poseidon/sources only_c
mv poseidon/sources/lib_pos.so lib_pos.so

make -C poseidon/sources clean
