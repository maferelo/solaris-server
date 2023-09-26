# solaris-python

Solaris python services

## Prerequisites

- [Python 3.11](https://docs.python.org/3/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)
- [brew](https://brew.sh/)

## Installation

### Windows

Coming soon

### UNIX/MacOS

1. Install [Homebrew](https://brew.sh/):

    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Install [Docker](https://docs.docker.com/) and [Vscode](https://code.visualstudio.com/docs):

    ```sh
        brew install --cask docker visual-studio-code
    ```

3. Install [Pyenv](https://github.com/pyenv/pyenv)[^1] [^2]:

    ```sh
        brew install pyenv
        alias brew='env PATH="${PATH//$(pyenv root)\/shims:/}" brew'
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
        echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
    ```

    [^1]: [Pyenv Homebrew in macOS](https://github.com/pyenv/pyenv#homebrew-in-macos)

    [^2]: [Set up your shell environment for Pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

4. Install [Python 3](https://docs.python.org/3/):

    ```sh
        pyenv install
    ```

5. Install [Poetry](https://python-poetry.org/docs/#installation):

    ```sh
        curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1
        poetry completions bash >> ~/.bash_completion
    ```

6. Install dependencies:

    ```sh
        poetry install
    ```

## Branching naming conventions

```sh
git branch <category/reference/description-in-kebab-case>
```

### category

- feat
- fix
- refactor
- chore

#### Example

- You need to fix a bug: git branch fix/issue-342/button-overlap-form-on-mobile[^3]
  
[^3]: [A Simplified Convention for Naming Branches and Commits in Git](https://dev.to/varbsan/a-simplified-convention-for-naming-branches-and-commits-in-git-il4)

### Commit naming conventions

```sh
git commit -m '<Action something; Action some other things>'
```

### Resources

- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)

### Troubleshooting

- Pyenv not loading environment on vs code: ctrl + shift + p -> Python: Clear Workspace Interpreter Setting -> Restart vs code

## Usage

### Run

```sh
    poetry run python main.py
```

### Run tests

```sh
    poetry run pytest
```

### Add dependencies

```sh
    poetry add <dependency>
```

### Update dependencies

```sh
    poetry update
```

### Remove dependencies

```sh
    poetry remove <dependency>
```
