import os
import subprocess
import sys
from pathlib import Path


def load_env(env_file: Path) -> dict[str, str]:
    env = os.environ.copy()
    if not env_file.is_file():
        return env
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                if key:
                    env[key] = value
    return env


def run_command(script_path: Path, parsed_vars: dict, env_file: Path) -> int:
    env = load_env(env_file)

    for key, value in parsed_vars.items():
        env_key = f"POULPE_{key.upper()}"
        if isinstance(value, list):
            env[env_key] = " ".join(str(v) for v in value)
        else:
            env[env_key] = str(value)

    shebang = ""
    try:
        with open(script_path) as f:
            first_line = f.readline().strip()
            if first_line.startswith("#!"):
                shebang = first_line
    except (OSError, UnicodeDecodeError):
        pass

    if "python" in shebang:
        cmd = [sys.executable, str(script_path)]
    else:
        cmd = ["bash", str(script_path)]

    result = subprocess.run(cmd, env=env)
    return result.returncode
