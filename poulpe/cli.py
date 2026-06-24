import argparse
import sys
from pathlib import Path

from poulpe.aliases import load_aliases, resolve_alias
from poulpe.completion import generate_setup_script, handle_completion
from poulpe.discovery import discover_commands
from poulpe.runner import run_command

ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = ROOT / "commands"
ALIASES_FILE = ROOT / "aliases.yaml"
ENV_FILE = ROOT / ".env"


class _PoulpeParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        if self.epilog:
            sys.stderr.write(f"\n{self.epilog}\n\n")
        self.exit(2, f"{self.prog}: error: {message}\n")


def build_parser(registry: dict) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="poulpe",
        description="Unified CLI hub for custom commands",
    )
    subparsers = parser.add_subparsers(dest="group", help="Command group")

    subparsers.add_parser("aliases", help="List all aliases")

    for group_name, commands in registry.items():
        group_parser = subparsers.add_parser(group_name, help=f"{group_name} commands")
        cmd_subparsers = group_parser.add_subparsers(dest="command", help="Command")
        cmd_subparsers._parser_class = _PoulpeParser
        for cmd_name, cmd in commands.items():
            epilog = None
            if cmd.examples:
                epilog = "examples:\n" + "\n".join(f"  {ex}" for ex in cmd.examples)
            cmd_parser = cmd_subparsers.add_parser(
                cmd_name,
                help=cmd.description,
                epilog=epilog,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
            for arg in cmd.args:
                names = [arg.name]
                if arg.short:
                    names.append(arg.short)
                kwargs = {"help": arg.help}
                if arg.required:
                    kwargs["required"] = True
                if arg.choices:
                    kwargs["choices"] = arg.choices
                if arg.default is not None:
                    kwargs["default"] = arg.default
                if arg.nargs is not None:
                    kwargs["nargs"] = arg.nargs
                kwargs.setdefault("default", None)
                cmd_parser.add_argument(*names, **kwargs)

    return parser


def main():
    registry = discover_commands(COMMANDS_DIR)
    aliases = load_aliases(ALIASES_FILE)

    if len(sys.argv) >= 2 and sys.argv[1] == "--complete":
        handle_completion(registry, aliases)

    if len(sys.argv) >= 2 and sys.argv[1] == "--setup-completion":
        shell = sys.argv[2] if len(sys.argv) > 2 else "zsh"
        print(generate_setup_script(shell))
        sys.exit(0)

    raw_args = sys.argv[1:]
    raw_args = resolve_alias(raw_args, aliases)

    parser = build_parser(registry)

    if not raw_args:
        parser.print_help()
        sys.exit(0)

    if raw_args[0] == "aliases":
        if not aliases:
            print("No aliases configured.")
        else:
            for alias, target in sorted(aliases.items()):
                print(f"  {alias} -> {target}")
        sys.exit(0)

    group = raw_args[0]
    if group not in registry:
        parser.print_help()
        sys.exit(1)

    if len(raw_args) < 2:
        parser.parse_args(raw_args + ["--help"])
        sys.exit(0)

    cmd_name = raw_args[1]
    if cmd_name not in registry[group]:
        parser.parse_args(raw_args[:1] + ["--help"])
        sys.exit(1)

    cmd = registry[group][cmd_name]
    parsed = parser.parse_args(raw_args)
    parsed_vars = {k: v for k, v in vars(parsed).items() if k not in ("group", "command") and v is not None}
    sys.exit(run_command(cmd.path, parsed_vars, ENV_FILE))


if __name__ == "__main__":
    main()
