from typing import List
from poseidon_py.c_bindings import hades_permutation
from poseidon_py.utils import blockify, from_bytes, to_bytes

POSEIDON_PARAMS = {
    "m": 3,
    "r": 2,
}


def poseidon_perm(x: int, y: int, z: int) -> List[int]:
    """
    Returns the poseidon permutation of the inputs.
    """
    return hades_permutation([x, y, z])


def poseidon_hash_func(x: bytes, y: bytes) -> bytes:
    """
    Returns the poseidon_hash of the inputs.
    """
    return to_bytes(poseidon_perm(from_bytes(x), from_bytes(y), 2)[0])


def poseidon_hash(x: int, y: int) -> int:
    """
    Hashes two elements and retrieves a single field element output.
    """
    return hades_permutation([x, y, 2])[0]


def poseidon_hash_single(x: int) -> int:
    """
    Hashes single element and retrieves a single field element output.
    """
    return hades_permutation([x, 0, 1])[0]


def poseidon_hash_many(array: List[int]) -> int:
    """
    Hashes array of elements and retrieves a single field element output.
    """
    values = list(array)
    m = POSEIDON_PARAMS["m"]
    r = POSEIDON_PARAMS["r"]

    # Pad input with 1 followed by 0's (if necessary).
    values.append(1)
    values += [0] * (-len(values) % r)

    assert len(values) % r == 0
    state = [0] * m
    for block in blockify(data=values, chunk_size=r):
        state = list(
            hades_permutation(
                [state_val + block_val for state_val, block_val in zip(state, block)]
                + state[-1:]
            )
        )

    return state[0]
