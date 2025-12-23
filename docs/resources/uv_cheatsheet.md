# uv_cheatsheet.md

## Project Setup & Management
```sh
# Creates a new project directory with pyproject.toml and main.py
uv init <project-name>
```

```sh
# Initializes uv in an existing project directory
uv init
```

```sh
# Installs dependencies from pyproject.toml or uv.lock, creating/updating the virtual environment
uv sync
```

```sh
# Updates the uv.lock file, creating reproducible builds
uv lock
```

## Dependency Management
```sh
# Adds a package as a main dependency
uv add <package-name>=
```

```sh
# Adds a development dependency
uv add --dev <package-name>
```

```sh
# Adds a package from a Git repository.
uv add git+<url>
```

```sh
# Removes a dependency Running Scripts & Tools
uv remove <package-name> 
```

```sh
# Runs a Python script within the project's environment
uv run <script.py>
```

```sh
# Runs a script with an extra package available (installs it if needed)
uv run <script.py> --with <package>
```

```sh
# Executes Python with specified packages in the environment
uv run -- python <script.py>
```

```sh
# Drops you into a shell within the virtual environment 
uv run bash 
# or 
uv run cmd
```

## Tool Management ( Ruff, etc.)
```sh
# Installs the ruff linter
uv tool install ruff
```

```sh
# Lists installed uv tools
uv tool list
```

```sh
# Upgrades ruff
uv tool upgrade ruff
```

```sh
# Upgrades all managed tools 
uv tool upgrade --all
```
