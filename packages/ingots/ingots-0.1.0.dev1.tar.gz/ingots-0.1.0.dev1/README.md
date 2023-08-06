# Ingots.

The asynchronous framework for developing web-services.

## Development flow

The project uses the **[GitHub-flow](https://habr.com/post/189046/)** with release branches. It's simpler flow than the `git-flow`.

Briefly. All activities (development, review, testing) execute in branches.
The `main` branch contains current development version and unreleased features.
Release branches start from the `main` branch. Name pattern for releases branches is `release/<magor>.<minor>`.
Main aim for using releases branches to allow support these releases in the future.
All bugfixes for released version have to execute in correspond releases branches.
One major note: bugfix doesn't have to break backward compatibility in the affected versions.
Prefer way for bugfix is the following: need to fix a bug in the `main` branch and move a fix commit down to all supported releases using the `cherry-pick` feature. 
Of course, after that need to prepare new patch versions for all affected releases.

During development and review stages, developer can make commits to branch as many as possible.
After the review phase developer have to squash all commits to one and push to branch with `force` mode.

During the testing phase developer and qa-engineer have to check constantly that development branch is actual from the `main` branch or releases branches.
After testing phase, a commit have to be merged with the `--fast-forward-only` merging strategy.

## Version identification

The package version identification is based on [PEP-440](https://www.python.org/dev/peps/pep-0440/) and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Backward compatibility supports for public API only.
Public API is a part of package functionality which enabled to import and call directly from descendant-s projects.
As a rule, public API is set all interfaces / bases classes with their methods which the package provides.
So, package maintainers can break functions / methods signatures in private part without making a new major version.
To break backward compatibility are:
* to add new required (positional) parameters,
* to rename parameters,
* to delete parameters,


## For developers

Clone a repository:
```bash
mkdir ingots-libs
cd ingots-libs
git clone https://github.com/ABKorotky/ingots.git
cd ingots
```

Prepare a virtual environment:
```bash
virtualenv .venv --python=python3.8
source .venv/bin/activate
pip install -r requirements.txt
```

Prepare repository hooks
```bash
pip install pre_commit
pre-commit install
```

Configure the Sphinx tool

Please, use the following page for configuring the Sphinx documentation generator: [Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)
```bash
pip install sphinx
sphinx-build -b html docs docs/build -v
```

Using the tox tool
```bash
pip install tox
```

Use configured tox tool for several activities.

`tox -e reformat` - auto reformat code by black tool, makes ordering import too.

`tox -e cs` - checks code style by PEP8.

`tox -e ann` - checks annotations of types by mypy.

`tox -e utc` - runs unittests with coverage tool.

`tox -e report` - builds coverage report for the project.

`tox -e doc` - builds a package documentation.

`tox -e build` - builds a package form current branch / tag / commit. Set the INGOTS_VERSION_SUFFIX virtual variable for specify package suffix.

`tox -e upload` - uploads package to PyPI index. Set the PYPI_REPOSITORY_ALIAS virtual variable for specify PyPI destination.

Calling tox without parameters will execute the following steps: **cs**, **ann**, **utc** and **report**.
