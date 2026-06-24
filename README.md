# poulpe-cli

Unified CLI hub to facilitate my reccurent commands/tasks.

## Prerequisites

- Python >= 3.9
- [uv](https://docs.astral.sh/uv/) or [pip](https://pip.pypa.io/en/stable/getting-started/)

## Installation

Clone the repository, create a virtual environment, and install:

```bash
git clone git@github.com:flandrecorentin/poulpe-cli.git
cd poulpe-cli
```

Create the virtual environment, and install dependencies:

```bash
uv venv || python3 -m venv .venv
uv pip install -e . || pip install -e .
```

Copy the environment file and fill in your values for powerful usage:

```bash
cp .env.example .env
```

Add the following to your `~/.zshrc` (add the poulpe command and enable the completion)

```bash
# --- poulpe-cli
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
