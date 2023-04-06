from typing import Iterable, Literal, Optional

Endianness = Literal["big", "little"]
HASH_BYTES = 32


def to_bytes(
    value: int,
    length: Optional[int] = None,
    byte_order: Optional[Endianness] = None,
    signed: Optional[bool] = None,
) -> bytes:
    """
    Converts the given integer to a bytes object of given length and byte order.
    The default values are 32B width (which is the hash result width) and 'big', respectively.
    """
    if length is None:
        length = HASH_BYTES

    if byte_order is None:
        byte_order = "big"

    if signed is None:
        signed = False

    return int.to_bytes(value, length=length, byteorder=byte_order, signed=signed)


def from_bytes(
    value: bytes,
    byte_order: Optional[Endianness] = None,
    signed: Optional[bool] = None,
) -> int:
    """
    Converts the given bytes object (parsed according to the given byte order) to an integer.
    Default byte order is 'big'.
    """
    if byte_order is None:
        byte_order = "big"

    if signed is None:
        signed = False

    return int.from_bytes(value, byteorder=byte_order, signed=signed)


def blockify(data, chunk_size: int) -> Iterable:
    """
    Returns the given data partitioned to chunks of chunks_size (last chunk might be smaller).
    """
    assert chunk_size > 0, f"chunk_size must be greater than 0. Got: {chunk_size}."
    return (data[i : i + chunk_size] for i in range(0, len(data), chunk_size))
