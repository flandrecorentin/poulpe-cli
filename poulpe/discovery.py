from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class CommandArg:
    name: str
    required: bool
    help: str = ""
    short: str = ""
    choices: list = field(default_factory=list)
    nargs: object = None
    default: object = None


@dataclass
class Command:
    name: str
    group: str
    path: Path
    description: str = ""
    examples: list[str] = field(default_factory=list)
    args: list[CommandArg] = field(default_factory=list)


def _load_metadata(script_path: Path) -> tuple[str, str, list[CommandArg]]:
    yaml_path = script_path.with_suffix(".yaml")
    if not yaml_path.is_file():
        return "", "", []
    try:
        with open(yaml_path) as f:
            data = yaml.safe_load(f)
    except (OSError, yaml.YAMLError):
        return "", "", []
    if not isinstance(data, dict):
        return "", "", []
    description = data.get("description", "")
    raw_examples = data.get("examples", data.get("example", []))
    if isinstance(raw_examples, str):
        examples = [raw_examples]
    elif isinstance(raw_examples, list):
        examples = raw_examples
    else:
        examples = []
    args = []
    for arg_data in data.get("args", []):
        if not isinstance(arg_data, dict) or "name" not in arg_data:
            continue
        args.append(CommandArg(
            name=arg_data["name"],
            required=arg_data.get("required", False),
            help=arg_data.get("help", ""),
            short=arg_data.get("short", ""),
            choices=arg_data.get("choices", []),
            nargs=arg_data.get("nargs"),
            default=arg_data.get("default"),
        ))
    return description, examples, args


def discover_commands(commands_dir: Path) -> dict[str, dict[str, Command]]:
    registry: dict[str, dict[str, Command]] = {}
    if not commands_dir.is_dir():
        return registry
    for group_dir in sorted(commands_dir.iterdir()):
        if not group_dir.is_dir() or group_dir.name.startswith("."):
            continue
        group_name = group_dir.name
        registry[group_name] = {}
        for cmd_file in sorted(group_dir.iterdir()):
            if cmd_file.is_file() and not cmd_file.name.startswith(".") and cmd_file.suffix != ".yaml":
                description, examples, args = _load_metadata(cmd_file)
                registry[group_name][cmd_file.name] = Command(
                    name=cmd_file.name,
                    group=group_name,
                    path=cmd_file,
                    description=description or f"Run {cmd_file.name}",
                    examples=examples,
                    args=args,
                )
    return registry
