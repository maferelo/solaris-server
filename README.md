# solaris-python

Solaris python services

## Installation

### Windows

Coming soon

### UNIX/MacOS

#### Install [Homebrew](https://brew.sh/)

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install [Docker](https://docs.docker.com/), [Vscode](https://code.visualstudio.com/docs), [python-tk](https://docs.python.org/es/3/library/tkinter.html), and [Gpg-suite](https://gpgtools.org/)

```sh
    brew install --cask docker visual-studio-code gpg-suite
```

```sh
    brew install python-tk
```

#### Setup git with GPG signing

##### Configure git

```sh
    git config --global user.name "<your-name>"
    git config --global user.email "<your-email>"
```

##### Generate a new GPG key [^1]

```sh
    gpg --full-generate-key
```

##### Configure key in git [^1]

```sh
    gpg --full-generate-key
    gpg --list-secret-keys --keyid-format LONG
    gpg --armor --export <KEY_ID>
    git config --global user.signingkey <KEY_ID>
    git config --global commit.gpgsign true
```

##### [Configure key in github](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account)

[^1]: [Generating a new GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key)

#### Install [Pyenv](https://github.com/pyenv/pyenv)[^2] [^3]

```sh
    brew install pyenv
    alias brew='env PATH="${PATH//$(pyenv root)\/shims:/}" brew'
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

[^2]: [Pyenv Homebrew in macOS](https://github.com/pyenv/pyenv#homebrew-in-macos)

[^3]: [Set up your shell environment for Pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

#### Install [Python 3](https://docs.python.org/3/)

```sh
    pyenv install
```

#### Install [Poetry](https://python-poetry.org/docs/#installation)

```sh
    curl -sSL https://install.python-poetry.org | python3 - --version 1.6.1
    poetry completions bash >> ~/.bash_completion
```

#### Install dependencies

```sh
    poetry install
```

## Branch and commit naming conventions

### category

- feat
- fix
- refactor
- chore

```sh
    git commit -m '<category>: <description>; <description>'
```

#### Example

- You need to fix a bug: git branch fix/issue-342/button-overlap-form-on-mobile[^4]
  
[^4]: [A Simplified Convention for Naming Branches and Commits in Git](https://dev.to/varbsan/a-simplified-convention-for-naming-branches-and-commits-in-git-il4)

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
    make run
```

### Run tests

```sh
    poetry run pytest
```

### Add dependencies

```sh
    poetry add <dependency>@<version>
```

### Update dependencies

```sh
    poetry update
```

### Remove dependencies

```sh
    poetry remove <dependency>
```

## Deployment

### Create Heroku app

```sh
    heroku create <app-name>
```

### Enable container registry

```sh
    heroku container:login
```

### Build image

```sh
    docker build -t registry.heroku.com/<app-name>/<process-type> .
```

Make sure to replace <app-name> with the name of the Heroku app that you just created and <process-type> with web since this will be for a [web process](https://devcenter.heroku.com/articles/procfile#the-web-process-type) [^5].
  
[^5]: [Deploying and Hosting a Machine Learning Model with FastAPI and Heroku](https://testdriven.io/blog/fastapi-machine-learning/)

### Push image

```sh
    docker push registry.heroku.com/<app-name>/<process-type>
```

### Release image

```sh
    heroku container:release -a <app-name> <process-type>
```

### Check logs

```sh
    heroku logs --tail
```

### Open app

```sh
    heroku open
```

