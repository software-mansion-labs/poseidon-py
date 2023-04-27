import ctypes
import dataclasses
import pathlib
import struct
import os
from typing import List, Optional

LIB_NAME = "lib_pos"
UINT256_MAX = 2**256 - 1


def hades_permutation(values: List[int]) -> List[int]:
    _validate_values(values)

    LOADER.load_c_lib()

    c_values = Converter.make_c_values(values)

    assert LOADER.c_lib is not None
    LOADER.c_lib.permutation_3(c_values)

    return Converter.make_py_values(c_values)


def _validate_values(values: List[int]) -> None:
    if len(values) != 3:
        raise ValueError(f"expected 3 values, got {len(values)} values")

    for val in values:
        _assert_u_int256_t(val)


def _assert_u_int256_t(value: int) -> None:
    if not 0 <= value <= UINT256_MAX:
        raise ValueError(f"{value} out of u_int256_t range")


@dataclasses.dataclass
class Loader:
    lib_name: str
    c_lib: Optional[ctypes.CDLL] = None

    def load_c_lib(self) -> None:
        if self.c_lib:
            return

        lib_path = self._get_lib_path()
        self.c_lib = ctypes.CDLL(str(lib_path))

        self._set_types()

    def _get_lib_path(self) -> pathlib.Path:
        dir_ = pathlib.Path(__file__).parents[1]
        file_ = next(file for file in os.listdir(dir_) if file.startswith(LIB_NAME))
        return dir_ / file_

    def _set_types(self) -> None:
        assert self.c_lib is not None
        self.c_lib.permutation_3.argtypes = [ctypes.POINTER(Converter.felt_t)]
        self.c_lib.permutation_3.restype = None


LOADER = Loader(LIB_NAME)


class Converter:
    felt_t = ctypes.c_uint64 * 4

    @staticmethod
    def make_c_values(values: List[int]) -> ctypes.Array:
        felts = [Converter.int_to_felt_t(val) for val in values]
        return (Converter.felt_t * 3)(*felts)

    @staticmethod
    def int_to_felt_t(value: int) -> felt_t:
        value_bytes = value.to_bytes(32, byteorder="little", signed=False)
        felt_ = struct.unpack("4Q", value_bytes)
        return Converter.felt_t(*felt_)

    @staticmethod
    def make_py_values(c_values: ctypes.Array) -> List[int]:
        return [
            int.from_bytes(val, byteorder="little", signed=False) for val in c_values
        ]
