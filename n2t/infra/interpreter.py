from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from n2t.core.assembler import Assembler
from n2t.core.interpreter import Interpreter
from n2t.infra.io import File


@dataclass
class InterpreterProgram:
    path: Path
    cycles: int

    @classmethod
    def load_from(cls, file_name: str, cycles: int) -> InterpreterProgram:
        return cls(Path(file_name), cycles)

    def interpret(self) -> None:
        file = File(self.path)
        instructions = file.load()
        assembler = Assembler()
        if str(self.path).split(".")[-1] == "asm":
            instructions = assembler.assemble(instructions)
        interpreter = Interpreter.create(instructions, self.cycles)
        interpreter.interpret()
        File(
            self.path.with_name(str(self.path.name).split(".")[-2] + ".json")
        ).save_string(interpreter.print_ram())
