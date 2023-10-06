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
