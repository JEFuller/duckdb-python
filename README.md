<div align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/duckdb/duckdb/refs/heads/main/logo/DuckDB_Logo-horizontal.svg">
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/duckdb/duckdb/refs/heads/main/logo/DuckDB_Logo-horizontal-dark-mode.svg">
    <img alt="DuckDB logo" src="https://raw.githubusercontent.com/duckdb/duckdb/refs/heads/main/logo/DuckDB_Logo-horizontal.svg" height="100">
  </picture>
</div>
<br />
<p align="center">
  <a href="https://discord.gg/tcvwpjfnZx"><img src="https://shields.io/discord/909674491309850675" alt="Discord" /></a>
  <a href="https://pypi.org/project/duckdb/"><img src="https://img.shields.io/pypi/v/duckdb.svg" alt="PyPI Latest Release"/></a>
</p>
<br />
<p align="center">
  <a href="https://duckdb.org">DuckDB.org</a>
  |
  <a href="https://duckdb.org/docs/stable/guides/python/install">User Guide (Python)</a>
  -
  <a href="https://duckdb.org/docs/stable/clients/python/overview">API Docs (Python)</a>
</p>

# DuckDB: A Fast, In-Process, Portable, Open Source, Analytical Database System

* **Simple**: DuckDB is easy to install and deploy. It has zero external dependencies and runs in-process in its host application or as a single binary.
* **Portable**: DuckDB runs on Linux, macOS, Windows, Android, iOS and all popular hardware architectures. It has idiomatic client APIs for major programming languages.
* **Feature-rich**: DuckDB offers a rich SQL dialect. It can read and write file formats such as CSV, Parquet, and JSON, to and from the local file system and remote endpoints such as S3 buckets.
* **Fast**: DuckDB runs analytical queries at blazing speed thanks to its columnar engine, which supports parallel execution and can process larger-than-memory workloads.
* **Extensible**: DuckDB is extensible by third-party features such as new data types, functions, file formats and new SQL syntax. User contributions are available as community extensions.
* **Free**: DuckDB and its core extensions are open-source under the permissive MIT License. The intellectual property of the project is held by the DuckDB Foundation.

## Installation

