from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from numpy import binary_repr, int16

MEMORY_SIZE = 2**16
MEMORY_WIDTH = 16


@dataclass
class Memory:
    mem: List[str]

    @classmethod
    def create(cls) -> Memory:
        return cls(["0" * MEMORY_WIDTH] * MEMORY_SIZE)

    @classmethod
    def from_list(cls, lst: List[str]) -> Memory:
        return cls(lst)

    def set(self, address: int, value: int16) -> None:
        if address >= MEMORY_SIZE:
            raise Exception(f"""Address {address} is out of bounds""")
        self.mem[address] = binary_repr(int(value), width=MEMORY_WIDTH)

    def get_int16(self, address: int) -> int16:
        if address >= MEMORY_SIZE:
            raise Exception(f"""Address {address} is out of bounds""")
        return int16(int(self.mem[address], 2))

    def get(self, address: int) -> str:
        if address >= MEMORY_SIZE:
            raise Exception(f"""Address {address} is out of bounds""")
        return self.mem[address]

    def size(self) -> int:
        return len(self.mem)

    def to_json(self, used: Set[int16]) -> str:
        json = '{\n\t"RAM": {\n'
        for address, value in enumerate(self.mem):
            if address not in used:
                continue
            json += f"""\t\t\"{address}\": {int(value, 2)},\n"""
        json = json[:-2] + "\n\t}\n}\n"
        return json
