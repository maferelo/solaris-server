Commit
======================================================================

Setup git with GPG signing (optional)
----------------------------------------------------------------------

On your local machine, if you haven't already done so, setup git with your name and email address::

    git config --global user.name "<your-name>"
    git config --global user.email "<your-email>"

then, generate a GPG key::

    gpg --full-generate-key

retrieve the key ID::

    gpg --list-secret-keys --keyid-format LONG

get the public key::

    gpg --armor --export <KEY_ID>

configure gpg signing and public key in git::

    git config --global commit.gpgsign true
    git config --global user.signingkey <KEY_ID>



Branch naming convention
----------------------------------------------------------------------

Branches are named according to the following convention:

    <type>/<name>

where `<type>` is one of the following:

* `feature`: a new feature
* `bugfix`: a bugfix
* `hotfix`: a hotfix
* `release`: a release
* `support`: a support branch
* `docs`: a documentation branch
* `style`: a style branch
* `refactor`: a refactoring branch
* `test`: a test branch
* `chore`: a chore branch

and `<name>` is a short description of the branch.

For example:

    feature/add-readme-file

    bugfix/fix-typo-in-readme-file

    hotfix/fix-typo-in-readme-file

    release/add-readme-file

    support/add-readme-file

    docs/add-readme-file

    style/add-readme-file

    refactor/add-readme-file

    test/add-readme-file

    chore/add-readme-file

Commit message convention
----------------------------------------------------------------------

Commits are named according to the following convention:

    <type>(<scope>): <description>

where `<type>` is one of the following:

* `feat`: a new feature
* `fix`: a bugfix
* `hotfix`: a hotfix
* `release`: a release
* `support`: a support commit
* `docs`: a documentation commit
* `style`: a style commit
* `refactor`: a refactoring commit
* `test`: a test commit
* `chore`: a chore commit

and `<scope>` is a short description of the scope of the commit, and
`<description>` is a short description of the commit starting with a verb.

For example:

    feat(README): add a README file

    fix(README): fix a typo in the README file

    hotfix(README): fix a typo in the README file

    release(README): add a README file

    support(README): add a README file

    docs(README): add a README file

    style(README): add a README file

    refactor(README): add a README file

    test(README): add a README file

    chore(README): add a README file


