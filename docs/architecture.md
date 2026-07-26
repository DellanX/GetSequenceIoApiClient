# Architecture Guidelines

## Purpose

This document defines architectural guidance for future development of `GetSequenceIoApiClient`.

## Core Principles

1. **Typed-first development**
   - Prefer explicit, validated models over loose dictionaries.
   - Keep request/response contracts strongly typed wherever possible.

2. **Pydantic-first for API endpoint contracts**
   - For endpoint inputs (query params, path/body payloads), use Pydantic models.
   - For endpoint outputs (response data models), use Pydantic models.
   - Use aliases to map API-native camelCase fields to Pythonic snake_case fields.
   - Preserve schema compatibility while improving local type safety.

3. **Composable endpoint modules**
   - Keep endpoint logic modular by resource area (accounts, rules, activity, audit logs, etc.).
   - Reuse shared transport/resource helpers instead of duplicating request plumbing.

4. **Validation at boundaries**
   - Validate payloads at API boundaries (incoming response data, outgoing request models).
   - Keep core business logic working with validated, typed structures.

5. **Backward-compatible serialization shape**
   - Continue serializing outbound payloads using API field names (`by_alias=True`).
   - Avoid silent shape drift in request/response fields.

## API Endpoint Development Standard

For each new or updated endpoint:

1. Define request param/body models in typed form (Pydantic).
2. Define response models in typed form (Pydantic).
3. Parse API responses directly into models via `from_dict` / `model_validate`.
4. Serialize outgoing payloads through typed model dumps (alias-aware).
5. Add/adjust tests to verify:
   - field alias mapping,
   - response parsing,
   - endpoint parameter serialization,
   - expected model types returned by service methods.

## Practical Rule of Thumb

If an endpoint currently uses a generic map shape, treat it as technical debt and prioritize migration to an explicit Pydantic model during the next touch of that endpoint.
