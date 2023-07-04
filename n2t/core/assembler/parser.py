from typing import Iterable, List

from n2t.core.assembler.mapping import InstructionMapping
from n2t.core.assembler.table import SymbolTable


class Parser:
    A_INSTRUCTION = 0
    C_INSTRUCTION = 1
    LABEL = 2

    def __init__(self) -> None:
        self.init_parser()

    def init_parser(self) -> None:
        self.symbol_table = SymbolTable()
        self.instr_mapping = InstructionMapping()
        self.asm: Iterable[str] = []
        self.stripped: List[str] = []
        self.min_free = 16

    def set(self, assembly: Iterable[str]) -> None:
        self.asm = assembly

    def parse(self) -> Iterable[str]:
        self.__strip_asm()
        self.__populate()

        result = []

        for instr in self.stripped:
            translated = self.__translate_instr(instr)
            if len(translated) > 0:
                result += [translated]

        return result

    def __create_var(self, name: str) -> int:
        if self.min_free <= self.symbol_table.get(
            "R15"
        ) or self.min_free >= self.symbol_table.get("SCREEN"):
            raise ValueError("Current code will cause memory overflow")
        self.symbol_table.add(name, self.min_free)
        self.min_free += 1
        return self.min_free - 1

    def __translate_A(self, instr: str) -> str:
        arg = instr[1:]
        val: int

        if arg.isdigit():
            val = int(arg)
            if val > 0x7FFF:
                raise ValueError("Size of immediate value is not supported")
        elif self.symbol_table.contains(arg):
            val = self.symbol_table.get(arg)
        else:
            val = self.__create_var(arg)

        return "0" + bin(val)[2:].zfill(15)

    def __translate_C(self, instr: str) -> str:
        dest_i = instr.find("=")

        dest_s = "null"
        jump_s = "null"

        if dest_i >= 0:
            dest_s = instr[:dest_i]
            instr = instr[slice(dest_i + 1, None)]

        jump_i = instr.find(";")

        if jump_i >= 0:
            jump_s = instr[slice(jump_i + 1, None)]
            instr = instr[:jump_i]

        result = (
            "111"
            + self.instr_mapping.get_comp(instr)
            + self.instr_mapping.get_dest(dest_s)
            + self.instr_mapping.get_jump(jump_s)
        )

        return result

    def __translate_instr(self, instr: str) -> str:
        i_type = self.__get_type(instr)

        translated = ""

        if i_type == self.A_INSTRUCTION:
            translated = self.__translate_A(instr)
        elif i_type == self.C_INSTRUCTION:
            translated = self.__translate_C(instr)

        return translated

    def __strip_instr(self, instr: str) -> str:
        if len(instr) <= 0:
            return ""

        comms = instr.find("//")

        if comms == 0:
            return ""

        wo_comms = instr if comms == -1 else instr[0:comms]

        wo_comms = wo_comms.replace(" ", "")
        return wo_comms

    def __strip_asm(self) -> None:
        for instr in self.asm:
            s_instr = self.__strip_instr(instr)
            if s_instr == "":
                continue
            self.stripped += [s_instr]

    def __get_type(self, instr: str) -> int:
        if instr[0] == "(":
            return self.LABEL
        elif instr[0] == "@":
            return self.A_INSTRUCTION
        return self.C_INSTRUCTION

    def __populate_one(self, instr: str, addr: int, i_type: int) -> None:
        if i_type == self.LABEL:
            self.symbol_table.add(instr[slice(1, instr.find(")"))], addr)

    def __populate(self) -> None:
        addr = 0
        for instr in self.stripped:
            i_type = self.__get_type(instr)
            self.__populate_one(instr, addr, i_type)
            if i_type != self.LABEL:
                addr += 1

    def clean(self) -> None:
        self.init_parser()

    def print_table(self) -> None:
        self.symbol_table.print_table()
