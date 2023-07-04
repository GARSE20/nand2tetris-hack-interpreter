from dataclasses import dataclass
from typing import List

from numpy import int16

from n2t.core.interpreter.memory import Memory


@dataclass
class State:
    reg_a: int16
    reg_d: int16
    reg_pc: int16
    ram: Memory
    rom: Memory

    def __init__(self, instructions: List[str]) -> None:
        self.reg_a = int16(0)
        self.reg_d = int16(0)
        self.reg_pc = int16(0)
        self.ram = Memory.create()
        self.rom = Memory.from_list(instructions)
