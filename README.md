# Python package/module management subtleties

This repo illustrates differences between two ways to structure Python code and the differences related to the execution of unit tests and debuggability in Visual Studio Code

## Option #1 - Just throw in some Python files into a directory

See the `option1` directory for this way of structuring Python code.

The `option1` directory has two files: `sut.py` and `sut_test.py`

`sut.py` contains a Python function and `sut_test.py` contains a unit test for that function. `sut` stands for "system under test".

The content of `sut.py`:

```python
"""
System under test. A sample method that returns a string
"""


def some_method_that_returns_string():
    return "noop"

```

The content of `sut_test.py`:

```python
"""
Test for sut.py
"""

from sut import some_method_that_returns_string1


def test_some_method_that_returns_string():
    assert some_method_that_returns_string() == "noop"


if __name__ == "__main__":
    test_some_method_that_returns_string()

```

This option is easy to debug: just open `sut_test.py`, put a breakpoint on the last line and press `F5` (or choose `Debug/Start Debugging` from the menu).

> If you have Python debug configurations, choose the `Python: Current File` one.

`pytest` runs with no problems. You can execute `sut_test.py` by running `python3 sut_test.py` from the `option1` directory.

One drawback is the `unresolved import 'sut' message`, which prevents VS Code from finding the function if you open `sut_test.py`, right-click on the `some_method_that_returns_string()` and choose `Go to Definition` (or press F12).

## Option #2 - declare the directory with Python files to be a package

See the `option2` directory for this way of structuring Python code.

The `option2` directory has the same two files as `option1` - `sut.py` and `sut_test.py` - plus an additional empty file - `__init__.py` - that indicates that `option2` is a Python package.

`option2/sut_test.py` looks almost identical to `option1/sut_test.py`, but notice the presence of a dot (`.`) in front of `sut` between `from` and `import`. This is called a relative import. Without it, `pytest` will fail to execute. It also enables VS Code to find the imported function when you right-click on the `some_method_that_returns_string()` and choose `Go to Definition` (or press F12).

However, debugging doesn't work anymore if you try to use the same method as described in the Option 1 section. If you try to debug, you'll get the following error:

```text
Exception has occurred: ImportError
attempted relative import with no known parent package
```

To debug, you need to create a Python debug configuration like below:

```json
        {
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "module": "option2.${fileBasenameNoExtension}",
            "console": "integratedTerminal"
            "cwd": "${workspaceFolder}/code"
        },

```

After you do that, you can debug the same way as described in Option1.

> Do not forget to set your debug configuration to `Python: Module`

If you want to execute `option2.sut_test`, open the Terminal, navigate to the `code` directory and run `python3 -m option2.sut_test`

> Notice that the current directory is `code`, that you need to specify `-m`, the name of the package and the name of the module WITHOUT the `.py` extension (`option2.sut_test`)

## Summary


Item | Option 1 | Option 2
---------|----------|---------
Package (`__init__.py` present) | No | Yes
Debug zero setup | Yes | No
Debug Config | Python: Current File | Python: Module
Execute code | `python3 sut.py` | `python3 -m option2.sut`
Current work dir | `code\option1`| `code`
