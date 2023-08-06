# Local CI Hooks

This script adds Git hooks to your repository to run the tests automatically
while pushing commits to your remotes. The idea is to avoid pushing broken
code to your remotes, automatising the process of verification.

## Installation

```bash
pip install local_ci_hooks
```

## Usage

Run the script in a repository:

```bash
local_ci_hooks --install
```

This will install the pre-push hook for you. Also, it will create a file
named `.local_ci.sh` with a dummy test. You can set your test commands
in this file.

To uninstall the hook:

```bash
local_ci_hooks --uninstall
```

## Example scripts

For modifying the CI, please, take into consideration the following
`.local_ci.sh` example files.

NodeJS:

```bash
#!/bin/bash
npm install || exit 1
npm run test || exit 1
exit 0
```

Python:

```bash
#!/bin/bash
pip install --prefix ./build . || exit 1
export PATH="./build/bin:$PATH"
export LD_LIBARY_PATH="./build/lib:$LD_LIBRARY_PATH"
pytest . || exit 1
pip uninstall <your project>
exit 0
```

Version: 0.1.1
