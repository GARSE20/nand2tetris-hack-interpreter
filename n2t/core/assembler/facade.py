from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from n2t.core.assembler.parser import Parser


@dataclass
class Assembler:
    asm_parser = Parser()

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        self.asm_parser.clean()
        self.asm_parser.set(assembly)
        result = self.asm_parser.parse()
        return result
