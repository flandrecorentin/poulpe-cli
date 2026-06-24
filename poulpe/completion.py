import sys
from pathlib import Path


def handle_completion(registry: dict, aliases: dict):
    words = sys.argv[2:]
    completions = _get_completions(words, registry, aliases)
    for c in completions:
        print(c)
    sys.exit(0)


def _get_completions(words: list[str], registry: dict, aliases: dict) -> list[str]:
    groups = list(registry.keys()) + ["aliases"]

    if len(words) == 0:
        return sorted(groups)

    partial = words[-1] if words else ""
    resolved_first = aliases.get(words[0], words[0]) if words else ""
    resolved_parts = resolved_first.split()

    if len(words) == 1:
        return sorted(c for c in groups if c.startswith(partial))

    group = resolved_parts[0]
    if group not in registry:
        return []

    if len(resolved_parts) == 2 and len(words) == 2:
        cmd_from_alias = resolved_parts[1]
        if cmd_from_alias in registry[group]:
            cmd = registry[group][cmd_from_alias]
            return sorted(a.name for a in cmd.args if a.name.startswith(partial))

    if len(words) == 2:
        commands = list(registry[group].keys())
        return sorted(c for c in commands if c.startswith(partial))

    if len(words) >= 3:
        cmd_name = words[1]
        if cmd_name in registry[group]:
            cmd = registry[group][cmd_name]
            return sorted(a.name for a in cmd.args if a.name.startswith(partial))

    return []


def generate_setup_script(shell: str) -> str:
    if shell == "zsh":
        return _zsh_setup()
    return _bash_setup()


def _zsh_setup() -> str:
    return """\
if ! type compdef &>/dev/null; then
    autoload -Uz compinit && compinit
fi

_poulpe() {
    local -a completions
    completions=(${(f)"$(poulpe --complete "${(@)words[2,CURRENT]}")"})
    compadd -- "${completions[@]}"
}

compdef _poulpe poulpe"""


def _bash_setup() -> str:
    return """\
_poulpe() {
    local cur
    cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(poulpe --complete "${COMP_WORDS[@]:1}"))
}

complete -F _poulpe poulpe"""
