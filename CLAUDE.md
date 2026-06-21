# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an empty project directory. The repository currently contains only a `test.txt` file with the content "test".

## Project Structure

```
project1/
  test.txt            # Contains: "test"
  hello.py            # Example script for testing slash commands
 .claude/
    settings.json     # Claude Code hook configuration
```

## Development Setup

No build, lint, or test commands exist for this project as it is empty.

### Running Scripts via Slash Commands

The project has a hook configured in `.claude/settings.json` that allows running scripts from this directory:

```bash
/run <scriptname>
```

Example: `/run hello` will execute `hello.py` from the project directory.

## Notes

When adding code to this repository:
- This project has no existing framework, dependencies, or conventions
- No README.md or other documentation files exist
- No Cursor rules, Copilot rules, or other IDE configurations exist