Install the latest release of DuckDB directly from [PyPI](https://pypi.org/project/duckdb/):

```bash
pip install duckdb
```

Install with all optional dependencies:

```bash
pip install 'duckdb[all]'
```

### This fork's zoneinfo build (without publishing to PyPI)

This branch combines the Python client and engine at `v1.5.6` with the `zoneinfo`
backport. Named time zones use the system IANA timezone database. Native fetched
datetimes now have `zoneinfo.ZoneInfo` objects; use `tzinfo.key` instead of
`tzinfo.zone`.

Build a wheel with the PEP 440 local version `1.5.6+zoneinfo`:

```bash
git submodule update --init --recursive
uv sync --only-group build --no-install-project -p 3.12.13
OVERRIDE_GIT_DESCRIBE=v1.5.6+zoneinfo uv build --wheel --python 3.12.13
```

Install that wheel in another project, without consulting a package index:

```bash
uv pip install --no-index --find-links /absolute/path/to/duckdb-python/dist \
  'duckdb==1.5.6+zoneinfo'
```

For a uv-managed project, use `uv add --python 3.12.13 /absolute/path/to/the-built-wheel.whl`
to record the wheel as a direct dependency. Wheels can also be distributed as
GitHub Release assets or through a private wheel directory. No PyPI upload is
needed. A wheel must match the consumer's Python version, OS, architecture, and
Linux runtime requirements; an Ubuntu-built wheel is not a manylinux wheel.
Use a manylinux/cibuildwheel build for broader Linux distribution.

Download the wheel matching your platform from
[the fork's release assets](https://github.com/JEFuller/duckdb/releases/tag/v1.5.6-zoneinfo),
then install it with `uv add --python 3.12.13 /path/to/downloaded-wheel.whl`.
To pin the version explicitly while retaining that wheel source:

```bash
uv add --python 3.12.13 --no-index 'duckdb==1.5.6+zoneinfo'
```

The release contains CPython 3.12 wheels for macOS ARM64 (macOS 15+),
Linux ARM64/x86_64, and Windows x64/ARM64.
Use the manylinux Linux wheels, built in manylinux 2.28 containers and repaired
with auditwheel for glibc 2.26 or newer. Both architectures are tested on
Ubuntu 20.04, Ubuntu 22.04, and Debian Bookworm using Python 3.12.13.
Verify them with the release's `SHA256SUMS-cp312-manylinux` manifest.
The original Ubuntu 24.04-only Linux wheels remain available, unchanged.
The earlier CPython 3.13 wheels remain available (macOS 26+ for that macOS wheel).
Ubuntu wheels require a compatible glibc runtime and are not manylinux wheels.
On Windows, install `tzdata` separately to provide the IANA timezone database;
it is not bundled in Python or this wheel.

To reference the CPython 3.12 release assets directly in a consuming project's
`pyproject.toml`, merge the following into its existing tables:

```toml
[project]
requires-python = ">=3.12,<3.13"
dependencies = [
    "duckdb==1.5.6+zoneinfo",
    "tzdata; sys_platform == 'win32'",
]

[tool.uv]
environments = [
    "sys_platform == 'darwin' and platform_machine == 'arm64'",
    "sys_platform == 'linux' and platform_machine == 'aarch64'",
    "sys_platform == 'linux' and platform_machine == 'x86_64'",
    "sys_platform == 'win32' and platform_machine == 'AMD64'",
    "sys_platform == 'win32' and platform_machine == 'ARM64'",
]

[tool.uv.sources]
duckdb = [
    { url = "https://github.com/JEFuller/duckdb/releases/download/v1.5.6-zoneinfo/duckdb-1.5.6%2Bzoneinfo-cp312-cp312-macosx_15_0_arm64.whl", marker = "sys_platform == 'darwin' and platform_machine == 'arm64'" },
    { url = "https://github.com/JEFuller/duckdb/releases/download/v1.5.6-zoneinfo/duckdb-1.5.6%2Bzoneinfo-cp312-cp312-manylinux_2_26_aarch64.manylinux_2_28_aarch64.whl", marker = "sys_platform == 'linux' and platform_machine == 'aarch64'" },
    { url = "https://github.com/JEFuller/duckdb/releases/download/v1.5.6-zoneinfo/duckdb-1.5.6%2Bzoneinfo-cp312-cp312-manylinux_2_26_x86_64.manylinux_2_28_x86_64.whl", marker = "sys_platform == 'linux' and platform_machine == 'x86_64'" },
    { url = "https://github.com/JEFuller/duckdb/releases/download/v1.5.6-zoneinfo/duckdb-1.5.6%2Bzoneinfo-cp312-cp312-win_amd64.whl", marker = "sys_platform == 'win32' and platform_machine == 'AMD64'" },
    { url = "https://github.com/JEFuller/duckdb/releases/download/v1.5.6-zoneinfo/duckdb-1.5.6%2Bzoneinfo-cp312-cp312-win_arm64.whl", marker = "sys_platform == 'win32' and platform_machine == 'ARM64'" },
]
```

These sources and resolver environments cover only the five listed platforms. Run
`uv python pin 3.12.13` and `uv sync --python 3.12.13`, then commit `uv.lock`
to retain the wheel URLs and hashes. The wheel ABI covers compatible CPython
3.12 patch releases; the Python pin selects the exact tested interpreter.

The fork-only `Packaging` workflow on branch `v1.5.6-zoneinfo` builds and tests
CPython 3.12 wheels using Python 3.12.13 on all five platforms, retaining them
as Actions artifacts. It never invokes
the PyPI publishing workflow. Release asset uploads are a separate operation.
Dispatch it with `manylinux-only=true` to build only the compatible Linux
CPython 3.12 wheels, auditwheel-repair them, and test the installed artifacts
on the supported Linux runtimes.

## Contributing

See the [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to set up a development environment.
