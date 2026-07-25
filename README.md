# cmclean

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python >=3.11](https://img.shields.io/badge/python-%3E%3D3.11-blue.svg)

A comment-structure linter for source trees. It scans source files and flags commented debris before it accumulates: TODOs/FIXMEs/HACKs, author plaques, suspicious one-liners, excessively long comments, and blocker-style remarks.

## About

`cmclean` is a language-agnostic static-analysis helper for codebases. It flags problematic comment patterns across supported file types, including Python, JavaScript/TypeScript, Markdown, and JSON/YAML/TOML. It is not a full linter; its job is *comment hygiene*.

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

## Detectors

- TODO-like debris: `TODO`, `FIXME`, `HACK`, `XXX`
- Author plaque: `@author`, `@created by`, `@written by`
- Suspicious debris: strings containing `@#\$%` and nearby characters
- Excessively long comment: raw comment lines longer than 240 characters
- Blocker-style remark: `@blame`, `@debugger`, `@temp`, `@workaround`

Supported extensions: `.py`, `.js`, `.ts`, `.tsx`, `.md`, `.yaml`, `.yml`, `.json`, `.toml`

## Examples

See [`examples/`](examples/) for sample scans. Run `cmclean examples/` to verify the linter reports no issues against shipped demo files.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

## Contributing

Issues and pull requests are welcome. Please open an issue before larger changes so scope and design can align with the comment-hygiene focus of the tool.

## License

MIT
