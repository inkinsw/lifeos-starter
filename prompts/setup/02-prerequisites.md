# Stage 2: Prerequisites

Check, report, and offer to fix. Install nothing without asking.

| Need | Check | If missing |
|---|---|---|
| git | `git --version` | Offer the install for this OS (Windows: `winget install Git.Git`; macOS: `xcode-select --install`). Required. |
| Python 3.10 or newer | `python --version` or `python3 --version` | Offer the install (Windows: `winget install Python.Python.3.12`; macOS: `brew install python`, or the installer from python.org). Recommended: the scripts need it. Without it the contract still works and the agent writes notes by hand. |
| GitHub CLI (optional) | `gh --version` | Only needed to back the workspace up to a private GitHub repository later. |

Use whichever Python command works (`python` or `python3`) everywhere the workspace says `python`, and
tell the user which one this machine uses.

Return what is installed, what was skipped, and the Python command.
