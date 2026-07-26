# Documentation

This directory contains architecture and specification guidance for the project.

- `architecture.md`: Core architecture principles and implementation guidance.
- `specs/`: Specification workspace mirrored to repository structure for endpoint-by-endpoint and module-by-module notes.

Quick contributor rules:
- Keep API groups as package folders with `service.py`.
- Keep tests mirrored to source; for multi-file coverage of one source file, use a same-name folder (for example `tests/<group>/service/`).
