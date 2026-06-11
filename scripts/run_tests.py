#!/usr/bin/env python3
import sys
import types
import os

# ensure workspace root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import inspect
import asyncio

# Minimal fake pytest to satisfy marker and raises usage in tests
pytest = types.ModuleType("pytest")

class _Mark:
    @staticmethod
    def asyncio(fn):
        return fn

def _raises(expected):
    class CM:
        def __init__(self):
            self.value = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            if exc_type is None:
                raise AssertionError(f"Did not raise {expected}")
            if issubclass(exc_type, expected):
                # capture the exception on the context manager for `as` usage
                self.value = exc
                return True
            # re-raise unexpected exceptions
            return False

    return CM()

pytest.mark = _Mark()
pytest.raises = _raises

sys.modules.setdefault("pytest", pytest)

def run_tests_module(module_name):
    mod = __import__(module_name, fromlist=["*"])
    tests = [getattr(mod, n) for n in dir(mod) if n.startswith("test_")]
    failures = []
    for t in tests:
        try:
            if inspect.iscoroutinefunction(t):
                asyncio.run(t())
            else:
                t()
            print(f"OK: {t.__name__}")
        except Exception as e:
            print(f"FAIL: {t.__name__}: {e}")
            failures.append((t.__name__, e))
    if failures:
        print(f"\n{len(failures)} tests failed")
        for name, ex in failures:
            print(f"- {name}: {ex}")
        sys.exit(1)
    print("\nAll tests passed")

if __name__ == '__main__':
    # Discover and run all test_*.py modules under the tests package
    tests_dir = os.path.join(ROOT, 'tests')
    for fname in sorted(os.listdir(tests_dir)):
        if fname.startswith('test_') and fname.endswith('.py'):
            modname = f"tests.{fname[:-3]}"
            run_tests_module(modname)
