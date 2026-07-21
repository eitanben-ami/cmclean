# cmclean

A comment-structure linter for source trees. It scans source files and flags commented debris before it accumulates: TODOs/FIXMEs/HACKs, author plaques, suspicious one-liners, excessively long comments, and blocker-style remarks.

## About

`cmclean` is a language-agnostic static-analysis helper for codebases. It flags problematic comment patterns across supported file types, including Python, JavaScript/TypeScript, Markdown, and JSON/YAML/TOML. It is not a full linter; its job is *comment hygiene*.

## Features

- Detect TODO-like debris: `TODO`, `FIXME`, `HACK`, `XXX`
- Detect author plaques: `@author`, `@created by`, `@written by`
- Detect suspicious debris: weird symbols, oddisms
- Detect blame/blocker-style remarks: `@blame`, `@debugger`, `@temp`, `@workaround`
- Detect excessively long comments above configurable length
- Multi-language file awareness across `.py`, `.js`, `.ts`, `.tsx`, `.md`, `.yaml`, `.yml`, `.json`, `.toml`
- JSON or human-friendly text output

## Installation

```bash
python -m pip install cmclean
```

## Usage

```bash
cmclean /path/to/project
cmclean /path/to/project --json
```

### Exit codes

- `0` No questionable comments found
- `1` Issues found or bad invocation

## Project structure

```
cmclean/
├── src/cmclean/
│   ├── __init__.py
│   ├── cli.py
│   ├── engine.py
│   └── models.py
├── tests/
│   └── test_cmclean.py
├── pyproject.toml
└── README.md
```

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

## Tags / keywords

comment linter, clean code, static analysis, cli, todo, developer tooling
