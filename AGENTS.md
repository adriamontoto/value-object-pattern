# AGENTS.md

## Project Overview

Value Object Pattern is a typed Python package for building validated value objects and reusable validation primitives.

Key paths:

- `value_object_pattern/models/`: base value-object contracts and collection helpers.
- `value_object_pattern/usables/`: reusable primitive, date, identifier, internet, money, and text value objects.
- `value_object_pattern/validators/`: reusable validation helpers used across value objects.
- `value_object_pattern/errors/`: package-specific validation and integrity errors.
- `value_object_pattern/__init__.py` and package `__init__.py` files: public exports.
- `value_object_pattern/py.typed`: marker that advertises package typing.
- `tests/`: pytest suite organized to mirror `value_object_pattern/`.
- `pyproject.toml`: package metadata and tool configuration.
- `Makefile`: canonical local workflow.

This is a single-package Python project, not a monorepo. It supports Python `>=3.11` and CI tests the configured Python versions.

## Setup Commands

Run commands from the repository root.

- Show available project commands: `make help`
- Create the default virtual environment, install all dependency groups, and install hooks: `make setup`
- Create all configured virtual environments: `make setup-all`
- Install all dependency groups into an existing environment: `make install`
- Install one dependency group: `make install GROUP=test`, `make install GROUP=lint`, `make install GROUP=format`, `make install GROUP=coverage`, `make install GROUP=release`, or `make install GROUP=types`

The Makefile defaults to:

- `UV_BIN=uv`
- `PYTHON_VERSION=3.14`
- `PYTHON_VERSIONS=3.11,3.12,3.13,3.14`
- `PYTHON_VIRTUAL_ENVIRONMENT=.venv$(PYTHON_VERSION)`, so the default environment is `.venv3.14`

If Python 3.14 is unavailable locally, pass a supported version explicitly, for example:

```bash
make setup PYTHON_VERSION=3.13 PYTHON_VIRTUAL_ENVIRONMENT=.venv3.13
```

After setup, activate the environment when useful:

```bash
source .venv3.14/bin/activate
```

There is no database or application server to start.

## Development Workflow

- Prefer the Make targets over ad hoc tool invocations.
- Keep changes scoped to the requested behavior; avoid unrelated cleanup.
- Add or update tests for behavior changes.
- For public API changes, update exports in `value_object_pattern/__init__.py` or package `__init__.py` files as needed.
- Keep `value_object_pattern/py.typed` present so package typing remains advertised.
- This repository currently has no lockfile; avoid introducing dependency lockfile churn unless the task is explicitly about dependency management.

Use this local verification loop for code changes:

```bash
make format
make lint
make test
make coverage
```

For multi-version checks when the interpreters are available:

```bash
make test-all
make coverage-all
```

For documentation-only changes, run the smallest relevant check and state what was skipped if full verification is not needed.

`make clean` removes configured virtual environments and generated files. Treat it as destructive and do not run it unless the task calls for cleanup.

## Testing Instructions

- Run all tests: `make test`
- Run all configured Python versions: `make test-all`
- Run coverage: `make coverage`
- Run all-version coverage: `make coverage-all`
- Run tests directly after setup: `.venv3.14/bin/python3.14 -m pytest --config-file pyproject.toml`
- Run a focused direct test: `.venv3.14/bin/python3.14 -m pytest tests/usables/primitives/string/test_string_value_object.py --config-file pyproject.toml`
- Run a focused test expression: `.venv3.14/bin/python3.14 -m pytest -k "StringValueObject" --config-file pyproject.toml`

If setup used a different `PYTHON_VERSION`, adjust the `.venv3.14/bin/python3.14` path or activate the environment and use `python -m pytest ...`.

Test conventions:

- Tests live under `tests/` and mirror package structure.
- Test files use `test_*.py` naming.
- Existing tests use `pytest.mark.unit_testing`.
- Assertions are plain `assert`; Ruff permits `assert` in test files.
- Keep generated-data and validation tests deterministic. Use fixed values when asserting exact messages, primitive output, or formatting.

Coverage is configured in `pyproject.toml` with branch coverage enabled for `value_object_pattern`. CI coverage reporting uses a 100% threshold, so consider uncovered branches and failure paths when changing behavior.

## Code Style

The canonical style is defined in `pyproject.toml`.

- Format with Ruff: `make format`
- Lint and type-check with Ruff and mypy: `make lint`
- Ruff line length is `120`.
- Ruff format uses single quotes and spaces for indentation.
- Mypy runs in strict mode.
- Imports are sorted by Ruff/isort with `value_object_pattern` as first-party.
- Public modules and classes use docstrings following the existing PEP 257 style.
- Keep runtime code compatible with Python `>=3.11`.
- When using `typing.override`, preserve the existing compatibility pattern that imports from `typing` on Python 3.12+ and from `typing_extensions` otherwise.

Architecture conventions:

- New value objects should follow the existing value-object model style and validation flow.
- `create()` and validators should preserve existing explicit-value behavior where nearby code does so.
- Put reusable validation logic under the closest existing validators module.
- Add public exports only when the value object is intended for package users.
- Keep static data files under the relevant `utils/` package.
- When public APIs, import paths, reusable value-object behavior, catalog entries, examples, or documented package-version
  facts change, update the installable Agent Skill under `skills/value-object-pattern/` in the same change.

## Build And Release

- Build distributions locally: `make build-code`
- Build output is written to `dist/`.
- Do not publish packages manually from an agent session.
- Releases are managed in CI on pushes to `master` using `python-semantic-release`.
- Version is read from `value_object_pattern/__init__.py`.
- Changelog generation uses templates in `docs/changelog_template/`.

Semantic-release is configured for Conventional Commits:

- Minor release tags: `feat`
- Patch release tags: `fix`, `perf`, `build`
- Other conventional types such as `docs`, `test`, `refactor`, and `ci` may be valid for commit hygiene but do not bump by default according to the local semantic-release config.

## Security

- Run dependency audit when security or dependency changes are involved: `make audit`
- Run secret scanning when touching configuration, CI, release, or credential-adjacent files: `make secrets`
- Never read or print secrets. Do not inspect `.env` files; use examples or placeholders instead.
- Security vulnerabilities should be handled through GitHub Security Advisories, not public issues.

## CI And Pull Requests

CI runs on pushes and pull requests targeting `master`, plus a scheduled daily run. The main checks are:

- Tests and coverage on Ubuntu and Windows across configured Python versions
- Format check with `make format` followed by a clean working tree assertion
- Lint and type check with `make lint`
- CodeQL analysis
- Secret scanning
- Dependency audit
- Release and PyPI publish jobs on successful pushes to `master`

Before opening or updating a PR, run:

```bash
make format
make lint
make test
make coverage
```

PRs should use `.github/pull_request_template.md`. Commits are expected to follow Conventional Commits and the repository accepts signed and signed-off commits.

## Agent Notes

- Inspect the relevant files before editing.
- Preserve existing project structure and naming.
- Prefer small, reviewable diffs.
- Do not create, switch, delete, or rewrite Git branches unless explicitly asked.
- Do not commit unless explicitly asked.
- Do not run externally visible release, publish, or pull-request automation from a local agent session.
