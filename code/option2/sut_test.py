"""
Test for sut.py
"""

from .sut import some_method_that_returns_string


def test_some_method_that_returns_string():
    assert some_method_that_returns_string() == "noop"


if __name__ == "__main__":
    test_some_method_that_returns_string()
