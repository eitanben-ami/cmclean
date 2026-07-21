# cmclean documentation

## Scoping rules

- Supported extensions: `.py`, `.js`, `.ts`, `.tsx`, `.md`, `.yaml`, `.yml`, `.json`, `.toml`
- One detector is reported per line; line-level comment detection is conservative.
- Long-comment detection counts raw line length; it does not expand multiline block comments as hot blobs.

## Detector kinds

- `TODO-like debris`: `TODO`, `FIXME`, `HACK`, `XXX`
- `Author plaque`: `@author`, `@created by`, `@written by`
- `Suspicious debris`: strings containing `@#\$%` and nearby characters
- `Excessively long comment`: raw comment lines longer than 240 characters
- `Blocker-style remark`: `@blame`, `@debugger`, `@temp`, `@workaround`

## Configuration

CLI:

```
cmclean /path/to/project --json
```

Python:

```python
from cmclean.engine import analyze
issues = analyze("/path/to/project")
print(len(issues))
```
