from pathlib import Path

import yaml


def load_aliases(aliases_file: Path) -> dict[str, str]:
    if not aliases_file.is_file():
        return {}
    with open(aliases_file) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def resolve_alias(args: list[str], aliases: dict[str, str]) -> list[str]:
    if not args:
        return args
    key = args[0]
    if key in aliases:
        expanded = aliases[key].split()
        args = expanded + args[1:]
    if len(args) >= 2 and args[1] in aliases:
        expanded = aliases[args[1]].split()
        args = [args[0]] + expanded + args[2:]
    return args
