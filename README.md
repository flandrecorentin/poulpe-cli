# poulpe-cli

Unified CLI hub for powerful custom commands.

## Prerequisites

- Python >= 3.9
- [uv](https://docs.astral.sh/uv/)

## Installation

Clone the repository, create a virtual environment, and install:

```bash
git clone <repo-url> ~/workspace/poulpe-cli
cd ~/workspace/poulpe-cli
uv venv
uv pip install -e .
```

Copy the environment file and fill in your values:

```bash
cp .env.example .env
```

Add the following to your `~/.zshrc`:

```bash
# poulpe-cli
export PATH="$HOME/workspace/poulpe-cli/bin:$PATH"
alias p="poulpe"
eval "$(poulpe --setup-completion zsh)"
compdef p=poulpe
```

Then reload your shell:

```bash
source ~/.zshrc
```

## Verify

```bash
poulpe --help
```

## Usage

```bash
poulpe <group> <command> [args]
```

List available aliases:

```bash
poulpe aliases
```
