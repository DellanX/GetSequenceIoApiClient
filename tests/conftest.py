"""Pytest configuration helpers for the workspace tests.

Ensure the workspace root is on sys.path so `GetSequenceIoApiClient` can be
imported when tests are run by the editor or `pytest` directly.
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Ensure our pytest_cov shim is loaded as a plugin when pytest runs.
pytest_plugins = ["pytest_cov"]
# Provide a minimal pytest integration so async tests run even when
# `pytest-asyncio` isn't installed (useful for editor runners).
import inspect
import asyncio

def pytest_configure(config):
    try:
        config.addinivalue_line("markers", "asyncio: mark test as asyncio")
    except Exception:
        pass

def pytest_pyfunc_call(pyfuncitem):
    testfunction = pyfuncitem.obj
    if inspect.iscoroutinefunction(testfunction):
        # run coroutine test directly
        asyncio.run(testfunction(**getattr(pyfuncitem, 'funcargs', {})))
        return True
    return None
