from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set

from numpy import int16

from n2t.core.interpreter.mappings import Mappings
from n2t.core.interpreter.state import State


@dataclass
class Interpreter:
    state: State
    cycles: int
    used: Set[int16]
    NO_DESTINATION = ""
    NO_JUMP = ""

    @classmethod
    def create(cls, instructions: Iterable[str], cycles: int) -> Interpreter:
        return cls(State(list(instructions)), cycles, set())

    def interpret(self) -> None:
        self.used = set()
        while self.cycles:
            self.cycles -= 1
            if self.state.reg_pc >= self.state.rom.size():
                break
            self.state.reg_pc += 1
            self.interpret_instruction(self.state.rom.get(int(self.state.reg_pc - 1)))

    def interpret_instruction(self, instruction: str) -> None:
        if instruction[0] == "0":
            self.interpret_a(instruction)
        elif instruction[0] == "1":
            self.interpret_c(instruction)

    def interpret_a(self, instruction: str) -> None:
        self.state.reg_a = int16(int(instruction[1:], 2))

    def interpret_c(self, instruction: str) -> None:
        instruction = instruction[3:]
        computation = Mappings.COMPUTATION_MAP[instruction[:7]]
        dest = Mappings.DESTINATION_MAP[instruction[7:10]]
        jump = Mappings.JUMP_MAP[instruction[-3:]]

        if dest.find("M") >= 0 or computation.find("M") >= 0:
            self.used.add(self.state.reg_a)

        computed_value = int16(
            eval(
                computation.replace("D", "self.state.reg_d")
                .replace("A", "self.state.reg_a")
                .replace("M", "self.state.ram.get_int16(self.state.reg_a)")
                .replace("!", "~")
            )
        )

        if dest != self.NO_DESTINATION:
            if dest.find("M") >= 0:
                self.state.ram.set(int(self.state.reg_a), computed_value)
            if dest.find("D") >= 0:
                self.state.reg_d = computed_value
            if dest.find("A") >= 0:
                self.state.reg_a = computed_value

        if jump != self.NO_JUMP:
            if (
                (jump == "JGT" and computed_value > 0)
                or (jump == "JEQ" and computed_value == 0)
                or (jump == "JGE" and computed_value >= 0)
                or (jump == "JLT" and computed_value < 0)
                or (jump == "JNE" and computed_value != 0)
                or (jump == "JLE" and computed_value <= 0)
                or (jump == "JMP")
            ):
                self.state.reg_pc = self.state.reg_a

    def print_ram(self) -> str:
        return self.state.ram.to_json(self.used)
