This devcontainer sets up a Python 3.11 development environment for the repository.

How to use

- Open this repository in VS Code.
- From the Command Palette choose: Remote-Containers: Reopen in Container.

What it does

- Builds a Docker container with Python 3.11 and `git` installed.
- Runs `pip install -e '.[test]'` after creating the container to install the package and test extras (pytest, pytest-cov, pytest-asyncio).

Run tests inside the container

```bash
pytest -q
```
