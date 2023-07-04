from typer import Option, Typer, echo

from n2t.infra import InterpreterProgram

cli = Typer(
    name="Nand 2 Tetris Software",
    no_args_is_help=True,
    add_completion=False,
)


@cli.command("execute", no_args_is_help=True)
def interpret(file: str, cycles: int = Option()) -> None:
    echo(f"Interpreting {file}")
    InterpreterProgram.load_from(file, cycles).interpret()
    echo("Done!")


@cli.command("help", no_args_is_help=True)
def interpreter_help() -> None:
    echo("Usage: python -m execute [FILE] --cycles [NUM_CYCLES]")
