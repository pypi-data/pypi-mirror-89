import secrets

from typing import Union
from pathlib import Path

MAX_64_INT = 2 ** 63 - 1
MAX_32_INT = 2 ** 31 - 1


class Optimus:
    prime: int
    inverse: int
    random: int
    max_int: int

    def __init__(self,
                 prime: int,
                 inverse: int = None,
                 random: int = None,
                 bitlength: int = 64):
        if bitlength not in (32, 64):
            raise ValueError('bitlength can only be 32 or 64')
        self.max_int = bitlength == 32 and MAX_32_INT or MAX_64_INT
        self.prime = prime
        if inverse is None:
            inverse = mod_inverse(prime, self.max_int)
        self.inverse = inverse
        if random is None:
            random = rand_n(self.max_int - 1)
        self.random = random

    def encode(self, n: int) -> int:
        return ((n * self.prime) & self.max_int) ^ self.random

    def decode(self, n: int) -> int:
        return ((n ^ self.random) * self.inverse) & self.max_int


def mod_inverse(n: int, p: int) -> int:
    return pow(n, -1, p + 1)


def generate(
    path_to_primes: Union[str, Path] = 'optimus-primes',
    bitlength: int = 64
) -> Optimus:
    if bitlength not in (32, 64):
        raise ValueError('bitlength can only be 32 or 64')
    if isinstance(path_to_primes, str):
        path_to_primes = Path(path_to_primes)
    if not (path_to_primes.exists() and path_to_primes.is_dir()):
        raise ValueError(
            f'{str(path_to_primes)} does not exist or is not a directory'
        )
    n = rand_n(50)
    input_file = str(path_to_primes.joinpath(f'p{n}.txt').absolute())
    line_number = rand_n(1_000_000)
    with open(input_file, 'r') as f:
        for i in range(line_number):
            f.readline()
        return Optimus(int(f.readline().strip()), bitlength=bitlength)


def rand_n(n: int) -> int:
    return secrets.randbelow(n) + 1
