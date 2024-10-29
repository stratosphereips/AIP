# Contributing

All contributions are welcomed. Thank you for taking the time to contribute to this project! 

## What branch should you base your contribution on?

Generally, base your contribution on the `development` branch.

   
## Naming Git branches for Pull Requests

To keep the Git history clean and facilitate the revision of contributions we 
ask all branches to follow concise namings. These are the branch-naming patterns
to follow when contributing:

- bugfix-<>:        pull request branch, contains one bugfix,
- docs-<>:          pull request branch, contains documentation work,
- enhance-<>:       pull request branch, contains one enhancement (not a new feature, but improvement nonetheless)
- feature-<>:       pull request branch, contains a new feature,
- refactor-<>:      pull request branch, contains code refactoring,


## Tests

Our project uses `unittest` for testing. To ensure code quality and maintainability, please run all tests before opening a pull request.

## Creating a pull request

Commits:
- Commits should do one thing. Keep it simple.
- Commit messages should be easily readable, in imperative style ("Fix memory leak in...", not "FixES mem...")

Pull Requests:
- If you have developed multiple features and/or bugfixes, create separate
    branches for each one of them, and request merges for each branch;
- The cleaner your code/change/changeset is, the faster it will be merged.

## How can you contribute?

* Report bugs
* Suggest features and ideas
* Pull requests with a solved GitHub issue and a new feature
* Pull request with new content.


## Persistent Git Branches

The following git branches are permanent in the repository:

- `main`: contains the stable version of the repository.
- `development`: contains the latest version of AIP with the latest changes. **All new features should be based on this branch.**
