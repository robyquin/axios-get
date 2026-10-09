# CONTRIBUTING

Thank you for your interest in contributing! Please follow these simple rules to keep the project organized and collaborative.

## Prerequisites

- Python 3.13+

## Report a bug

This is the link to submit a [new issue](https://github.com/robyquin/axios-get/issues/new).

Please check if the issue has already been fixed or if it is already currently discussed in an existing issue.

Don't forget to mention :

- a more or less precise protocol to reproduce the bug

When opening an issue, include:

- Environment details (OS, Python version, project version)
- Steps to reproduce
- Expected behavior
- Observed behavior

## Suggest a feature

You can also submit a [new issue](https://github.com/robyquin/axios-get/issues/new) to suggest a change or to make a feature request.

Please make sure the feature you ask for is not too specific to your use case and make sense in the project.

Please include:

- Why the feature is useful
- Who benefits from it
- How it integrates into the project

## Submit your own changes

Feel free to fork **axios-get** to make your own changes.

### Pull Request Rules

- Keep PRs small and focused
- Clearly describe the problem being solved
- Link any related issues
- Update documentation if needed
- Ensure code is formatted and linted

### Code Style

- Use **flake8** to follow _PEP8_
  - `pip install flake8 flake8-pyproject`
- Use **pydoclint** to follow _PEP257_
  - `pip install pydoclint`
- Avoid overly long functions
- Use clear and meaningful names
- Try to use explicit variable names
- Try to comment your code if what it does it not obvious
<!-- - Use Black for formatting -->

### Tests

- Use **pytest** and ensure it runs without errors
  - `pip install pytest`
- Add tests for every new feature in _test_ folder

### Workflow

Here is a brief description of the `fork and merge request` workflow (or at least my interpretation of it) :

- Fork the project to get a copy of which you are the owner
- Don't push commits in your main branch, it is easier to use your main branch to stay up to date with original project
- Create a branch from your up-to-date main to make a bunch of commits **related to one single topic**. Name the branch explicitly.
- Implement your changes
- Ensure all tests pass
- Create a merge request from this branch to main branch of the original project with a clear description of what you did

Here is a memo of git commands to run after having forked the project:

```bash
git clone https://github.com/robyquin/axios-get.git axios-get
cd axios-get

# on your local branch main, to get changes from main branch of original project :
git pull https://github.com/robyquin/axios-get main

# create a branch to work on a future merge request
git checkout -b new_feature1
# make changes then commit
git commit -a -m "beginning to implement my new feature"
# continue developing
git commit -a -m "new feature is now ready"
# push it to your repo
git push origin new_feature1
# now you can make your merge request ^^ !

# you want to update your main branch
git checkout main
git pull https://github.com/robyquin/axios-get main
```

Optional:

```bash
# you've started to work on new_feature1 and in the meantime,
# the main branch of original project integrated some new stuff.
# If you want to get the new stuff in your new_feature1 branch :
git checkout main
git pull https://github.com/robyquin/axios-get main
git checkout new_feature1
# rebasing a branch means trying to put the commits of local branch on top of requested branch
# in this example : remove your changes, get new stuff from main, put your changes on top !
git rebase main
# if there is no conflict between your changes
# and the new stuff in main branch of original project
# the rebase will go just fine.
# You can then continue developing on your new_feature1 branch
```
